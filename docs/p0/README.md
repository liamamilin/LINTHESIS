# Website Polish P0: change notes

**Home** (`index.html`, `en/index.html`): larger hero with a rule and CTAs; "Selected work" section with Lookbook as a full-width lead (real screenshot + key numbers), Aide and Application Atlas as secondary cards, remaining works as a text list linking to Works. Books shows the four printed books plus a link to the online guides; Writing shows series names with counts; Lab shows three entries.

**Lookbook detail** (`works/lookbook/`, `en/works/lookbook/`): answers, in order, what it is, the problem, what you can see (five real screenshots of the live site plus the existing demo video), where to use it, and the design/tech. Other project pages keep the previous template.

**Build**: UI strings moved to `data/ui.json`; the home layout and the Lookbook story live in `data/content*.json` (`home`, `feature`). `check.py` verifies zh/en page parity and that every internal link and asset path resolves. GitHub Actions now runs `build.py`, fails if generated files are stale, runs `check.py`, then deploys.

Screenshots: `before-*` and `after-*` in this folder. New images in `img/projects/lookbook-*.jpg` were captured from https://liamamilin.github.io/Lookbook/.
