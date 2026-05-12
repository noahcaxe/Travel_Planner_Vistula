import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import { getProjects, getPlaces, addPlace, deletePlace, updatePlace, logout as apiLogout } from '../api.js';
import { useAuth, useToast } from '../App.jsx';
import PlaceSearch from '../components/PlaceSearch.jsx';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

function createNumberedIcon(n, visited) {
  const color = visited ? '#4caf50' : 'var(--terra, #c4622d)';
  return L.divIcon({
    className: '',
    html: `<div style="
      width:32px;height:32px;border-radius:50% 50% 50% 0;
      background:${color};transform:rotate(-45deg);
      display:flex;align-items:center;justify-content:center;
      box-shadow:0 2px 8px rgba(0,0,0,0.3);
    "><span style="transform:rotate(45deg);color:#fff;font-size:12px;font-weight:600">${n}</span></div>`,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -36],
  });
}

function FlyTo({ center }) {
  const map = useMap();
  useEffect(() => {
    if (center) map.flyTo(center, 13, { duration: 1.2 });
  }, [center, map]);
  return null;
}

function AddPlaceModal({ projectId, onClose, onAdded }) {
  const [selected, setSelected] = useState(null);
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  async function handleAdd() {
    if (!selected) return;
    setLoading(true);
    try {
      await addPlace(projectId, {
        name: selected.name,
        address: selected.address,
        latitude: selected.latitude,
        longitude: selected.longitude,
        notes,
      });
      toast('Place added 📍', 'success');
      onAdded();
      onClose();
    } catch (err) {
      toast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <div className="modal-header">
          <h2 className="modal-title">Add a place</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          <PlaceSearch onSelect={setSelected} />

          {selected && (
            <div style={{
              marginTop: 14,
              padding: '12px 14px',
              background: 'var(--terra-dim)',
              borderRadius: 'var(--radius-sm)',
              border: '1px solid rgba(196,98,45,0.2)'
            }}>
              <div style={{ fontWeight: 500, fontSize: '0.9rem' }}>{selected.name}</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--ink-soft)', marginTop: 2 }}>{selected.address}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--terra)', marginTop: 4 }}>
                {selected.latitude.toFixed(4)}, {selected.longitude.toFixed(4)}
              </div>
            </div>
          )}

          <div className="field" style={{ marginTop: 14 }}>
            <label>Notes (optional)</label>
            <textarea
              value={notes}
              onChange={e => setNotes(e.target.value)}
              placeholder="Opening hours, tips, things to do…"
              rows={2}
              style={{ resize: 'vertical' }}
            />
          </div>

          <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
            <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
            <button
              className="btn btn-primary"
              style={{ width: 'auto' }}
              disabled={!selected || loading}
              onClick={handleAdd}
            >
              {loading ? 'Adding…' : '+ Add place'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ProjectDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const toast = useToast();

  const [project, setProject] = useState(null);
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [flyTo, setFlyTo] = useState(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [activePlace, setActivePlace] = useState(null);

  async function load() {
    try {
      const [projs, plcs] = await Promise.all([getProjects(), getPlaces(id)]);
      setProject(projs.find(p => String(p.id) === String(id)));
      setPlaces(plcs);
    } catch (err) {
      toast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, [id]);

  async function handleDelete(placeId) {
    if (!confirm('Remove this place?')) return;
    try {
      await deletePlace(id, placeId);
      setPlaces(ps => ps.filter(p => p.id !== placeId));
      toast('Place removed', 'success');
    } catch (err) {
      toast(err.message, 'error');
    }
  }

  async function handleToggleVisited(e, place) {
    e.stopPropagation();
    try {
      const updated = await updatePlace(id, place.id, { visited: !place.visited });
      setPlaces(ps => ps.map(p => p.id === place.id ? updated : p));
    } catch (err) {
      toast(err.message, 'error');
    }
  }

  function handlePlaceClick(place) {
    setActivePlace(place.id);
    if (place.latitude && place.longitude) {
      setFlyTo([place.latitude, place.longitude]);
    }
  }

  async function handleLogout() {
    try { await apiLogout(); } catch {}
    logout();
  }

  const defaultCenter = places.find(p => p.latitude)
    ? [places.find(p => p.latitude).latitude, places.find(p => p.latitude).longitude]
    : [48.8566, 2.3522];

  if (loading) return (
    <div className="app-layout">
      <div className="spinner" />
    </div>
  );

  const visitedCount = places.filter(p => p.visited).length;

  return (
    <div className="app-layout">
      <header className="topbar">
        <div className="topbar-logo">🗺️ Travel Planner</div>
        <div className="topbar-actions">
          <button className="btn btn-ghost btn-sm" onClick={handleLogout}>Sign out</button>
        </div>
      </header>

      <main className="main-content">
        <div className="breadcrumb">
          <button onClick={() => navigate('/')}>← All projects</button>
          <span className="breadcrumb-sep">/</span>
          <span>{project?.name || 'Project'}</span>
        </div>

        <div className="page-header" style={{ marginBottom: 24 }}>
          <div>
            <h1 className="page-title">
              {project?.name}
              {project?.description && <span>{project.description}</span>}
            </h1>
          </div>
          <button
            className="btn btn-primary"
            style={{ width: 'auto' }}
            disabled={places.length >= 10}
            onClick={() => setShowAddModal(true)}
            title={places.length >= 10 ? 'Max 10 places per project' : ''}
          >
            + Add place
          </button>
        </div>

        <div className="detail-layout">
          {/* MAP */}
          <div className="map-container">
            <MapContainer
              center={defaultCenter}
              zoom={places.length > 0 ? 10 : 4}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                attribution='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              {flyTo && <FlyTo center={flyTo} />}
              {places.map((place, i) => place.latitude && (
                <Marker
                  key={place.id}
                  position={[place.latitude, place.longitude]}
                  icon={createNumberedIcon(i + 1, place.visited)}
                  eventHandlers={{ click: () => setActivePlace(place.id) }}
                >
                  <Popup>
                    <strong>{place.name}</strong>
                    {place.visited && <> ✅</>}
                    {place.address && <><br /><small>{place.address}</small></>}
                    {place.notes && <><br /><em style={{ fontSize: '0.8rem' }}>{place.notes}</em></>}
                  </Popup>
                </Marker>
              ))}
            </MapContainer>
          </div>

          {/* PLACES PANEL */}
          <div className="places-panel">
            <div className="places-panel-header">
              <div className="places-panel-title">Places</div>
              <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                {places.length > 0 && (
                  <span className="badge" style={{ background: 'var(--teal)', color: '#fff', fontSize: '0.72rem' }}>
                    ✅ {visitedCount} / {places.length} visited
                  </span>
                )}
                <span className="badge badge-terra">{places.length} / 10</span>
              </div>
            </div>

            {places.length === 0 ? (
              <div style={{ padding: '40px 20px', textAlign: 'center', color: 'var(--ink-soft)' }}>
                <div style={{ fontSize: '2.5rem', marginBottom: 12 }}>📍</div>
                <div style={{ fontSize: '0.9rem' }}>No places yet. Add your first spot!</div>
              </div>
            ) : (
              <div className="places-list">
                {places.map((place, i) => (
                  <div
                    key={place.id}
                    className="place-item"
                    style={activePlace === place.id ? { background: 'var(--terra-dim)' } : {}}
                    onClick={() => handlePlaceClick(place)}
                  >
                    <div className="place-item-num">{i + 1}</div>
                    <div className="place-item-info">
                      <div
                        className="place-item-name"
                        style={place.visited ? { textDecoration: 'line-through', opacity: 0.55 } : {}}
                      >
                        {place.name}
                      </div>
                      {place.address && (
                        <div
                          className="place-item-addr"
                          style={place.visited ? { opacity: 0.45 } : {}}
                        >
                          {place.address}
                        </div>
                      )}
                      {place.notes && (
                        <div style={{ fontSize: '0.75rem', color: 'var(--teal)', marginTop: 4, fontStyle: 'italic' }}>
                          {place.notes}
                        </div>
                      )}
                    </div>
                    <div className="place-item-actions">
                      <button
                        className="btn btn-ghost btn-icon"
                        style={{ fontSize: '0.9rem', opacity: place.visited ? 1 : 0.35 }}
                        onClick={e => handleToggleVisited(e, place)}
                        title={place.visited ? 'Mark as not visited' : 'Mark as visited'}
                      >✅</button>
                      <button
                        className="btn btn-ghost btn-icon"
                        style={{ fontSize: '0.9rem' }}
                        onClick={e => { e.stopPropagation(); handleDelete(place.id); }}
                        title="Remove"
                      >🗑️</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>

      {showAddModal && (
        <AddPlaceModal
          projectId={id}
          onClose={() => setShowAddModal(false)}
          onAdded={load}
        />
      )}
    </div>
  );
}