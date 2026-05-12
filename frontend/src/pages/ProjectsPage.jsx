import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, useToast } from '../App.jsx';
import { getProjects, createProject, deleteProject, updateProject, logout as apiLogout } from '../api.js';

function ProjectModal({ project, onClose, onSaved }) {
  const [form, setForm] = useState({
    name: project?.name || '',
    description: project?.description || '',
    cover_url: project?.cover_url || '',
    start_date: project?.start_date || '',
  });
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState(project?.cover_url || '');
  const toast = useToast();
  const isEdit = !!project;

  function handleUrlChange(e) {
    const val = e.target.value;
    setForm(f => ({ ...f, cover_url: val }));
    setPreview(val);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        name: form.name,
        description: form.description || null,
        cover_url: form.cover_url || null,
        start_date: form.start_date || null,
      };
      if (isEdit) {
        await updateProject(project.id, payload);
        toast('Project updated ✓', 'success');
      } else {
        await createProject(payload);
        toast('Project created! ✈️', 'success');
      }
      onSaved();
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
          <h2 className="modal-title">{isEdit ? 'Edit project' : 'New project'}</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        <div className="modal-body">
          <form onSubmit={handleSubmit}>
            <div className="field">
              <label>Project name</label>
              <input
                value={form.name}
                onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
                placeholder="e.g. Summer in Japan"
                required
                autoFocus
              />
            </div>
            <div className="field">
              <label>Description (optional)</label>
              <textarea
                value={form.description}
                onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
                placeholder="What's this trip about?"
                rows={3}
                style={{ resize: 'vertical' }}
              />
            </div>
            <div className="field">
              <label>Start date (optional)</label>
              <input
                type="date"
                value={form.start_date}
                onChange={e => setForm(f => ({ ...f, start_date: e.target.value }))}
              />
            </div>
            <div className="field">
              <label>Cover image URL (optional)</label>
              <input
                value={form.cover_url}
                onChange={handleUrlChange}
                placeholder="https://example.com/photo.jpg"
              />
            </div>

            {preview && (
              <div style={{ marginBottom: 16 }}>
                <img
                  src={preview}
                  alt="Cover preview"
                  style={{
                    width: '100%',
                    height: 140,
                    objectFit: 'cover',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--border)',
                  }}
                  onError={e => { e.target.style.display = 'none'; }}
                  onLoad={e => { e.target.style.display = 'block'; }}
                />
              </div>
            )}

            <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end', marginTop: 8 }}>
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
              <button type="submit" className="btn btn-primary" style={{ width: 'auto' }} disabled={loading}>
                {loading ? 'Saving…' : isEdit ? 'Save changes' : 'Create project'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

const EMOJIS = ['🗾', '🏔️', '🏖️', '🏛️', '🌿', '🏙️', '🌊', '🏜️', '🌸'];

function formatDate(dateStr) {
  if (!dateStr) return null;
  return new Date(dateStr).toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

export default function ProjectsPage() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState(null);
  const { logout } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  async function load() {
    try {
      const data = await getProjects();
      setProjects(data);
    } catch (err) {
      toast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  async function handleDelete(e, id) {
    e.stopPropagation();
    if (!confirm('Delete this project and all its places?')) return;
    try {
      await deleteProject(id);
      setProjects(ps => ps.filter(p => p.id !== id));
      toast('Project deleted', 'success');
    } catch (err) {
      toast(err.message, 'error');
    }
  }

  async function handleLogout() {
    try { await apiLogout(); } catch {}
    logout();
  }

  return (
    <div className="app-layout">
      <header className="topbar">
        <div className="topbar-logo">🗺️ Travel Planner</div>
        <div className="topbar-actions">
          <button className="btn btn-ghost btn-sm" onClick={handleLogout}>Sign out</button>
        </div>
      </header>

      <main className="main-content">
        <div className="page-header">
          <div>
            <h1 className="page-title">
              My Projects
              <span>{projects.length} {projects.length === 1 ? 'trip' : 'trips'} planned</span>
            </h1>
          </div>
          <button className="btn btn-primary" style={{ width: 'auto' }} onClick={() => setModal('create')}>
            + New project
          </button>
        </div>

        {loading ? (
          <div className="spinner" />
        ) : (
          <div className="projects-grid">
            {projects.length === 0 && (
              <div className="empty-state">
                <div className="empty-state-icon">✈️</div>
                <div className="empty-state-title">No trips yet</div>
                <p className="empty-state-sub">Create your first travel project to get started.</p>
              </div>
            )}
            {projects.map((p, i) => (
              <div key={p.id} className="project-card" onClick={() => navigate(`/projects/${p.id}`)}>
                <div className="project-card-map">
                  {p.cover_url ? (
                    <img
                      src={p.cover_url}
                      alt={p.name}
                      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                      onError={e => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                      }}
                    />
                  ) : null}
                  <div
                    className="project-card-map-placeholder"
                    style={{ display: p.cover_url ? 'none' : 'flex' }}
                  >
                    {EMOJIS[i % EMOJIS.length]}
                  </div>
                </div>
                <div className="project-card-body">
                  <div className="project-card-name">{p.name}</div>
                  {p.description && <div className="project-card-desc">{p.description}</div>}
                  <div className="project-card-meta">
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                      <div className="project-card-places">
                        📍 {p.places?.length ?? 0} / 10 places
                      </div>
                      {p.start_date && (
                        <div style={{ fontSize: '0.75rem', color: 'var(--ink-soft)' }}>
                          🗓️ {formatDate(p.start_date)}
                        </div>
                      )}
                    </div>
                    <div className="project-card-actions">
                      <button
                        className="btn btn-ghost btn-icon"
                        title="Edit"
                        onClick={e => { e.stopPropagation(); setModal(p); }}
                      >✏️</button>
                      <button
                        className="btn btn-ghost btn-icon"
                        title="Delete"
                        onClick={e => handleDelete(e, p.id)}
                      >🗑️</button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {modal && (
        <ProjectModal
          project={modal === 'create' ? null : modal}
          onClose={() => setModal(null)}
          onSaved={load}
        />
      )}
    </div>
  );
}