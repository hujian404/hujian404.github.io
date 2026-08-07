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

1. Push the code to the `main` branch root of your GitHub repository.
2. For a user site, rename the repository to `<username>.github.io`.
3. In the repository, go to **Settings → Pages**, set Source to the `main` branch and `/ (root)` directory, then save.
4. Wait 1–2 minutes and visit `https://<username>.github.io`.

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
