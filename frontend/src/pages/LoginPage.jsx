import { useState } from 'react';
import { useAuth, useToast } from '../App.jsx';
import { login as apiLogin } from '../api.js';

export default function LoginPage({ onSwitch }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const toast = useToast();


  const goRegister = onSwitch || (() => window.location.href = '/register');

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await apiLogin(email, password);
      login(data.access_token, data.refresh_token);
      toast('Welcome back! ✈️', 'success');
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
          Plan your next<br /><em>adventure.</em>
        </div>
        <p className="auth-illustration-sub">Save places, build itineraries, explore the world.</p>
      </div>
      <div className="auth-form-panel">
        <div className="auth-form-box">
          <div className="auth-logo">🗺️ Travel Planner</div>
          <h1 className="auth-heading">Sign in</h1>
          <p className="auth-sub">Welcome back, explorer.</p>

          {error && <div className="error-msg">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="field">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="you@example.com"
                required
                autoFocus
              />
            </div>
            <div className="field">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="••••••••"
                required
              />
            </div>
            <button className="btn btn-primary" type="submit" disabled={loading}>
              {loading ? 'Signing in…' : 'Sign in →'}
            </button>
          </form>

          <div className="auth-switch">
            Don't have an account?{' '}
            <button onClick={goRegister}>Create one</button>
          </div>
        </div>
      </div>
    </div>
  );
}