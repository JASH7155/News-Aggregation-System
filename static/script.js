// static/script.js (updated: lazy images, timeAgo, load more)
document.addEventListener('DOMContentLoaded', () => {
  const search = document.getElementById('searchInput');
  const select = document.getElementById('categorySelect');
  const refreshBtn = document.getElementById('refreshBtn');
  const container = document.getElementById('newsContainer');
  const loadMoreBtn = document.getElementById('loadMoreBtn');

  let currentLimit = 20; // initial number shown
  const PAGE_SIZE = 20; // how many to add on "load more"

  function timeAgo(iso) {
    if (!iso) return '';
    const d = new Date(iso);
    const diff = (Date.now() - d.getTime()) / 1000;
    if (diff < 60) return `${Math.floor(diff)}s ago`;
    if (diff < 3600) return `${Math.floor(diff/60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff/3600)}h ago`;
    return d.toLocaleDateString();
  }

  async function fetchLatest(limit=50, category='') {
    const params = new URLSearchParams();
    params.set('limit', limit);
    if (category) params.set('category', category);
    const res = await fetch(`/api/latest?${params.toString()}`);
    const data = await res.json();
    return data.articles || [];
  }

  function makeCard(article) {
    const a = document.createElement('article');
    a.className = 'card';
    a.dataset.title = article.title || '';
    a.dataset.desc = article.description || '';
    a.dataset.category = article.category || '';

    const img = document.createElement('img');
    img.loading = 'lazy';
    img.alt = article.title || '';
    img.src = article.image_url || '';

    const body = document.createElement('div');
    body.className = 'card-body';
    const title = document.createElement('div');
    title.className = 'title';
    title.textContent = article.title || 'No title';
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = `${article.source || ''} • ${timeAgo(article.published_at || '')}`;
    const desc = document.createElement('div');
    desc.className = 'desc';
    desc.textContent = article.description || '';
    const link = document.createElement('a');
    link.className = 'link';
    link.href = article.url || '#';
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = 'Read more';
    body.appendChild(title);
    body.appendChild(meta);
    body.appendChild(desc);
    body.appendChild(link);
    a.appendChild(img);
    a.appendChild(body);
    return a;
  }

  function renderArticles(list) {
    container.innerHTML = '';
    const toShow = list.slice(0, currentLimit);
    toShow.forEach(article => {
      const card = makeCard(article);
      container.appendChild(card);
    });
    filterCards(); // apply current filters
  }

  function filterCards() {
    const q = search.value.trim().toLowerCase();
    const cat = select.value;
    const cards = Array.from(container.querySelectorAll('.card'));
    cards.forEach(card => {
      const title = card.dataset.title.toLowerCase();
      const desc = card.dataset.desc ? card.dataset.desc.toLowerCase() : '';
      const category = card.dataset.category;
      const matchesQuery = q === '' || title.includes(q) || desc.includes(q);
      const matchesCategory = !cat || category === cat;
      card.style.display = (matchesQuery && matchesCategory) ? '' : 'none';
    });
  }

  async function loadAndRender() {
    const category = select.value || '';
    // fetch a larger set so load more works client-side
    const articles = await fetchLatest(200, category);
    window.__LATEST_ARTICLES = articles; // cache in memory for load more
    currentLimit = Math.min(20, articles.length);
    renderArticles(articles);
    // recommendations
    const recRes = await fetch(`/api/recommend?limit=6${category ? '&category='+encodeURIComponent(category) : ''}`);
    const rec = await recRes.json();
    showRecommendations(rec.recommendations || []);
    // show/hide load more button
    loadMoreBtn.style.display = (articles.length > currentLimit) ? '' : 'none';
  }

  function showRecommendations(recs) {
    let rc = document.getElementById('recommendContainer');
    if (!rc) {
      rc = document.createElement('aside');
      rc.id = 'recommendContainer';
      rc.style.width = '320px';
      rc.style.marginLeft = '16px';
      document.querySelector('main').insertBefore(rc, document.querySelector('main').firstChild);
    }
    rc.innerHTML = '<h3>Recommended</h3>';
    recs.forEach(a => {
      const c = document.createElement('div');
      c.className = 'rec-card';
      const img = document.createElement('img');
      img.src = a.image_url || '';
      img.loading = 'lazy';
      const link = document.createElement('a');
      link.href = a.url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = (a.title || '').slice(0, 80);
      const meta = document.createElement('div');
      meta.className = 'rec-meta';
      meta.textContent = `${a.source || ''} • ${timeAgo(a.published_at || '')}`;
      c.appendChild(img);
      const text = document.createElement('div');
      text.appendChild(link);
      text.appendChild(meta);
      c.appendChild(text);
      rc.appendChild(c);
    });
  }

  // events
  search.addEventListener('input', filterCards);
  select.addEventListener('change', () => loadAndRender());

  loadMoreBtn.addEventListener('click', () => {
    const all = window.__LATEST_ARTICLES || [];
    currentLimit = Math.min((currentLimit || 20) + PAGE_SIZE, all.length);
    renderArticles(all);
    loadMoreBtn.style.display = (all.length > currentLimit) ? '' : 'none';
  });

  refreshBtn.addEventListener('click', async () => {
    refreshBtn.disabled = true;
    refreshBtn.textContent = 'Refreshing...';
    await fetch('/api/refresh', { method: 'POST' });
    setTimeout(async () => {
      await loadAndRender();
      refreshBtn.disabled = false;
      refreshBtn.textContent = 'Refresh (regen)';
    }, 4000);
  });

  // initial load
  loadAndRender();
});
