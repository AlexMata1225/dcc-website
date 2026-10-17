# Deacon Consulting Club website

Official website of Deacon Consulting Club at Wake Forest University: **https://wfudcc.org/**.

## Pages

Home, Our work, Analyst Program, The club and calendar, Our people, Partner with DCC, and Resources.

## Editing and building

The site is static HTML, CSS, and vanilla JavaScript with no npm dependencies. `build.py` contains the page content, board, event calendar, and resource list. `site.css` and `campus.css` contain the design; `site.js` contains menu, calendar, legacy-link routing, and resource-search behavior. Assets and fonts are served locally.

Run with Python 3.12 or newer after editing content, CSS, or JavaScript:

```sh
python3 build.py --production
```

Production builds include canonical URLs and allow search indexing. Omitting `--production` creates a non-indexable local review build, which must not be committed for production. The build updates content hashes for CSS and JavaScript. It regenerates all seven HTML pages plus `events.js` and `events.json`.

For local review:

```sh
python3 -m http.server 4317 --bind 127.0.0.1
```

## Publishing and domain

Push reviewed production files to `main`. The existing workflow in `.github/workflows/pages.yml` deploys the repository through GitHub Pages. The custom domain `wfudcc.org` is configured in Settings → Pages. DNS and HTTPS settings are unchanged by the redesign. No Cloudflare deployment is required.

The previous site is preserved in Git history at commit `5645bc9259e24347ba855bc46c6808e727d48509`. Use a normal revert of the redesign commit if rollback is needed; do not rewrite branch history. Older asset paths are retained for visitors with cached HTML. Old homepage anchors route to their corresponding new pages.

## Content and photography

The fall 2026 Analyst Program has 14 participants, confirmed by the club. Program, board, calendar, and contact content came from the previous public website. Keep semester and application status current in `build.py`. Meetings are interpreted in America/New_York time; calendar downloads contain upcoming event starts and do not invent end times.

The two club photographs were supplied by the club. The Wait Chapel image and DCC monogram are retained from the previous website. Additional campus photographs are credited on their pages:

- [Hearn Plaza in autumn — Wake Admissions](https://admissions.wfu.edu/visit/tour/)
- [Founders Living Room — Wake Forest Parents & Families](https://parents.wfu.edu/2017/02/panoramic-view-of-farrell-hall-living-room/)
- [Farrell Hall exterior — Wake School of Business](https://business.wfu.edu/campus-winston-salem/farrell-hall/)

The Farrell interior photograph is from 2017 and depicts campus life, not the current DCC cohort. Campus-image public reuse permission has not been independently documented. Open Sans is distributed under the included SIL Open Font License. No headshots, testimonials, client names, or outcomes were generated.

## Verification

All seven page layouts were reviewed at desktop and phone widths; the five pages with new campus photography were also checked at tablet width. Navigation, FAQs, resource search/filter/reset, and the calendar download were exercised. Local links and assets were validated. Search metadata and old homepage anchors were checked for the production release.

## Contact

wakeforestdcc@gmail.com · [@wfudcc](https://www.instagram.com/wfudcc/)
