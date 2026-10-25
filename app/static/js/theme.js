(function () {
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
})();
