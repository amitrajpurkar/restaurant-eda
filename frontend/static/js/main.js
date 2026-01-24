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

  void loadRestaurantTypes();
  void loadTopRestaurants();
});
