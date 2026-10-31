# Maintaining LINTHESIS

Pure Python 3, no dependencies. Content lives in `data/`, strings in `data/ui.json`, layout in `build.py`, styles in `css/site.css`. Generated pages (`index.html`, `works/`, `en/`, …) are committed; CI rebuilds and fails if they are stale.

## Two languages
`data/content.json` is Chinese, `data/content.en.json` is English. Both must have the same slugs, the same links and the same link kinds; `check.py` fails otherwise. Interface text (nav, headings, button titles, stage labels) is in `data/ui.json` under `zh` and `en`.

## Add a software project (`projects`)
Add one entry to each content file:
`slug`, `title`, `sub`, `kind`, `one_liner`, `status`, `platform`, `tech`, `stage`, `cover`, `gallery`, `intro`, `features`, `links`.
Optional: `video` + `poster`, `note`, `feature` (long-form page, see Lookbook), `related`.

- **stage**: `live`, `dev` or `early`. It sets the chip and the stage note, and groups the Works index.
- **links**: a list of `{"kind", "label", "url"}`. Kinds: `demo` (try online), `download` (installer or release), `source` (code), `external` (anything else). The page shows the buttons in that order, and the closing call to action follows the kinds present: demo → "try", download → "download", otherwise "follow". Add a link only if it really exists; never infer one from a status. Set `"cta": "explore"` to override.
- **related**: `[kind, url, reason]` with kind `works`, `books`, `writing` or `lab`; works and books must exist in the data. Keep it to a few hand-picked entries, each with a reason.

## Add a book, article series or experiment
- Printed book: `print_books` (`slug`, `title`, `year`, `publisher`, `isbn`, `cover`, `intro`, `link`).
- Online book: `ebooks` (adds `sub`, `status`, optional `video`, `poster`).
- Article series entry: append `[title, url]` to an item list in `series`.
- Featured reading on Writing (6–8 items): `writing_featured` (`url` matching a series item, `theme`, `desc`).
- Experiment: append `[name, url, description]` to `lab`. `home.lab_count` and `home.writing_count` set how many show on the home page.
- Home lead and secondary works: `home.lead` and `home.secondary` (slugs).

## Update a project's status
Edit `stage`, `status`, `links` and, if needed, `note` in both languages. Check facts at the source (repo README, GitHub Releases) before writing them. Do not claim a release that has no release link.

## Update screenshots and demos
Put images in `img/projects/` (JPEG or PNG; width and height are read at build time so layout does not jump) `cover` is the card image; `gallery` lists the page images, and the first one is the main media when there is no video. Use real captures of the real product. A demo video goes in `video/` with a `poster` image.

## Build and publish
```bash
python3 build.py && python3 check.py
git add -A && git commit -m "..." && git push
```
Pushing to `main` runs `.github/workflows/pages.yml`: build, fail on stale generated files, run `check.py`, deploy to Pages. Preview locally with `python3 -m http.server` (the 404 page uses the deployed `/LINTHESIS/` path).
