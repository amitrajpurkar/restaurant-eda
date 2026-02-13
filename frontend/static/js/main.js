async function loadRestaurantTypes() {
  const loadingEl = document.getElementById('restaurant-types-loading');
  const errorEl = document.getElementById('restaurant-types-error');
  const gridEl = document.getElementById('restaurant-types-grid');

  if (!loadingEl || !errorEl || !gridEl) return;

  loadingEl.classList.remove('d-none');
  errorEl.classList.add('d-none');
  errorEl.textContent = '';
  gridEl.innerHTML = '';

  try {
    const res = await fetch('/api/restaurant-types');
    const body = await res.json();

    if (!res.ok || !body.success) {
      throw new Error(body && body.error ? body.error : `Request failed (${res.status})`);
    }

    const items = body.data.restaurant_types;
    for (const item of items) {
      const col = document.createElement('div');
      col.className = 'col-12 col-sm-6 col-lg-4 col-xl-3';

      const avgRating = item.avg_rating == null ? 'N/A' : item.avg_rating.toFixed(2);
      const avgCost = item.avg_cost_for_two == null ? 'N/A' : item.avg_cost_for_two;

      col.innerHTML = `
        <div class="card type-card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
              <h3 class="h6 mb-1">${item.restaurant_type}</h3>
              <span class="badge text-bg-primary">${item.percentage.toFixed(1)}%</span>
            </div>
            <div class="display-6 fw-semibold">${item.count.toLocaleString()}</div>
            <div class="meta mt-2">
              <div>Avg rating: <span class="fw-medium">${avgRating}</span></div>
              <div>Avg cost for two: <span class="fw-medium">${avgCost}</span></div>
            </div>
          </div>
        </div>
      `;

      gridEl.appendChild(col);
    }
  } catch (err) {
    errorEl.textContent = err instanceof Error ? err.message : String(err);
    errorEl.classList.remove('d-none');
  } finally {
    loadingEl.classList.add('d-none');
  }
}

async function loadFoodieAreas() {
  const loadingEl = document.getElementById('foodie-areas-loading');
  const errorEl = document.getElementById('foodie-areas-error');
  const gridEl = document.getElementById('foodie-areas-grid');

  if (!loadingEl || !errorEl || !gridEl) return;

  loadingEl.classList.remove('d-none');
  errorEl.classList.add('d-none');
  errorEl.textContent = '';
  gridEl.innerHTML = '';

  try {
    const res = await fetch('/api/foodie-areas');
    const body = await res.json();

    if (!res.ok || !body.success) {
      throw new Error(body && body.error ? body.error : `Request failed (${res.status})`);
    }

    const items = body.data.foodie_areas;
    for (const item of items) {
      const col = document.createElement('div');
      col.className = 'col-12 col-lg-6';

      const rating = item.avg_rating == null ? 'N/A' : item.avg_rating.toFixed(2);
      const cuisines = Array.isArray(item.top_cuisines) ? item.top_cuisines.join(', ') : '';
      const types = Array.isArray(item.restaurant_types) ? item.restaurant_types.join(', ') : '';

      col.innerHTML = `
        <div class="card foodie-area-card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
              <h3 class="h6 mb-1">${item.area}</h3>
              <span class="badge text-bg-secondary">${item.restaurant_count.toLocaleString()} restaurants</span>
            </div>
            <div class="meta mt-2">
              <div>Avg rating: <span class="fw-medium">${rating}</span></div>
              <div>Top cuisines: <span class="fw-medium">${cuisines}</span></div>
              <div>Top types: <span class="fw-medium">${types}</span></div>
            </div>
          </div>
        </div>
      `;

      gridEl.appendChild(col);
    }
  } catch (err) {
    errorEl.textContent = err instanceof Error ? err.message : String(err);
    errorEl.classList.remove('d-none');
  } finally {
    loadingEl.classList.add('d-none');
  }
}

async function loadTopRestaurants() {
  const loadingEl = document.getElementById('top-restaurants-loading');
  const errorEl = document.getElementById('top-restaurants-error');
  const gridEl = document.getElementById('top-restaurants-grid');

  if (!loadingEl || !errorEl || !gridEl) return;

  loadingEl.classList.remove('d-none');
  errorEl.classList.add('d-none');
  errorEl.textContent = '';
  gridEl.innerHTML = '';

  try {
    const res = await fetch('/api/top-restaurants');
    const body = await res.json();

    if (!res.ok || !body.success) {
      throw new Error(body && body.error ? body.error : `Request failed (${res.status})`);
    }

    const items = body.data.top_restaurants;
    for (const item of items) {
      const col = document.createElement('div');
      col.className = 'col-12 col-lg-6';

      const rating = item.rating == null ? 'N/A' : item.rating.toFixed(2);
      const cuisines = Array.isArray(item.cuisines) ? item.cuisines.join(', ') : '';

      col.innerHTML = `
        <div class="card top-restaurant-card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
              <h3 class="h6 mb-1">#${item.rank} ${item.name}</h3>
              <span class="badge text-bg-dark">${item.votes.toLocaleString()} votes</span>
            </div>
            <div class="meta mt-2">
              <div>Location: <span class="fw-medium">${item.location}</span></div>
              <div>Type: <span class="fw-medium">${item.restaurant_type}</span></div>
              <div>Rating: <span class="fw-medium">${rating}</span></div>
              <div>Cuisines: <span class="fw-medium">${cuisines}</span></div>
            </div>
          </div>
        </div>
      `;

      gridEl.appendChild(col);
    }
  } catch (err) {
    errorEl.textContent = err instanceof Error ? err.message : String(err);
    errorEl.classList.remove('d-none');
  } finally {
    loadingEl.classList.add('d-none');
  }
}

async function loadCharts() {
  const loadingEl = document.getElementById('charts-loading');
  const errorEl = document.getElementById('charts-error');
  const gridEl = document.getElementById('charts-grid');

  if (!loadingEl || !errorEl || !gridEl) return;

  loadingEl.classList.remove('d-none');
  errorEl.classList.add('d-none');
  errorEl.textContent = '';
  gridEl.innerHTML = '';

  const chartTypes = [
    { type: 'restaurant-types-pie' },
    { type: 'top-restaurants-bar' },
    { type: 'foodie-areas-bar' },
  ];

  try {
    for (const chart of chartTypes) {
      const res = await fetch(`/api/charts/${chart.type}?width=900&height=420`);
      const body = await res.json();

      if (!res.ok || !body.success) {
        throw new Error(body && body.error ? body.error : `Request failed (${res.status})`);
      }

      const item = body.data;
      const col = document.createElement('div');
      col.className = 'col-12 col-xl-6';

      const title = item.title || item.chart_type;
      const src = `data:image/png;base64,${item.base64_image}`;

      col.innerHTML = `
        <div class="card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start">
              <h3 class="h6 mb-2">${title}</h3>
              <span class="badge text-bg-light">${item.width}×${item.height}</span>
            </div>
            <img class="img-fluid border rounded" alt="${title}" src="${src}" />
          </div>
        </div>
      `;

      gridEl.appendChild(col);
    }
  } catch (err) {
    errorEl.textContent = err instanceof Error ? err.message : String(err);
    errorEl.classList.remove('d-none');
  } finally {
    loadingEl.classList.add('d-none');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const refreshBtn = document.getElementById('refresh-btn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      void loadRestaurantTypes();
    });
  }

  const topRefreshBtn = document.getElementById('top-restaurants-refresh-btn');
  if (topRefreshBtn) {
    topRefreshBtn.addEventListener('click', () => {
      void loadTopRestaurants();
    });
  }

  const foodieAreasRefreshBtn = document.getElementById('foodie-areas-refresh-btn');
  if (foodieAreasRefreshBtn) {
    foodieAreasRefreshBtn.addEventListener('click', () => {
      void loadFoodieAreas();
    });
  }

  const chartsRefreshBtn = document.getElementById('charts-refresh-btn');
  if (chartsRefreshBtn) {
    chartsRefreshBtn.addEventListener('click', () => {
      void loadCharts();
    });
  }

  void loadRestaurantTypes();
  void loadTopRestaurants();
  void loadFoodieAreas();
  void loadCharts();
});
