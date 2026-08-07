# Herbert | Personal Blog

A personal blog built from an HTML/CSS/JS vCard template and hosted for free on **GitHub Pages**.

## About

IC design engineer. Research interests: **GPU architecture** and **Network-on-Chip (NoC) modeling & implementation**.

## Directory structure

```
.
├── index.html          # Home (Home / About / Skills / Resume / Services / Works / Blog / Contact)
├── blog-single.html    # Single blog post page
├── css/                # Stylesheets
├── js/                 # Scripts
├── fonts/              # Icon fonts
└── images/             # Image assets
```

> All asset references use **relative paths**, so the site loads correctly whether it is served from a user site (`<username>.github.io`) or a project subpath.

## Local preview

Open `index.html` directly in a browser, or run a local server:

```bash
# Python 3
python -m http.server 8000
# then visit http://localhost:8000
```

## Deploy to GitHub Pages

1. Push the code to the `main` branch root of your GitHub repository.
2. For a user site, rename the repository to `<username>.github.io` (e.g. `hujian404.github.io`).
3. In the repository, go to **Settings → Pages**, set Source to the `main` branch and `/ (root)` directory, then save.
4. Wait 1–2 minutes and visit `https://<username>.github.io`.

## Customization

Content to edit lives in `index.html` and `blog-single.html`:

- **Author / tagline**: search for `Herbert`, `IC designer` / `GPU architect` / `NoC researcher`.
- **Contact**: search for `3194446884@qq.com`, `hujian404`.
- **Social links**: search for `github.com/hujian404`, `mailto:`.
- **Blog posts**: edit the `news-block` items under `id="blog"` in `index.html`, and the post body in `blog-single.html`.
- **Resume / Works**: currently placeholders — replace with real education, experience, and project entries when ready.
- **Contact form**: uses `mailto:` so it works on static hosting. For a richer form, integrate a service such as [Formspree](https://formspree.io/) and replace the `<form>` `action`.

## Notes

- The map widget depends on a Google Maps API key. Without a valid key the map area simply stays empty; other features are unaffected.
