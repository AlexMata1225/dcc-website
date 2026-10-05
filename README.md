# Deacon Consulting Club — Website

The official website of the **Deacon Consulting Club** (formerly the Wake Forest
Management Consulting Club) at Wake Forest University.

**Live site:** https://wfudcc.org (also reachable at https://alexmata1225.github.io/dcc-website/,
which redirects there once the custom domain is set)

## Pages

- `index.html` — Home: hero, club stats, about, our work, programs, Analyst Program,
  semester schedule, executive board, and how to get involved
- `resources.html` — Case-prep library: recommended platforms, industry primers,
  networking guides, and interview prep

## Tech

Plain HTML/CSS with a small vanilla JS file — no frameworks, no build step.

- `assets/styles.css` — shared design system (Wake Forest gold + black, editorial style)
- `assets/site.js` — mobile nav, scroll reveals, footer year, next-meeting banner
- `assets/` — DCC logo files, WFU logo, favicons

## Editing

- **Update the board:** in `index.html`, find the `board__grid` section — duplicate a
  `board-card` block and edit the initials, name, role, and LinkedIn link.
- **Update the schedule:** in `index.html`, edit the `timeline__row` blocks in the
  `#schedule` section. Each row's `data-date` (YYYY-MM-DD) decides which meeting the hero
  banner and "Next up" card show, and which rows are greyed out as past. Add
  `data-where="..."` to a row if that meeting isn't at 5:00 PM in Farrell Hall A27.
- **Add a page:** copy `resources.html` as a starting point (it has the nav + footer),
  keep the `assets/styles.css` link, and set `aria-current="page"` on the active nav item.
- **Preview locally:** run `python3 -m http.server` in this folder and open
  `http://localhost:8000`.

## Domain

`wfudcc.org` points at GitHub Pages. The site deploys through the Actions workflow in
`.github/workflows/pages.yml`, so the custom domain is set in the repo's
**Settings → Pages**, not with a `CNAME` file (Actions deploys ignore that file).
DNS records at the registrar:

| Type  | Name  | Value |
|-------|-------|-------|
| A     | `@`   | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
| AAAA  | `@`   | `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153` |
| CNAME | `www` | `alexmata1225.github.io` |

If the repo moves to another account or org, update the `www` CNAME to that owner's
`<name>.github.io` and re-enter the custom domain in the new repo's Pages settings.

## History

The old Management Consulting Club site was published under `/mcc` for side-by-side
review during the rebrand. It was retired from the live site in October 2026 and is
preserved in git at the tag `mcc-site-archive` (`git checkout mcc-site-archive -- mcc`
restores it).

## Contact

wakeforestdcc@gmail.com · Instagram [@wfudcc](https://www.instagram.com/wfudcc/)
