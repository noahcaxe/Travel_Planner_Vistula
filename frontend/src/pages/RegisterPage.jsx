import { useState } from 'react';
import { useAuth, useToast } from '../app.jsx';
import { register as apiRegister, login as apiLogin } from '../api.js';

export default function RegisterPage() {
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const toast = useToast();

  function set(k) { return e => setForm(f => ({ ...f, [k]: e.target.value })); }

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await apiRegister(form.username, form.email, form.password);
      const data = await apiLogin(form.email, form.password);
      login(data.access_token, data.refresh_token);
      toast('Account created! Let\'s explore 🌍', 'success');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-bg">
      <div className="auth-illustration">
        <div className="auth-illustration-title">
          Your journeys,<br /><em>organised.</em>
        </div>
        <p className="auth-illustration-sub">Create an account to start planning your travels.</p>
      </div>
      <div className="auth-form-panel">
        <div className="auth-form-box">
          <div className="auth-logo">🗺️ Travel Planner</div>
          <h1 className="auth-heading">Create account</h1>
          <p className="auth-sub">Start exploring the world.</p>

          {error && <div className="error-msg">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="field">
              <label>Username</label>
              <input
                value={form.username}
                onChange={set('username')}
                placeholder="explorer42"
                required
                autoFocus
              />
            </div>
            <div className="field">
              <label>Email</label>
              <input
                type="email"
                value={form.email}
                onChange={set('email')}
                placeholder="you@example.com"
                required
              />
            </div>
            <div className="field">
              <label>Password</label>
              <input
                type="password"
                value={form.password}
                onChange={set('password')}
                placeholder="••••••••"
                required
              />
            </div>
            <button className="btn btn-primary" type="submit" disabled={loading}>
              {loading ? 'Creating…' : 'Create account →'}
            </button>
          </form>

          <div className="auth-switch">
            Already have an account?{' '}
            <button onClick={() => window.location.href = '/login'}>Sign in</button>
          </div>
        </div>
      </div>
    </div>
  );
}