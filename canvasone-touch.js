(() => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const progress = document.querySelector(".scroll-progress__bar");
  const glow = document.querySelector(".cursor-glow");
  const header = document.querySelector("#site-header");

  let scrollQueued = false;
  const updateProgress = () => {
    const range = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = range > 0 ? Math.min(1, Math.max(0, window.scrollY / range)) : 0;
    if (progress) progress.style.transform = `scaleX(${ratio})`;
    header?.classList.toggle("is-scrolled", window.scrollY > 24);
    scrollQueued = false;
  };
  const queueProgress = () => {
    if (scrollQueued) return;
    scrollQueued = true;
    window.requestAnimationFrame(updateProgress);
  };
  window.addEventListener("scroll", queueProgress, { passive: true });
  window.addEventListener("resize", queueProgress, { passive: true });
  updateProgress();

  const navLinks = [...document.querySelectorAll(".primary-nav a[href^='#']")];
  if ("IntersectionObserver" in window && navLinks.length) {
    const sections = navLinks
      .map((link) => document.querySelector(link.getAttribute("href")))
      .filter(Boolean);
    const navObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        navLinks.forEach((link) => {
          const active = link.getAttribute("href") === `#${entry.target.id}`;
          link.classList.toggle("is-active", active);
          if (active) link.setAttribute("aria-current", "location");
          else link.removeAttribute("aria-current");
        });
      });
    }, { rootMargin: "-42% 0px -50% 0px", threshold: 0 });
    sections.forEach((section) => navObserver.observe(section));
  }

  const revealTargets = document.querySelectorAll(
    ".intro__copy, .metric, .featured-card, .industry-band__content, .section-heading, .service-card, .package-band__inner, .principle-card, .statement-band > p, .approach__heading, .journey-step, .contact__heading, .contact-card, .healthcare-callout, .footer-main"
  );
  if (!reduceMotion && "IntersectionObserver" in window && revealTargets.length) {
    [...revealTargets].forEach((element, index) => {
      element.classList.add("touch-reveal");
      element.style.setProperty("--reveal-delay", `${(index % 4) * 65}ms`);
    });
    document.documentElement.classList.add("motion-ready");
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in-view");
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -7% 0px" });
    revealTargets.forEach((element) => revealObserver.observe(element));
  }

  if (!finePointer || reduceMotion) return;

  if (glow) {
    let framePending = false;
    let pointerX = 0;
    let pointerY = 0;
    window.addEventListener("pointermove", (event) => {
      pointerX = event.clientX;
      pointerY = event.clientY;
      if (framePending) return;
      framePending = true;
      window.requestAnimationFrame(() => {
        glow.style.transform = `translate3d(${pointerX}px, ${pointerY}px, 0) translate(-50%, -50%)`;
        glow.classList.add("is-visible");
        framePending = false;
      });
    }, { passive: true });
    document.addEventListener("pointerout", (event) => {
      if (!event.relatedTarget) glow.classList.remove("is-visible");
    });
  }

  document.querySelectorAll(".hero__visual, .featured-card, .service-card, .principle-card, .contact-card").forEach((card) => {
    card.addEventListener("pointermove", (event) => {
      const rect = card.getBoundingClientRect();
      const x = (event.clientX - rect.left) / rect.width;
      const y = (event.clientY - rect.top) / rect.height;
      card.style.setProperty("--spot-x", `${x * 100}%`);
      card.style.setProperty("--spot-y", `${y * 100}%`);
      if (card.classList.contains("hero__visual")) {
        card.style.setProperty("--tilt-x", `${(0.5 - y) * 3.5}deg`);
        card.style.setProperty("--tilt-y", `${(x - 0.5) * 5}deg`);
        card.querySelector(".studio-board")?.style.setProperty("transform", `rotateX(${(0.5 - y) * 3.5}deg) rotateY(${(x - 0.5) * 5}deg)`);
      } else {
        card.style.transform = `perspective(950px) rotateX(${(0.5 - y) * 3}deg) rotateY(${(x - 0.5) * 4}deg) translateY(-3px)`;
      }
    }, { passive: true });
    card.addEventListener("pointerleave", () => {
      card.style.transform = "";
      card.style.removeProperty("--tilt-x");
      card.style.removeProperty("--tilt-y");
      if (card.classList.contains("hero__visual")) {
        const board = card.querySelector(".studio-board");
        if (board) board.style.transform = "";
      }
    });
  });
})();
