# P2 editorial polish: change notes

- **CTA**: each project has a `cta` in the JSON (try / download / follow / explore) that sets the bottom heading. `check.py` fails the build if "try" has no non-GitHub link, or "download" has no release/installer link. Current: Lookbook "亲自试一试" (has a live link); Aide, Atlas, Research2Video, PersonalSpace "查看开发进展" (source only); Radar "探索这个项目". No project has a download link, so none says "下载与安装".
- **Related**: Lookbook, Aide, Atlas and Research2Video each carry three hand-picked links (works, books, writing, lab) with the reason. Data is the `related` list in `data/content*.json`; a missing target stops the build.
- **Writing**: numbered, larger titles; on small screens the read link drops below the description.
- **Header**: below 900px the nav drops the Chinese labels so it stays on one row at 768px.
- Checked at 1440, 768 and 375 px; screenshots in this folder.
