# P1 content and experience polish: change notes

**Works**
- Every project now has a `stage` (live / in development / early version) in the JSON. Cards show a status chip, and the Works index is grouped by stage.
- All project pages use one template: status note, real media first (demo video where one exists, otherwise the main screenshot), then intro, features, notes, screenshots, stack and links. Lookbook keeps its richer walk-through.
- No screen recordings were added: the other projects are native macOS apps or local services that I did not run here, and no simulated footage was made. Atlas and Lookbook keep their existing videos.

**Writing**: a "Start here" list of 8 series (title, one-line description, topic, link), above the full catalogue. Descriptions come from each site's own contents page or description. Home shows the first four. No view counts or ratings.

**Consistency**
- Images carry width/height read from the file header, so the page does not jump while loading; tall screenshots are capped.
- Duplicate and unused CSS rules (hero, tags, badge, todo, compact series) removed; mobile type and spacing adjusted.
- Per-page share image (project cover), `twitter:title` and `twitter:description` added.

**Verification**: `build.py` and `check.py` pass (19 zh + 19 en pages, all links and assets resolve). All 24 key pages were loaded at 375px: no horizontal overflow, no broken images. Before/after screenshots are in this folder.
