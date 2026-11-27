"""Generate local SVG cards from GitHub API data; never export repo names or tokens."""
import collections
import datetime as dt
import html
import json
import os
import pathlib
import urllib.request
import urllib.parse

USER = 'nickeremeevsky'
ROOT = pathlib.Path(__file__).resolve().parents[1] / 'assets' / 'stats'
COLORS = ['#197765', '#426b9e', '#ad7441', '#765a9a', '#b25969', '#78838c']

def escape(text):
    return html.escape(str(text), quote=True)

def card(title, body, height=132):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}" viewBox="0 0 900 {height}" role="img">'
            f'<title>{escape(title)}</title><rect width="898" height="{height-2}" x="1" y="1" rx="12" fill="#f5f7f5" stroke="#d5ded8"/>'
            f'<g font-family="Arial, Helvetica, sans-serif" fill="#25392f"><text x="24" y="32" font-size="19" font-weight="bold">{escape(title)}</text>{body}</g></svg>\n')

def note(text, y=62):
    return f'<text x="24" y="{y}" font-size="14" fill="#4e6258">{escape(text)}</text>'

def languages_svg(counts):
    if not counts or sum(counts.values()) == 0:
        return card('Top languages', note('No eligible public repositories with reported code bytes.'), 88)
    top = sorted(counts.items(), key=lambda x: (-x[1], x[0])); total = sum(v for _, v in top)
    groups = top[:5] + ([('Other', sum(v for _, v in top[5:]))] if len(top)>5 else [])
    body = note('Public, owned, non-fork, non-archived repositories · code bytes', 54)
    x = 24.0
    for i, (name, value) in enumerate(groups):
        width = 852 * value / total
        body += f'<rect x="{x:.2f}" y="68" width="{width:.2f}" height="13" fill="{COLORS[i]}"/>'
        x += width
        cx = 24 + (i % 3) * 285; cy = 105 + (i // 3) * 24
        body += f'<rect x="{cx}" y="{cy-11}" width="11" height="11" rx="2" fill="{COLORS[i]}"/><text x="{cx+18}" y="{cy}" font-size="14">{escape(name)} · {value/total:.1%}</text>'
    return card('Top languages', body, 150)

def contributions_svg(calendar):
    weeks=calendar['weeks']; body=note(f"{calendar['totalContributions']} contributions · GitHub-reported rolling year",54)
    palette=['#dfe7e0','#b9daca','#79b49c','#36866c','#155743']
    for i, week in enumerate(weeks):
        for day in week['contributionDays']:
            date=dt.date.fromisoformat(day['date']); n=day['contributionCount']; level=0 if n==0 else 1 if n<=2 else 2 if n<=5 else 3 if n<=10 else 4
            x=24+i*15; y=69+((date.weekday()+1)%7)*15
            body += f'<rect x="{x}" y="{y}" width="12" height="12" rx="2" fill="{palette[level]}"><title>{date.isoformat()}: {n} contributions</title></rect>'
    body += note('Sunday to Saturday · darker cells indicate more contributions',192)
    return card('Contribution calendar',body,211)

def request(path, token, payload=None):
    url='https://api.github.com'+path
    data=None if payload is None else json.dumps(payload).encode()
    req=urllib.request.Request(url,data=data,headers={'Accept':'application/vnd.github+json','Authorization':'Bearer '+token,'X-GitHub-Api-Version':'2022-11-28','User-Agent':'ne-profile-stats','Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as resp:
        return json.load(resp)

def main():
    token=os.environ['GH_TOKEN']; counts=collections.Counter(); page=1
    while True:
        repos=request(f'/users/{USER}/repos?type=owner&per_page=100&page={page}',token)
        for repo in repos:
            if repo['private'] or repo['fork'] or repo['archived'] or repo['owner']['login'].lower()!=USER.lower() or repo['name'].lower()==USER.lower():
                continue
            langs=request(f"/repos/{USER}/{urllib.parse.quote(repo['name'],safe='')}/languages",token)
            counts.update(langs)
        if len(repos)<100: break
        page+=1
    query='query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}'
    data=request('/graphql',token,{'query':query,'variables':{'login':USER}})
    if data.get('errors') or not data.get('data',{}).get('user'):
        raise RuntimeError('GitHub contribution calendar unavailable; previous files retained')
    calendar=data['data']['user']['contributionsCollection']['contributionCalendar']
    rendered={'languages.svg':languages_svg(counts),'contributions.svg':contributions_svg(calendar)}
    for name,value in rendered.items():
        (ROOT/name).write_text(value,encoding='utf-8')

if __name__=='__main__':
    main()
