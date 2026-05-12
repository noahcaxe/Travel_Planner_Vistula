const BASE = '/api';

function getToken() {
  return localStorage.getItem('access_token');
}

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${getToken()}`,
  };
}

async function handle(res) {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Request failed');
  }
  if (res.status === 204) return null;
  return res.json();
}


export async function register(username, email, password) {
  return handle(await fetch(`${BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password }),
  }));
}

export async function login(email, password) {
  return handle(await fetch(`${BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  }));
}

export async function logout() {
  return handle(await fetch(`${BASE}/auth/logout`, {
    method: 'POST',
    headers: authHeaders(),
  }));
}

export async function refreshToken() {
  const refresh_token = localStorage.getItem('refresh_token');
  return handle(await fetch(`${BASE}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token }),
  }));
}


export async function getProjects() {
  return handle(await fetch(`${BASE}/projects`, { headers: authHeaders() }));
}

export async function createProject(data) {
  return handle(await fetch(`${BASE}/projects`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(data),
  }));
}

export async function updateProject(id, data) {
  return handle(await fetch(`${BASE}/projects/${id}`, {
    method: 'PATCH',
    headers: authHeaders(),
    body: JSON.stringify(data),
  }));
}

export async function deleteProject(id) {
  return handle(await fetch(`${BASE}/projects/${id}`, {
    method: 'DELETE',
    headers: authHeaders(),
  }));
}


export async function getPlaces(projectId) {
  return handle(await fetch(`${BASE}/projects/${projectId}/places`, { headers: authHeaders() }));
}

export async function addPlace(projectId, data) {
  return handle(await fetch(`${BASE}/projects/${projectId}/places`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(data),
  }));
}

export async function updatePlace(projectId, placeId, data) {
  return handle(await fetch(`${BASE}/projects/${projectId}/places/${placeId}`, {
    method: 'PATCH',
    headers: authHeaders(),
    body: JSON.stringify(data),
  }));
}

export async function deletePlace(projectId, placeId) {
  return handle(await fetch(`${BASE}/projects/${projectId}/places/${placeId}`, {
    method: 'DELETE',
    headers: authHeaders(),
  }));
}


export async function searchPlaces(query) {
  const res = await fetch(
    `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=6&addressdetails=1`,
    { headers: { 'Accept-Language': 'en' } }
  );
  return res.json();
}