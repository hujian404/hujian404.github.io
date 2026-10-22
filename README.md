# Personal Website

A personal portfolio & blog built from a static HTML/CSS/JS vCard template, hosted for free on **GitHub Pages**.

**Live site:** https://hujian404.github.io

## Features

- Single-page card-based layout with smooth transitions between sections
- Multiple blog series / columns rendered client-side from Markdown files
- Fully responsive — adaptive layout on mobile, tablet, and desktop

## Local preview

Open `index.html` directly in a browser, or run a local server:

```bash
# Python 3
python -m http.server 8000
# then visit http://localhost:8000
```

## Deploy to GitHub Pages

1. Push the code to the `main` branch of your GitHub repository.
2. In **Settings → Pages**, set Source to **GitHub Actions**.
3. The **Sync resume and deploy blog** workflow publishes the static blog and builds the Jekyll resume at `/resume/`.
4. Check the workflow's deployment result, then visit `https://hujian404.github.io/`.

## Resume submodule and automatic updates

The homepage's **Resume** section embeds the personal homepage from
[`hujian404/hujian`](https://github.com/hujian404/hujian). It also links to the
standalone homepage at `/resume/` and CV at `/resume/cv/`.
The source is a Git submodule at `resume/`, tracking its `master` branch.
The resume uses a shared bilingual profile in `_data/profile.yml`: Chinese at
`/resume/` and English at `/resume/en/`, with corresponding CV routes. Use the
中文 / English buttons to switch language while preserving the current section.

```bash
git clone --recurse-submodules https://github.com/hujian404/hujian404.github.io.git
# For an existing checkout:
git submodule update --init --recursive
# To pull the latest resume locally:
git submodule update --remote resume
```

Edit and push resume content in `hujian404/hujian`. The blog workflow checks
the tracked branch hourly (at minute 17 UTC), commits any new submodule revision,
builds the resume with the correct blog URL and `/resume` base path, and deploys
both sites in one Pages artifact. Pushes to the blog's `main` branch and manual
**Actions → Sync resume and deploy blog → Run workflow** runs also synchronize.
No personal access token or cross-repository secret is required for this public
submodule. The workflow requests `contents: write` to record its revision.
Scheduled GitHub Actions can be delayed; this is not instantaneous push syncing.
GitHub may disable scheduled workflows after 60 days without repository activity;
re-enable the workflow in Actions if necessary.

The original Jekyll source and its configuration remain in the submodule. The
blog only overrides the deployment URL and base path at build time. Future
updates to profile text, CV, publications, styling, and assets therefore flow
through from the resume repository. Local `python -m http.server` previews the
static blog only; `/resume/` needs a Jekyll build (the workflow performs it).

## Directory structure

```
.
├── *.html              # Pages (index, blog, series, note reader, etc.)
├── css/                # Stylesheets
├── js/                 # Scripts
├── notes/              # Markdown notes grouped by series
├── fonts/              # Icon fonts
└── images/             # Image assets
```

All asset references use **relative paths**, so the site loads correctly whether it is served from a user site (`<username>.github.io`) or a project subpath.

## Notes

- The map widget depends on a Google Maps API key. Without a valid key the map area simply stays empty; other features are unaffected.
