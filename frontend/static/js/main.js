/* ===== Home Page: Search ===== */

async function handleSearch() {
  const queryEl = document.getElementById('search-query');
  const modeEl = document.getElementById('search-mode');
  const resultsContainer = document.getElementById('search-results');
  const resultsGrid = document.getElementById('search-results-grid');
  const noResults = document.getElementById('search-no-results');
  const errorEl = document.getElementById('search-error');

  if (!queryEl || !modeEl || !resultsContainer) return;

  const q = queryEl.value.trim();
  if (!q) {
    clearSearch();
    return;
  }

  resultsContainer.style.display = 'block';
  resultsGrid.innerHTML = '';
  noResults.style.display = 'none';
  errorEl.style.display = 'none';

  try {
    const res = await fetch(`/api/search?q=${encodeURIComponent(q)}&mode=${modeEl.value}`);
    const body = await res.json();

    if (!res.ok || !body.success) {
      throw new Error(body && body.error ? body.error : `Request failed (${res.status})`);
    }

    const items = body.data.results;
    const mode = body.data.mode;

    if (items.length === 0) {
      noResults.style.display = 'block';
      return;
    }

    document.getElementById('search-results-title').textContent =
      `Search Results (${body.data.total_matches} match${body.data.total_matches !== 1 ? 'es' : ''})`;

    for (const item of items) {
      const col = document.createElement('div');
      col.className = 'col-12 col-sm-6 col-lg-4';
      col.innerHTML = renderSearchResult(item, mode);
      resultsGrid.appendChild(col);
    }
  } catch (err) {
    errorEl.textContent = err instanceof Error ? err.message : String(err);
    errorEl.style.display = 'block';
  }
}

function renderSearchResult(item, mode) {
  if (mode === 'name') {
    const rating = item.rating == null ? 'N/A' : item.rating.toFixed(2);
    return `
      <div class="card search-result-card h-100">
        <div class="card-body">
          <h6 class="card-title">${item.name}</h6>
          <div class="text-muted small">
            <div>${item.location} &middot; ${item.restaurant_type}</div>
            <div>Rating: ${rating} &middot; ${item.votes.toLocaleString()} votes</div>
          </div>
        </div>
      </div>`;
  } else if (mode === 'type') {
    const avg = item.avg_rating == null ? 'N/A' : item.avg_rating.toFixed(2);
    return `
      <div class="card search-result-card h-100">
        <div class="card-body">
          <h6 class="card-title">${item.restaurant_type}</h6>
          <div class="text-muted small">
            <div>${item.count} restaurants</div>
            <div>Avg rating: ${avg}</div>
          </div>
        </div>
      </div>`;
  } else {
    const avg = item.avg_rating == null ? 'N/A' : item.avg_rating.toFixed(2);
    return `
      <div class="card search-result-card h-100">
        <div class="card-body">
          <h6 class="card-title">${item.area}</h6>
          <div class="text-muted small">
            <div>${item.restaurant_count} restaurants</div>
            <div>Avg rating: ${avg}</div>
          </div>
        </div>
      </div>`;
  }
}

function clearSearch() {
  const queryEl = document.getElementById('search-query');
  const resultsContainer = document.getElementById('search-results');
  if (queryEl) queryEl.value = '';
  if (resultsContainer) resultsContainer.style.display = 'none';
}

/* ===== Drill-down Pages ===== */

async function loadDrilldownChart(chartType) {
  const container = document.getElementById('chart-container');
  const errorEl = document.getElementById('chart-error');
  const loadingEl = document.getElementById('chart-loading');

  if (!container) return;
  if (loadingEl) loadingEl.style.display = 'block';
  if (errorEl) errorEl.style.display = 'none';

  try {
    const res = await fetch(`/api/charts/${chartType}?width=900&height=420`);
    const body = await res.json();

    if (!res.ok || !body.success) {
      throw new Error(body && body.error ? body.error : `Request failed (${res.status})`);
    }

    const imgEl = document.getElementById('chart-image');
    if (imgEl) {
      imgEl.src = `data:image/png;base64,${body.data.base64_image}`;
      imgEl.alt = body.data.title || chartType;
      imgEl.style.display = 'block';
    }
  } catch (err) {
    if (errorEl) {
      errorEl.textContent = `Chart failed to load: ${err instanceof Error ? err.message : String(err)}`;
      errorEl.style.display = 'block';
    }
  } finally {
    if (loadingEl) loadingEl.style.display = 'none';
  }
}

async function loadDrilldownItems(apiEndpoint, renderFn) {
  const grid = document.getElementById('items-grid');
  const errorEl = document.getElementById('items-error');
  const loadingEl = document.getElementById('items-loading');

  if (!grid) return;
  if (loadingEl) loadingEl.style.display = 'block';
  if (errorEl) errorEl.style.display = 'none';
  grid.innerHTML = '';

  try {
    const res = await fetch(apiEndpoint);
    const body = await res.json();

    if (!res.ok || !body.success) {
      throw new Error(body && body.error ? body.error : `Request failed (${res.status})`);
    }

    renderFn(body.data, grid);
  } catch (err) {
    if (errorEl) {
      errorEl.textContent = err instanceof Error ? err.message : String(err);
      errorEl.style.display = 'block';
    }
  } finally {
    if (loadingEl) loadingEl.style.display = 'none';
  }
}

function renderTopRestaurants(data, grid) {
  const items = data.top_restaurants || [];
  for (const item of items) {
    const col = document.createElement('div');
    col.className = 'col-12 col-lg-6';
    const rating = item.rating == null ? 'N/A' : item.rating.toFixed(2);
    const cuisines = Array.isArray(item.cuisines) ? item.cuisines.join(', ') : '';
    col.innerHTML = `
      <div class="card drilldown-item-card h-100">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start">
            <h6 class="mb-1">#${item.rank} ${item.name}</h6>
            <span class="badge text-bg-dark">${item.votes.toLocaleString()} votes</span>
          </div>
          <div class="text-muted small mt-1">
            <div>${item.location} &middot; ${item.restaurant_type}</div>
            <div>Rating: ${rating}</div>
            <div>Cuisines: ${cuisines}</div>
          </div>
        </div>
      </div>`;
    grid.appendChild(col);
  }
}

function renderFoodieAreas(data, grid) {
  const items = data.foodie_areas || [];
  for (const item of items) {
    const col = document.createElement('div');
    col.className = 'col-12 col-lg-6';
    const rating = item.avg_rating == null ? 'N/A' : item.avg_rating.toFixed(2);
    const cuisines = Array.isArray(item.top_cuisines) ? item.top_cuisines.join(', ') : '';
    const types = Array.isArray(item.restaurant_types) ? item.restaurant_types.join(', ') : '';
    col.innerHTML = `
      <div class="card drilldown-item-card h-100">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start">
            <h6 class="mb-1">${item.area}</h6>
            <span class="badge text-bg-secondary">${item.restaurant_count} restaurants</span>
          </div>
          <div class="text-muted small mt-1">
            <div>Avg rating: ${rating}</div>
            <div>Top cuisines: ${cuisines}</div>
            <div>Types: ${types}</div>
          </div>
        </div>
      </div>`;
    grid.appendChild(col);
  }
}

function renderRestaurantTypes(data, grid) {
  const items = data.restaurant_types || [];
  for (const item of items) {
    const col = document.createElement('div');
    col.className = 'col-12 col-sm-6 col-lg-4';
    const avgRating = item.avg_rating == null ? 'N/A' : item.avg_rating.toFixed(2);
    const avgCost = item.avg_cost_for_two == null ? 'N/A' : item.avg_cost_for_two;
    col.innerHTML = `
      <div class="card drilldown-item-card h-100">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start">
            <h6 class="mb-1">${item.restaurant_type}</h6>
            <span class="badge text-bg-primary">${item.percentage.toFixed(1)}%</span>
          </div>
          <div class="display-6 fw-semibold">${item.count.toLocaleString()}</div>
          <div class="text-muted small mt-1">
            <div>Avg rating: ${avgRating}</div>
            <div>Avg cost for two: ${avgCost}</div>
          </div>
        </div>
      </div>`;
    grid.appendChild(col);
  }
}

/* ===== Page Initialization ===== */

document.addEventListener('DOMContentLoaded', () => {
  // Home page: search form
  const searchForm = document.getElementById('search-form');
  if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      void handleSearch();
    });
  }
  const searchBtn = document.getElementById('search-btn');
  if (searchBtn) {
    searchBtn.addEventListener('click', () => {
      void handleSearch();
    });
  }
  const clearBtn = document.getElementById('clear-search-btn');
  if (clearBtn) {
    clearBtn.addEventListener('click', clearSearch);
  }

  // Drill-down: Top Restaurants
  const restaurantsPage = document.getElementById('drilldown-restaurants');
  if (restaurantsPage) {
    void loadDrilldownChart('top-restaurants-bar');
    void loadDrilldownItems('/api/top-restaurants', renderTopRestaurants);
  }

  // Drill-down: Top Foodie Areas
  const foodieAreasPage = document.getElementById('drilldown-foodie-areas');
  if (foodieAreasPage) {
    void loadDrilldownChart('foodie-areas-bar');
    void loadDrilldownItems('/api/foodie-areas', renderFoodieAreas);
  }

  // Drill-down: Top Restaurant Types
  const typesPage = document.getElementById('drilldown-restaurant-types');
  if (typesPage) {
    void loadDrilldownChart('restaurant-types-pie');
    void loadDrilldownItems('/api/restaurant-types', renderRestaurantTypes);
  }
});
