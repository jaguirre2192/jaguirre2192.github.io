const revealItems = document.querySelectorAll(".reveal");

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-visible");
      revealObserver.unobserve(entry.target);
    });
  },
  {
    threshold: 0.18,
  }
);

revealItems.forEach((item, index) => {
  item.style.setProperty("--delay", `${Math.min(index * 60, 360)}ms`);
  revealObserver.observe(item);
});

const driftingProjects = document.querySelectorAll("[data-drift]");

const updateDrift = () => {
  const viewportCenter = window.innerHeight * 0.5;

  driftingProjects.forEach((project) => {
    const rect = project.getBoundingClientRect();
    const distance = rect.top + rect.height * 0.5 - viewportCenter;
    const drift = Math.max(-12, Math.min(12, distance * -0.018));
    project.style.setProperty("--drift-x", `${drift}px`);
  });
};

const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

if (!mediaQuery.matches) {
  updateDrift();
  window.addEventListener("scroll", updateDrift, { passive: true });
  window.addEventListener("resize", updateDrift);
}
