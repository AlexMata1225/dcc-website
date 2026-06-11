# Deacon Consulting Club — Website

The official website of the **Deacon Consulting Club** (formerly the Wake Forest
Management Consulting Club) at Wake Forest University.

**Live site:** https://alexmata1225.github.io/dcc-website/

## Pages

- `index.html` — Home: hero, club stats, about, our work, programs, semester schedule,
  executive board, and how to get involved
- `resources.html` — Case-prep library: recommended platforms, industry primers,
  networking guides, and interview prep

## Tech

Plain HTML/CSS with a small vanilla JS file — no frameworks, no build step.

- `assets/styles.css` — shared design system (Wake Forest gold + black, editorial style)
- `assets/site.js` — mobile nav, scroll reveals, footer year
- `assets/` — DCC logo files, WFU logo, favicons

## Editing

- **Update the board:** in `index.html`, find the `board__grid` section — duplicate a
  `board-card` block and edit the initials, name, role, and LinkedIn link.
- **Add a page:** copy `resources.html` as a starting point (it has the nav + footer),
  keep the `assets/styles.css` link, and set `aria-current="page"` on the active nav item.
- **Preview locally:** run `python3 -m http.server` in this folder and open
  `http://localhost:8000`.

## Contact

wakeforestmcc@gmail.com · Instagram [@wfumcc](https://www.instagram.com/wfumcc/)
