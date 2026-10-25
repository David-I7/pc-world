function toggleTheme() {
  const toggleBtn = document.getElementById("theme-toggle");
  if (!toggleBtn) return;

  function getEffectiveTheme() {
    const currentAttr = document.documentElement.getAttribute("data-theme");
    if (currentAttr) return currentAttr;
    return window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light";
  }

  toggleBtn.addEventListener("click", function () {
    const current = getEffectiveTheme();
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("pc_world_theme", next);
  });
}

toggleTheme();
