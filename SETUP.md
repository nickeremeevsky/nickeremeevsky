# Publishing the GitHub profile

This package is intended for the public repository `nickeremeevsky/nickeremeevsky` (not the personal website repository). The profile README is English-first. The personal site need not be deployed for local graphics to render.

1. Review the asset licenses in `assets/tech/SOURCES.md` and `assets/icons/LICENSE.txt`, confirm rights to the Keywordly demo screenshots, and inspect all files before uploading. The provided V18 asset copies include neutral pictograms where no verified brand mark exists; WorldBible.app has a text link only because no logo was supplied.
2. Push the package contents to the profile repository's `main` branch. Do not copy the V18 website, audio, testimonials, private data, or any secret keys into this repository.
3. Run **Update profile statistics** in GitHub Actions (or `gh workflow run profile-stats.yml --ref main`). The workflow uses the repository-scoped GitHub token. The calendar is aggregate GitHub data and may include anonymized private contributions according to account visibility. Public language totals exclude this profile repository, forks and archived repositories. If the API/token cannot retrieve the calendar or commit changes, previous placeholder/data files are retained and the run fails; do not broaden token permissions without review. Weekly scheduled runs are optional and can be disabled. No PAT is needed by design; actual GitHub permissions must be tested.
4. Review the actual profile rendering on GitHub in light and dark themes. The local animated GIF plays once; static SVG is also included as a replacement for reduced motion. No third-party stats or badge services are required.
5. Recommendations are kept out of this public package until the original authors explicitly approve the final English text for publication on GitHub. A separate draft can be inserted after approval. No photos or music recordings are included.

Local validation covers SVG/XML syntax, resource paths, workflow YAML parsing and sample statistics generation; live GitHub API/Actions and rendered profile appearance require verification after upload.
