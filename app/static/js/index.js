function loadTheme() {
  const savedTheme = localStorage.getItem("pc_world_theme");
  if (savedTheme) {
    document.documentElement.setAttribute("data-theme", savedTheme);
  } else {
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)",
    ).matches;

    if (prefersDark) {
      document.documentElement.setAttribute("data-theme", "dark");
    }
  }
}

loadTheme();

function addThemeEventListeners() {
  const toggleBtns = document.querySelectorAll("[data-theme-toggle]");
  if (!toggleBtns.length) return;

  function getEffectiveTheme() {
    const currentAttr = document.documentElement.getAttribute("data-theme");
    if (currentAttr) return currentAttr;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  toggleBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const currentTheme = getEffectiveTheme();
      const next = currentTheme === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("pc_world_theme", next);
    });
  });
}

addThemeEventListeners();
