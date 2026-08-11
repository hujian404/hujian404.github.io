/* Sidebar hide/show toggle for blog & series pages.
 *
 * Only runs on pages whose <body> has class "sidebar-toggleable"
 * (blog-single, series, booksim-series, constellation-series,
 * garnet-series, note). About / Resume / Services / Works / Home
 * (index.html) do NOT carry that class, so the toggle never appears
 * there and the sidebar always stays visible.
 *
 * State persists across pages via localStorage("herbert-sidebar-hidden").
 * On mobile (<=1199px) the toggle is hidden via CSS because the author
 * sidebar is already display:none there.
 */
(function () {
    "use strict";

    function ready(fn) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", fn);
        } else {
            fn();
        }
    }

    ready(function () {
        var body = document.body;
        if (!body || !body.classList.contains("sidebar-toggleable")) return;

        var STORAGE_KEY = "herbert-sidebar-hidden";

        // Build the floating toggle button.
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "sidebar-toggle";
        btn.setAttribute("aria-label", "Toggle author sidebar");
        btn.setAttribute("title", "Hide / show author sidebar");
        btn.innerHTML = '<i class="fa fa-caret-left"></i>';
        body.appendChild(btn);

        // Apply persisted state (and a default). We default to visible,
        // so only apply the hidden class if the stored value is "1".
        try {
            if (window.localStorage.getItem(STORAGE_KEY) === "1") {
                body.classList.add("sidebar-hidden");
            }
        } catch (e) {
            /* localStorage may be unavailable (private mode); ignore. */
        }

        btn.addEventListener("click", function () {
            var hidden = body.classList.toggle("sidebar-hidden");
            try {
                window.localStorage.setItem(STORAGE_KEY, hidden ? "1" : "0");
            } catch (e) {
                /* ignore storage errors */
            }
        });
    });
})();
