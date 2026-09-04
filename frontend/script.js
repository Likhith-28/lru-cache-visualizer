const API_BASE = window.location.origin;

const capacityInput = document.getElementById("capacity");
const keyInput = document.getElementById("key-input");
const valueInput = document.getElementById("value-input");
const cacheList = document.getElementById("cache-list");
const historyList = document.getElementById("history-list");

const statCapacity = document.getElementById("stat-capacity");
const statSize = document.getElementById("stat-size");
const statHits = document.getElementById("stat-hits");
const statMisses = document.getElementById("stat-misses");
const statEvictions = document.getElementById("stat-evictions");
const statHitRate = document.getElementById("stat-hit-rate");

let history = [];

async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(payload.detail || "Request failed");
  }

  return payload;
}

function addHistory(message, type = "info") {
  history.unshift({ message, type });
  history = history.slice(0, 8);
  renderHistory();
}

function renderHistory() {
  historyList.innerHTML = "";

  for (const item of history) {
    const li = document.createElement("li");
    li.className = item.type;
    li.textContent = item.message;
    historyList.appendChild(li);
  }
}

function renderState(state) {
  statCapacity.textContent = state.capacity;
  statSize.textContent = state.size;
  statHits.textContent = state.hits;
  statMisses.textContent = state.misses;
  statEvictions.textContent = state.evictions;
  statHitRate.textContent = `${state.hit_rate}%`;

  cacheList.innerHTML = "";

  if (!state.items || state.items.length === 0) {
    const empty = document.createElement("div");
    empty.className = "cache-item empty";
    empty.textContent = "Empty cache";
    cacheList.appendChild(empty);
    return;
  }

  for (const item of state.items) {
    const node = document.createElement("div");
    node.className = "cache-item";
    node.innerHTML = `
      <span class="tag">LRU → MRU</span>
      <span class="key">${item.key}</span>
      <span class="value">${item.value}</span>
    `;
    cacheList.appendChild(node);
  }
}

async function refreshState() {
  try {
    const state = await apiRequest("/cache/state");
    renderState(state);
  } catch (error) {
    addHistory(`State error: ${error.message}`, "miss");
  }
}

async function handlePut() {
  const key = keyInput.value.trim();
  const value = valueInput.value.trim();

  if (!key) {
    addHistory("PUT requires a key", "miss");
    return;
  }

  try {
    const capacity = Number(capacityInput.value) || 5;
    const state = await apiRequest("/cache/put", {
      method: "POST",
      body: JSON.stringify({ key, value, capacity }),
    });
    addHistory(`PUT ${key} = ${value} (cap=${capacity})`, "info");
    renderState(state);
    keyInput.value = "";
    valueInput.value = "";
  } catch (error) {
    addHistory(`PUT failed: ${error.message}`, "miss");
  }
}

async function handleGet() {
  const key = keyInput.value.trim();

  if (!key) {
    addHistory("GET requires a key", "miss");
    return;
  }

  try {
    const result = await apiRequest(`/cache/get/${encodeURIComponent(key)}`);
    const label = result.hit ? "HIT" : "MISS";
    addHistory(`${label}: ${key}`, result.hit ? "hit" : "miss");
    await refreshState();
    keyInput.value = "";
  } catch (error) {
    addHistory(`GET failed: ${error.message}`, "miss");
  }
}

async function handleReset() {
  try {
    const capacity = Number(capacityInput.value) || 5;
    const state = await apiRequest("/cache/reset", {
      method: "POST",
      body: JSON.stringify({ capacity }),
    });
    addHistory(`RESET cache (capacity=${capacity})`, "info");
    renderState(state);
  } catch (error) {
    addHistory(`RESET failed: ${error.message}`, "miss");
  }
}

document.getElementById("put-btn").addEventListener("click", handlePut);
document.getElementById("get-btn").addEventListener("click", handleGet);
document.getElementById("reset-btn").addEventListener("click", handleReset);

refreshState();
