const siteData = window.__AUTHOR_SITE_DATA__;

if (!siteData) {
  throw new Error("Site data was not loaded.");
}

const app = document.querySelector("#app");

const escapeHtml = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");

const pillMarkup = (items) =>
  items
    .map((item) => `<li class="tag">${escapeHtml(item)}</li>`)
    .join("");

const renderHero = (data) => {
  const focusMarkup = data.currentFocus
    .map(
      (book) => `
        <li class="focus-item">
          <span class="focus-title">${escapeHtml(book.title)}</span>
          <div class="focus-copy">${escapeHtml(book.logline)}</div>
        </li>
      `
    )
    .join("");

  const snapshotMarkup = data.snapshot
    .map(
      (item) => `
        <li class="snapshot-item">
          <span class="snapshot-label">${escapeHtml(item.label)}</span>
          <span class="snapshot-value">${escapeHtml(item.value)}</span>
        </li>
      `
    )
    .join("");

  return `
    <header class="topbar">
      <div class="topbar-brand">
        <span class="brand-mark" aria-hidden="true">J</span>
        <div class="brand-copy">
          <span class="brand-name">${escapeHtml(data.author.name)}</span>
          <span class="brand-note">${escapeHtml(data.author.microNote)}</span>
        </div>
      </div>
      <nav class="topbar-nav" aria-label="Primary">
        <a class="ghost-link" href="#selected-work">Selected work</a>
        <a class="ghost-link" href="#library">Full library</a>
        <a class="ghost-link" href="#about">About</a>
      </nav>
    </header>

    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-main">
        <div>
          <div class="section-label">${escapeHtml(data.author.kicker)}</div>
          <h1 class="hero-title" id="hero-title">
            <span>${escapeHtml(data.author.firstName)}</span>
            <span>${escapeHtml(data.author.lastName)}</span>
          </h1>
          <p class="hero-deck">${escapeHtml(data.author.tagline)}</p>
        </div>
        <div class="hero-meta">
          <div>
            <p class="hero-note">${escapeHtml(data.author.deck)}</p>
          </div>
          <div class="hero-actions">
            <a class="solid-link" href="#selected-work">Browse manuscripts</a>
            <a class="ghost-link" href="#library">See the full shelf</a>
          </div>
        </div>
      </div>

      <aside class="hero-panel" aria-labelledby="focus-title">
        <div class="section-label">Built from the novels folder</div>
        <div>
          <h2 class="panel-heading" id="focus-title">Current pulse</h2>
          <p class="panel-copy">${escapeHtml(data.author.panelCopy)}</p>
        </div>
        <ul class="focus-list">${focusMarkup}</ul>
        <ul class="snapshot-list">${snapshotMarkup}</ul>
      </aside>
    </section>
  `;
};

const renderFeatured = (data) => {
  const cards = data.featured
    .map(
      (book, index) => `
        <article class="featured-card" style="--card-accent: ${escapeHtml(book.accent)};">
          <div class="featured-index" aria-hidden="true">${String(index + 1).padStart(2, "0")}</div>
          <div class="featured-content">
            <div class="book-kicker">
              <span>${escapeHtml(book.track)}</span>
              <span class="dot-sep" aria-hidden="true"></span>
              <span>${escapeHtml(book.genre)}</span>
            </div>
            <h3 class="book-title">${escapeHtml(book.title)}</h3>
            <p class="book-logline">${escapeHtml(book.logline)}</p>
            <p class="book-promise">${escapeHtml(book.promise)}</p>
          </div>
          <div class="featured-side">
            <div>
              <p class="feature-panel-title">Pressure points</p>
              <ul class="tag-list">${pillMarkup(book.tags)}</ul>
            </div>
            <div class="feature-theme">
              <strong>Theme question</strong>
              <p class="book-promise">${escapeHtml(book.themeQuestion)}</p>
            </div>
          </div>
        </article>
      `
    )
    .join("");

  return `
    <section class="featured-section" id="selected-work" aria-labelledby="selected-work-title">
      <div class="section-head">
        <div>
          <div class="section-label">Selected manuscripts</div>
          <h2 class="section-title" id="selected-work-title">High-concept novels with teeth.</h2>
          <p class="section-copy">${escapeHtml(data.sections.featured)}</p>
        </div>
        <div class="section-anchor">featured set / ${String(data.featured.length).padStart(2, "0")}</div>
      </div>
      <div class="featured-list">
        ${cards}
      </div>
    </section>
  `;
};

const renderLibrary = (data) => {
  const filters = data.tracks
    .map(
      (track) => `
        <button class="track-filter${track.slug === "all" ? " is-active" : ""}" type="button" data-track="${escapeHtml(track.slug)}">
          <span>${escapeHtml(track.label)}</span>
          <span class="track-count">${escapeHtml(String(track.count))}</span>
        </button>
      `
    )
    .join("");

  const rows = data.books
    .map(
      (book) => `
        <li class="library-row" data-track="${escapeHtml(book.trackSlug)}">
          <div>
            <h3 class="library-title">${escapeHtml(book.title)}</h3>
            <div class="library-lane">${escapeHtml(book.track)}</div>
          </div>
          <div class="library-genre">${escapeHtml(book.genre)}</div>
          <p class="library-summary">${escapeHtml(book.logline)}</p>
          <div class="library-source">${escapeHtml(book.sourceLabel)}</div>
        </li>
      `
    )
    .join("");

  return `
    <section class="tracks-section" id="library" aria-labelledby="library-title">
      <div class="section-head">
        <div>
          <div class="section-label">Full manuscript library</div>
          <h2 class="section-title" id="library-title">An atlas of pressure systems, haunted identities, and epic orders.</h2>
          <p class="section-copy">${escapeHtml(data.sections.library)}</p>
        </div>
        <div class="section-anchor">${escapeHtml(data.author.sourceNote)}</div>
      </div>
      <div class="tracks-shell">
        <div class="track-filters" role="toolbar" aria-label="Filter projects by track">
          ${filters}
        </div>
        <ul class="library-list" aria-live="polite">
          ${rows}
        </ul>
      </div>
    </section>
  `;
};

const renderObsessions = (data) => {
  const panels = data.obsessions
    .map(
      (item, index) => `
        <li class="obsession-panel">
          <span class="obsession-number">${String(index + 1).padStart(2, "0")}</span>
          <h3 class="obsession-title">${escapeHtml(item.title)}</h3>
          <p class="obsession-copy">${escapeHtml(item.body)}</p>
        </li>
      `
    )
    .join("");

  return `
    <section class="obsessions-section" aria-labelledby="obsessions-title">
      <div class="section-head">
        <div>
          <div class="section-label">Across the shelf</div>
          <h2 class="section-title" id="obsessions-title">The recurring obsessions are clear.</h2>
          <p class="section-copy">${escapeHtml(data.sections.obsessions)}</p>
        </div>
        <div class="section-anchor">design thesis / dossier</div>
      </div>
      <ul class="obsession-grid">
        ${panels}
      </ul>
    </section>
  `;
};

const renderAbout = (data) => {
  const footerList = data.footerNotes
    .map((item) => `<li>${escapeHtml(item)}</li>`)
    .join("");

  return `
    <section class="about-section" id="about" aria-labelledby="about-title">
      <div class="closing-intro">
        <div>
          <div class="section-label">About the work</div>
          <h2 class="closing-title" id="about-title">A portfolio built from the active shelf, not invented credentials.</h2>
          <p class="closing-intro-copy">The ending stays compact on purpose: one statement of author positioning, one note on what the site is and is not, and a clean path back to the top.</p>
        </div>
      </div>
      <div class="closing-grid">
        <article class="about-panel dark">
          <div class="section-label">Author positioning</div>
          <p class="about-copy">${escapeHtml(data.author.about)}</p>
        </article>
        <aside class="footer-panel">
          <div class="section-label">Site notes</div>
          <p class="footer-copy">${escapeHtml(data.sections.footer)}</p>
          <ul class="footer-list">${footerList}</ul>
          <div class="footer-actions">
            <span class="footer-year">Updated <span id="footerYear">${escapeHtml(String(data.currentYear))}</span></span>
            <a class="back-to-top" href="#hero-title">Back to top</a>
          </div>
        </aside>
      </div>
    </section>
  `;
};

app.innerHTML = `
  ${renderHero(siteData)}
  ${renderFeatured(siteData)}
  ${renderLibrary(siteData)}
  ${renderObsessions(siteData)}
  ${renderAbout(siteData)}
`;

const filters = Array.from(document.querySelectorAll(".track-filter"));
const rows = Array.from(document.querySelectorAll(".library-row"));

const updateLibrary = (track) => {
  let visibleCount = 0;

  rows.forEach((row) => {
    const isVisible = track === "all" || row.dataset.track === track;
    row.hidden = !isVisible;
    if (isVisible) {
      visibleCount += 1;
    }
  });

  filters.forEach((button) => {
    button.classList.toggle("is-active", button.dataset.track === track);
  });

  const libraryTitle = document.querySelector("#library-title");
  const filterLabel =
    track === "all"
      ? `An atlas of pressure systems, haunted identities, and epic orders.`
      : `An atlas filtered to ${track.replaceAll("-", " ")}.`;
  libraryTitle.setAttribute("data-visible", String(visibleCount));
  libraryTitle.setAttribute("aria-label", `${filterLabel} ${visibleCount} projects shown.`);
};

filters.forEach((button) => {
  button.addEventListener("click", () => updateLibrary(button.dataset.track));
});

updateLibrary("all");
