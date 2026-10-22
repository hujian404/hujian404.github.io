# Highlight.js 11.11.1

Vendored browser assets for Markdown code fences. Loaded locally by `note.html`;
no runtime CDN requests are needed.

- `highlight.min.js`: official common-language browser build (including C/C++, Bash).
- `scala.min.js`: additional Scala grammar for Chisel examples.
- `github-dark.min.css`: GitHub Dark syntax colors. The site's existing `pre` / `code`
  rules retain their spacing, background, font and scrolling behavior.
- `LICENSE`: upstream BSD-3-Clause license.

Source: https://github.com/highlightjs/cdn-release/tree/11.11.1/build

Downloaded from the version-pinned jsDelivr mirror of that repository. The license
is from https://github.com/highlightjs/highlight.js/blob/11.11.1/LICENSE.

Only explicitly labeled, registered languages are highlighted after Markdown is
inserted into the reader. Unlabeled and unsupported code fences remain plain text.
