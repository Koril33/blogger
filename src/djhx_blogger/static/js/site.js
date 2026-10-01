(() => {
  const toggle = document.querySelector('#theme-toggle');
  if (toggle) {
    toggle.hidden = false;
    const sync = () => toggle.setAttribute('aria-pressed', String(document.documentElement.dataset.theme === 'dark'));
    sync();
    toggle.addEventListener('click', () => {
      const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      document.documentElement.dataset.theme = theme;
      try { localStorage.setItem('blogger-theme', theme); } catch (_) {}
      sync();
    });
  }
  if (navigator.clipboard && window.isSecureContext) {
    document.querySelectorAll('.article-content pre').forEach(pre => {
      const codeText = pre.textContent;
      const button = document.createElement('button');
      button.className = 'copy-button';
      button.type = 'button';
      button.textContent = '复制';
      button.setAttribute('aria-label', '复制代码');
      button.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(codeText);
          button.textContent = '已复制';
        } catch (_) { button.textContent = '复制失败'; }
        setTimeout(() => { button.textContent = '复制'; }, 1600);
      });
      pre.append(button);
    });
  }
  const links = [...document.querySelectorAll('.toc-panel a')];
  if ('IntersectionObserver' in window && links.length) {
    const headings = links.map(link => document.getElementById(decodeURIComponent(link.hash.slice(1)))).filter(Boolean);
    const observer = new IntersectionObserver(entries => {
      const visible = entries.find(entry => entry.isIntersecting);
      if (!visible) return;
      links.forEach(link => link.classList.toggle('active', decodeURIComponent(link.hash.slice(1)) === visible.target.id));
    }, { rootMargin: '-100px 0px -65% 0px' });
    headings.forEach(heading => observer.observe(heading));
  }
})();
