/* =============================================================================
   static/js/main.js  —  Interaction Layer (Phases 18–24)
   Vanilla JS, progressive enhancement, no libraries. Everything degrades to a
   fully usable no-JS experience (CSS never hides content; JS owns reveal init
   states). All motion is gated on prefers-reduced-motion.

   Modules: smooth anchors · scroll reveals · mobile dialog (focus trap /
   restore / Escape) · accessible disclosures · sticky header · hero video ·
   contact-actions toggle · first-party analytics beacons.
   ============================================================================= */
(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.add("has-js");

  var REDUCED = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var HEADER_OFFSET = 80; // matches sticky header height / scroll-margin
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------------------------------------------------- Smooth anchors ---- */
  function initAnchors() {
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest('a[href^="#"]');
      if (!a) return;
      var id = a.getAttribute("href");
      if (id === "#" || id.length < 2) return;
      var target = document.getElementById(id.slice(1));
      if (!target) return;
      e.preventDefault();
      var top = target.getBoundingClientRect().top + window.pageYOffset - HEADER_OFFSET;
      window.scrollTo({ top: top, behavior: REDUCED ? "auto" : "smooth" });
      // Move focus for keyboard/AT users without a second visual jump.
      target.setAttribute("tabindex", "-1");
      target.focus({ preventScroll: true });
    });
  }

  /* ---------------------------------------------------- Scroll reveals ---- */
  function initReveals() {
    if (REDUCED || !("IntersectionObserver" in window)) return; // content stays visible
    var selector = [
      ".site-main > section", ".product-card", ".value-card", ".article-card",
      ".certification-card", ".home-process__step", ".process-steps__step",
      ".partner-process__step", ".inquiry-next__step", ".trust-strip__item"
    ].join(",");
    var targets = $$(selector).filter(function (el) { return !el.closest(".home-hero"); });

    // Stagger per parent group so items in a row cascade gently (calm, not showy).
    var counters = new Map();
    var EASE = "cubic-bezier(.16,1,.3,1)";
    targets.forEach(function (el) {
      var parent = el.parentElement;
      var n = counters.get(parent) || 0; counters.set(parent, n + 1);
      var delay = Math.min(n * 55, 220);
      el.style.willChange = "opacity, transform";
      el.style.opacity = "0";
      el.style.transform = "translateY(12px)";
      el.style.transition = "opacity 520ms " + EASE + " " + delay + "ms, transform 520ms " + EASE + " " + delay + "ms";
    });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        el.style.opacity = "1";
        el.style.transform = "none";
        io.unobserve(el);
        // Clean up inline styles (and the GPU layer hint) after the transition.
        window.setTimeout(function () {
          el.style.transition = ""; el.style.transform = ""; el.style.opacity = ""; el.style.willChange = "";
        }, 1000);
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.08 });

    targets.forEach(function (el) { io.observe(el); });
  }

  /* ------------------------------------------------ Focusable helpers ---- */
  var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
  function focusables(container) {
    return $$(FOCUSABLE, container).filter(function (el) {
      return el.offsetWidth > 0 || el.offsetHeight > 0 || el === document.activeElement;
    });
  }

  /* ---------------------------------------------------- Mobile dialog ---- */
  function initMobileDialog() {
    var toggle = $(".site-header__toggle");
    var dialog = document.getElementById("mobile-nav");
    if (!toggle || !dialog) return;
    var closeBtn = $(".mobile-nav-dialog__close", dialog);
    var lastFocused = null;

    function open() {
      lastFocused = document.activeElement;
      dialog.hidden = false;
      toggle.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
      (closeBtn || dialog).focus();
      document.addEventListener("keydown", onKeydown, true);
    }
    function close() {
      dialog.hidden = true;
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      document.removeEventListener("keydown", onKeydown, true);
      if (lastFocused && lastFocused.focus) lastFocused.focus();
    }
    function onKeydown(e) {
      if (e.key === "Escape") { e.preventDefault(); close(); return; }
      if (e.key === "Tab") {
        var f = focusables(dialog);
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    }

    toggle.addEventListener("click", function () {
      (toggle.getAttribute("aria-expanded") === "true") ? close() : open();
    });
    if (closeBtn) closeBtn.addEventListener("click", close);
    // Close if a navigation link inside is activated.
    dialog.addEventListener("click", function (e) {
      if (e.target.closest("a[href]")) close();
    });
    // Reset when resizing up to desktop.
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1024 && !dialog.hidden) close();
    });
  }

  /* --------------------------------------------- Accessible disclosures -- */
  function initDisclosures() {
    var buttons = $$(".primary-nav__disclosure");
    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var expanded = btn.getAttribute("aria-expanded") === "true";
        buttons.forEach(function (b) { if (b !== btn) b.setAttribute("aria-expanded", "false"); });
        btn.setAttribute("aria-expanded", String(!expanded));
      });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") buttons.forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".primary-nav__item--has-children")) {
        buttons.forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
      }
    });
  }

  /* ---------------------------------------------------- Sticky header ---- */
  function initStickyHeader() {
    var header = $(".site-header");
    if (!header) return;
    var ticking = false;
    function update() {
      header.style.boxShadow = window.pageYOffset > 8 ? "0 4px 16px rgba(14,59,46,0.06)" : "";
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  /* ------------------------------------------------------- Hero video ---- */
  /* [P3B] Root cause of the "video never plays" reports: the previous gate
     returned early for ANY viewport below 1024px and for ANY touch/no-hover
     device, so phones, tablets and a phone in desktop-site mode never played
     the hero. It also left `autoplay` in the markup, so those same phones
     downloaded the WebM anyway and discarded it.
     Policy now:
       desktop (>= 1024px): hero.mp4 first, hero.webm fallback, autoplay muted;
       below 1024px: the optimised hero-mobile.* files (same footage);
       poster only under reduced motion, Save-Data, or a 2G/3G connection;
       paused while the hero is off-screen; poster shown again on any error. */
  function initHeroVideo() {
    var video = $(".home-hero__video");
    if (!video) return;
    var media = video.closest(".home-hero__media");
    var conn = navigator.connection || {};
    var slow = /(^|-)2g$|^3g$/.test(conn.effectiveType || "");
    if (REDUCED || conn.saveData || slow) {
      video.removeAttribute("autoplay");
      video.setAttribute("preload", "none");
      return;                                   // poster carries the hero
    }

    var mobile = window.matchMedia("(max-width: 1023px)").matches;
    if (mobile) {
      var mp4 = video.getAttribute("data-mobile-mp4");
      var webm = video.getAttribute("data-mobile-webm");
      if (mp4) {
        $$("source", video).forEach(function (s) { s.parentNode.removeChild(s); });
        [[mp4, "video/mp4"], [webm, "video/webm"]].forEach(function (pair) {
          if (!pair[0]) return;
          var s = document.createElement("source");
          s.src = pair[0]; s.type = pair[1];
          video.appendChild(s);
        });
      }
    }

    function fail() {
      video.classList.add("is-failed");        // CSS poster behind shows through
      if (media) media.classList.add("is-poster-only");
    }
    var sources = $$("source", video);
    if (sources.length) sources[sources.length - 1].addEventListener("error", fail);
    video.addEventListener("error", fail);
    // [P3B.1] The poster (painted behind the video) is what shows whenever the
    // video is not actually playing — before the first frame AND after a pause
    // — so a paused mid-clip frame never replaces it.
    video.addEventListener("playing", function () { if (media) media.classList.add("is-playing"); });
    ["pause", "ended", "emptied"].forEach(function (ev) {
      video.addEventListener(ev, function () { if (media) media.classList.remove("is-playing"); });
    });

    video.muted = true;
    video.defaultMuted = true;
    video.setAttribute("muted", "");
    video.setAttribute("playsinline", "");

    function tryPlay() {
      if (video.classList.contains("is-failed")) return;
      var p = video.play();
      if (p && p.catch) p.catch(function () { /* refused: poster stays */ });
    }
    var hero = video.closest(".home-hero") || video;

    if (!mobile) {
      // DESKTOP (>= 1024px): unchanged — autoplay hero.mp4 (hero.webm fallback),
      // pause off-screen, resume on return.
      // Do NOT touch `preload` here: changing it on an element that has already
      // resolved its source makes the browser fetch it early. autoplay + load().
      video.autoplay = true;
      video.load();
      tryPlay();
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (e.isIntersecting) { if (video.paused) tryPlay(); }
            else if (!video.paused) video.pause();
          });
        }, { threshold: 0 }).observe(hero);
      }
      return;
    }

    /* [P3B.1] MOBILE / TABLET (< 1024px): interaction-gated playback.
       Initial state is the poster: no autoplay, preload stays "none", and
       load() is NOT called until the first interaction — calling it on page
       load made Chromium request the video even with preload="none".
       ONE meaningful interaction unlocks playback while the hero is on screen:
         - touching / pressing on the hero (pointerdown or touchstart);
         - a swipe, wheel or scroll key anywhere while the hero is visible,
           including momentum scrolling that follows a real input;
         - pointer hover on the hero, only on devices with true hover and a
           fine pointer (a small desktop window) — never relied on for touch.
       The finger need not stay down. Leaving the viewport pauses the video
       and re-locks it; the next interaction with the hero visible (e.g. the
       swipe that scrolls it back into view) resumes it — never silently. */
    video.autoplay = false;
    video.removeAttribute("autoplay");

    var heroVisible = true, unlocked = false, lastInput = 0, loaded = false;
    function unlock() {
      if (!heroVisible) return;
      unlocked = true;
      if (!loaded) { loaded = true; video.load(); }   // first byte requested here
      if (video.paused) tryPlay();
    }
    function noteInput() { lastInput = Date.now(); }

    hero.addEventListener("pointerdown", unlock, { passive: true });
    hero.addEventListener("touchstart", unlock, { passive: true });
    if (window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
      hero.addEventListener("pointerenter", unlock, { passive: true });
    }
    window.addEventListener("touchstart", noteInput, { passive: true });
    window.addEventListener("touchmove", function () { noteInput(); unlock(); }, { passive: true });
    window.addEventListener("wheel", function () { noteInput(); unlock(); }, { passive: true });
    window.addEventListener("keydown", function (e) {
      if (/^(ArrowDown|ArrowUp|PageDown|PageUp|Home|End| |Spacebar)$/.test(e.key)) { noteInput(); unlock(); }
    });
    // Scroll counts only when it follows a real input (momentum after a
    // swipe), never programmatic scrolling or scroll restoration on load.
    window.addEventListener("scroll", function () {
      if (Date.now() - lastInput < 1500) unlock();
    }, { passive: true });

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          heroVisible = e.isIntersecting;
          if (!heroVisible) {
            unlocked = false;
            if (!video.paused) video.pause();
          } else if (unlocked && video.paused) {
            tryPlay();
          }
        });
      }, { threshold: 0 }).observe(hero);
    }
  }

  /* --------------------------------------------------- Hero load reveal -- */
  function initHeroReveal() {
    var content = document.querySelector(".home-hero__content");
    if (!content) return;
    // Two frames ensure the hidden state is painted before revealing, so the
    // transition runs on first load (calm fade + slight rise). Under reduced
    // motion the CSS transition is a no-op, so content simply appears.
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { content.classList.add("is-ready"); });
    });
  }

  /* ------------------------------------------------- Contact actions ----- */
  /* [P2] The quick-contact stack is a support, not a competitor: it hides while
     the footer (which lists every channel) is on screen, and it never collapses
     into an unlabelled control. Without JS it simply stays visible. */
  /* [P3B] The floating action is a contextual affordance, not an overlay.
     It appears only when ALL of these hold:
       - the reader is scrolling back UP (looking for what to do next) and is
         past the first screen — while scrolling down they are reading;
       - no form, footer or on-page button is anywhere on screen (the page
         already offers the action, or the control would sit on it);
       - no image or evidence block (facts, specifications, varieties,
         registrations, market lists, process steps) is in the bottom band
         where the control sits.
     Hidden by default; without JS it never appears (CSS), because the header
     menu and on-page actions already carry the route. */
  function initContactActions() {
    var wrap = $(".contact-actions");
    var toggle = $(".contact-actions__toggle", wrap || document);
    var group = $("#contact-actions-group", wrap || document);
    if (!wrap || !group) return;
    if (toggle) { toggle.hidden = true; toggle.style.display = "none"; }
    group.hidden = false;
    wrap.classList.add("is-dismissed");
    if (!("IntersectionObserver" in window)) return;

    var blocking = new Set();
    var up = false, lastY = window.pageYOffset, ticking = false;
    var link = $(".contact-actions__item.is-primary .contact-actions__link", wrap) || $("a", wrap);
    // What the control must never sit on. Checked synchronously under the
    // control's own box on every scroll frame (an IntersectionObserver
    // reports a frame late, which let it flash over a list while fading out).
    var NO_COVER = [
      "main img", "main figure", "main .btn", "main form", ".site-footer",
      ".product-summary", ".product-snapshot__list", ".product-specs__list",
      ".product-varieties__list", ".product-order__steps", ".home-process__steps",
      ".process-steps__list", ".certifications-section", ".home-markets__list",
      ".markets-current__list", ".markets-developing__list", ".markets-legend",
      ".products-note", ".trust-strip"
    ].join(",");

    function clearUnderneath() {
      if (!link || !document.elementsFromPoint) return true;
      var r = link.getBoundingClientRect();
      if (!r.width) return true;
      // While hidden the control sits 8px lower (its entry transform), so the
      // test area starts 12px above the measured box to cover where it lands.
      var top = r.top - 12;
      var pts = [[r.left + 2, top], [r.right - 2, top], [r.left + 2, r.bottom - 2],
                 [r.right - 2, r.bottom - 2], [(r.left + r.right) / 2, (top + r.bottom) / 2]];
      for (var i = 0; i < pts.length; i++) {
        var stack = document.elementsFromPoint(pts[i][0], pts[i][1]);
        for (var j = 0; j < stack.length; j++) {
          if (wrap.contains(stack[j])) continue;
          if (stack[j].closest && stack[j].closest(NO_COVER)) return false;
        }
      }
      return true;
    }
    function update() {
      var show = up && window.pageYOffset > window.innerHeight * 0.75 &&
                 blocking.size === 0 && clearUnderneath();
      wrap.classList.toggle("is-dismissed", !show);
    }
    // Any form, footer or on-page button anywhere on screen: the page already
    // offers the action, so the floating control stays away entirely.
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) blocking.add(e.target); else blocking.delete(e.target); });
      update();
    }, { rootMargin: "0px 0px 72px 0px", threshold: 0 });
    $$(".site-footer, main form, main .btn").forEach(function (el) { io.observe(el); });

    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () {
        var y = window.pageYOffset, dy = y - lastY;
        if (Math.abs(dy) > 8) { up = dy < 0; lastY = y; }
        update();
        ticking = false;
      });
    }, { passive: true });
  }

  /* ---------------------------------------------------------- Analytics -- */
  function initAnalytics() {
    function sid() {
      try {
        var k = "ref_sid", v = sessionStorage.getItem(k);
        if (!v) {
          v = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2);
          sessionStorage.setItem(k, v);
        }
        return v;
      } catch (e) { return ""; }
    }
    function send(type, meta) {
      var payload = JSON.stringify({ type: type, path: location.pathname, referrer: document.referrer, sid: sid(), meta: meta || null });
      try {
        if (navigator.sendBeacon) navigator.sendBeacon("/track", new Blob([payload], { type: "application/json" }));
        else fetch("/track", { method: "POST", headers: { "Content-Type": "application/json" }, body: payload, keepalive: true });
      } catch (e) {}
    }
    send(location.pathname.indexOf("/thank-you") > -1 ? "form_success" : "pageview");

    var started = {};
    $$("form").forEach(function (form) {
      form.addEventListener("focusin", function () {
        var id = form.action || "form";
        if (!started[id]) { started[id] = true; send("form_start", { form: id }); }
      }, { once: false });
    });

    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[href]");
      if (!a) return;
      var href = a.getAttribute("href") || "";
      if (/^https?:\/\//.test(href) && a.host !== location.host) send("outbound", { href: href });
      else if (a.classList.contains("contact-actions__link")) send("click", { action: "contact" });
    });
  }

  /* ------------------------------------------- Reading progress (article) */
  function initScrollProgress() {
    if (!document.querySelector(".article")) return; // long-form pages only
    var bar = document.createElement("div");
    bar.className = "reading-progress";
    bar.setAttribute("aria-hidden", "true");
    document.body.appendChild(bar);
    var ticking = false;
    function update() {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      var ratio = max > 0 ? Math.min(h.scrollTop / max, 1) : 0;
      bar.style.transform = "scaleX(" + ratio + ")";
      ticking = false;
    }
    function onScroll() { if (!ticking) { window.requestAnimationFrame(update); ticking = true; } }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    update();
  }

  /* ------------------------------------------- Progressive media load-in - */
  function initLazyMedia() {
    if (REDUCED) return; // reduced motion: images already shown, no fade
    $$('img[loading="lazy"]').forEach(function (img) {
      if (img.complete && img.naturalWidth > 0) return;          // already loaded
      if (img.getBoundingClientRect().top <= window.innerHeight) return; // near/above fold: LCP-safe
      img.classList.add("media-fade");
      function reveal() { img.classList.add("is-loaded"); }
      if (img.decode) img.decode().then(reveal).catch(reveal);
      img.addEventListener("load", reveal, { once: true });
      img.addEventListener("error", reveal, { once: true });
    });
  }

  /* ------------------------------------------- Contact actions settle-in - */
  function initContactActionsReady() {
    var wrap = document.querySelector(".contact-actions");
    if (!wrap) return;
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(function () { wrap.classList.add("is-ready"); });
    });
  }

  /* ------------------------------------------- Dropdown focus return ----- */
  function initDropdownFocusReturn() {
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      var open = document.querySelector('.primary-nav__disclosure[aria-expanded="true"]');
      if (open && open.parentElement && open.parentElement.contains(document.activeElement)) open.focus();
    });
  }

  /* ------------------------------------------------------------- Boot ---- */
  function boot() {
    initAnchors();
    initReveals();
    initMobileDialog();
    initDisclosures();
    initStickyHeader();
    initHeroVideo();
    initHeroReveal();
    initContactActions();
    initContactActionsReady();
    initLazyMedia();
    initScrollProgress();
    initDropdownFocusReturn();
    initAnalytics();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
