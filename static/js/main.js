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
  function initHeroVideo() {
    var video = $(".home-hero__video");
    if (!video) return;
    video.muted = true;
    video.setAttribute("playsinline", "");
    video.setAttribute("preload", "metadata");
    if (REDUCED) { try { video.pause(); } catch (e) {} return; }
    var hero = video.closest(".home-hero");
    function play() { var p = video.play(); if (p && p.catch) p.catch(function () {}); }
    function pause() { try { video.pause(); } catch (e) {} }
    if (hero) {
      hero.addEventListener("pointerenter", play);
      hero.addEventListener("pointerleave", pause);
      hero.addEventListener("focusin", play);
      hero.addEventListener("focusout", pause);
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
  function initContactActions() {
    var wrap = $(".contact-actions");
    var toggle = $(".contact-actions__toggle", wrap || document);
    var group = $("#contact-actions-group", wrap || document);
    if (!wrap || !toggle || !group) return;
    var mq = window.matchMedia("(max-width: 640px)");
    function apply() {
      if (mq.matches) {
        wrap.classList.add("contact-actions--enhanced");
        toggle.style.display = "inline-flex";
        setExpanded(false);
      } else {
        wrap.classList.remove("contact-actions--enhanced");
        toggle.style.display = "none";
        group.hidden = false;
        toggle.setAttribute("aria-expanded", "true");
      }
    }
    function setExpanded(v) { group.hidden = !v; toggle.setAttribute("aria-expanded", String(v)); }
    toggle.addEventListener("click", function () {
      setExpanded(toggle.getAttribute("aria-expanded") !== "true");
    });
    (mq.addEventListener ? mq.addEventListener("change", apply) : mq.addListener(apply));
    apply();
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
