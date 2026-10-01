(() => {
  let theme;
  try { theme = localStorage.getItem('blogger-theme') || localStorage.getItem('theme'); } catch (_) {}
  const dark = theme ? theme === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
})();
