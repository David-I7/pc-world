function toggleTheme() {
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
    btn.addEventListener("click", function () {
      const current = getEffectiveTheme();
      const next = current === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("pc_world_theme", next);
    });
  });
}

toggleTheme();
