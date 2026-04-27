import { useState } from 'react';
import './styles/AuthPages.css';
import { authService } from './services/api';

function App() {
  const [mode, setMode] = useState('register');
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    first_name: '',
    last_name: '',
    password: '',
    password_confirm: '',
  });
  const [currentUser, setCurrentUser] = useState(() => {
    const saved = localStorage.getItem('auth_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    try {
      if (mode === 'register') {
        await authService.register(formData);
        setMessage('Registration successful. You can now log in.');
        setMode('login');
        setFormData((current) => ({
          ...current,
          password: '',
          password_confirm: '',
        }));
        return;
      }

      const response = await authService.login(formData.email, formData.password);
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);

      const profileResponse = await authService.getProfile(response.data.access);
      localStorage.setItem('auth_user', JSON.stringify(profileResponse.data));
      setCurrentUser(profileResponse.data);
      setMessage('Login successful.');
    } catch (err) {
      const data = err.response?.data;
      if (data && typeof data === 'object') {
        const firstKey = Object.keys(data)[0];
        const firstValue = data[firstKey];
        setError(Array.isArray(firstValue) ? firstValue[0] : firstValue || 'Registration failed');
      } else {
        setError(mode === 'register' ? 'Registration failed' : 'Login failed');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('auth_user');
    setCurrentUser(null);
    setMessage('Logged out.');
  };

  return (
    <div className="auth-page">
      <div className="auth-shell">
        <section className="auth-card">
          <p className="auth-kicker">CinemaHub</p>
          <h1>{mode === 'register' ? 'Create account' : 'Log in'}</h1>
          <p className="auth-subtitle">
            {mode === 'register'
              ? 'Register a new account and connect React to Django.'
              : 'Use your email and password to enter the app.'}
          </p>

          <div className="auth-switch">
            <button
              type="button"
              className={mode === 'register' ? 'auth-tab auth-tab--active' : 'auth-tab'}
              onClick={() => {
                setMode('register');
                setError('');
                setMessage('');
              }}
            >
              Register
            </button>
            <button
              type="button"
              className={mode === 'login' ? 'auth-tab auth-tab--active' : 'auth-tab'}
              onClick={() => {
                setMode('login');
                setError('');
                setMessage('');
              }}
            >
              Login
            </button>
          </div>

          {error ? <div className="auth-alert auth-alert--error">{error}</div> : null}
          {message ? <div className="auth-alert auth-alert--success">{message}</div> : null}

          {currentUser ? (
            <div className="auth-user">
              <div>
                <strong>{currentUser.username}</strong>
                <p>{currentUser.email}</p>
              </div>
              <button type="button" className="auth-ghost-button" onClick={handleLogout}>
                Logout
              </button>
            </div>
          ) : null}

          <form className="auth-form" onSubmit={handleSubmit}>
            <label>
              Email Address *
              <input type="email" name="email" value={formData.email} onChange={handleChange} required />
            </label>

            {mode === 'register' ? (
              <label>
                Username *
                <input type="text" name="username" value={formData.username} onChange={handleChange} required />
              </label>
            ) : null}

            {mode === 'register' ? (
              <div className="auth-grid">
                <label>
                  First Name
                  <input type="text" name="first_name" value={formData.first_name} onChange={handleChange} />
                </label>

                <label>
                  Last Name
                  <input type="text" name="last_name" value={formData.last_name} onChange={handleChange} />
                </label>
              </div>
            ) : null}

            <label>
              Password *
              <input type="password" name="password" value={formData.password} onChange={handleChange} minLength={8} required />
            </label>

            {mode === 'register' ? (
              <label>
                Confirm Password *
                <input type="password" name="password_confirm" value={formData.password_confirm} onChange={handleChange} minLength={8} required />
              </label>
            ) : null}

            <button className="auth-button" type="submit" disabled={loading}>
              {loading ? (mode === 'register' ? 'Creating account...' : 'Signing in...') : mode === 'register' ? 'Register' : 'Login'}
            </button>
          </form>
        </section>
      </div>
    </div>
  )
}

export default App
