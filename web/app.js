(function () {
  "use strict";

  let plugins = [];
  let activeCategory = "all";

  const grid = document.getElementById("plugin-grid");
  const searchInput = document.getElementById("search");
  const categoriesEl = document.getElementById("categories");
  const noResults = document.getElementById("no-results");
  const themeToggle = document.getElementById("theme-toggle");

  // Theme
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark" || (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
    document.documentElement.setAttribute("data-theme", "dark");
  }

  themeToggle.addEventListener("click", function () {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  });

  // Fetch plugins
  fetch("plugins.json")
    .then(function (r) { return r.json(); })
    .then(function (data) {
      plugins = data;
      renderCategories();
      render();
    })
    .catch(function () {
      grid.innerHTML = '<p class="no-results">Failed to load plugins. Run <code>cli build-web</code> first.</p>';
    });

  // Search
  searchInput.addEventListener("input", function () {
    render();
  });

  function getCategories() {
    var cats = {};
    plugins.forEach(function (p) { cats[p.category] = true; });
    return Object.keys(cats).sort();
  }

  function renderCategories() {
    var cats = getCategories();
    categoriesEl.innerHTML = '<button class="cat-btn active" data-cat="all">All</button>';
    cats.forEach(function (cat) {
      var btn = document.createElement("button");
      btn.className = "cat-btn";
      btn.setAttribute("data-cat", cat);
      btn.textContent = cat;
      categoriesEl.appendChild(btn);
    });

    categoriesEl.addEventListener("click", function (e) {
      if (e.target.classList.contains("cat-btn")) {
        activeCategory = e.target.getAttribute("data-cat");
        categoriesEl.querySelectorAll(".cat-btn").forEach(function (b) { b.classList.remove("active"); });
        e.target.classList.add("active");
        render();
      }
    });
  }

  function getFiltered() {
    var q = searchInput.value.toLowerCase().trim();
    return plugins.filter(function (p) {
      if (activeCategory !== "all" && p.category !== activeCategory) return false;
      if (!q) return true;
      var allText = [p.name, p.description].concat(p.keywords || []).concat(p.skills || []);
      return allText.some(function (t) { return t.toLowerCase().includes(q); });
    });
  }

  function render() {
    var filtered = getFiltered();
    if (filtered.length === 0) {
      grid.innerHTML = "";
      noResults.hidden = false;
      return;
    }
    noResults.hidden = true;

    grid.innerHTML = filtered.map(function (p) {
      var keywords = (p.keywords || []).map(function (k) {
        return '<span class="keyword">' + escapeHtml(k) + '</span>';
      }).join("");

      var skills = (p.skills || []).map(function (s) {
        return '<li>' + escapeHtml(s) + '</li>';
      }).join("");

      var agentBadge = p.hasAgent ? ' <span class="keyword" style="background:#4361ee;color:#fff">agent</span>' : '';

      return (
        '<div class="plugin-card">' +
          '<h3>' + escapeHtml(p.name) + ' <span class="version">v' + escapeHtml(p.version) + '</span>' + agentBadge + '</h3>' +
          '<p class="description">' + escapeHtml(p.description) + '</p>' +
          '<p class="meta">' + escapeHtml(p.category) + '</p>' +
          (skills ? '<ul class="skill-list">' + skills + '</ul>' : '') +
          '<div class="keywords">' + keywords + '</div>' +
        '</div>'
      );
    }).join("");
  }

  function escapeHtml(str) {
    var div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }
})();
