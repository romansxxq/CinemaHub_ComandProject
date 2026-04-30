import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import '../styles/AuthPages.css';

function RegisterPage() {
  const navigate = useNavigate();
  const { register, error } = useAuth();
  const toast = useToast();

  const [formData, setFormData] = useState({
    email: '',
    username: '',
    firstName: '',
    lastName: '',
    password: '',
    passwordConfirm: '',
  });
  const [loading, setLoading] = useState(false);
  const [localError, setLocalError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLocalError('');

    // Validation
    if (!formData.email || !formData.username || !formData.password || !formData.passwordConfirm) {
      const msg = 'Будь ласка, заповніть всі необхідні поля';
      setLocalError(msg);
      toast.warning(msg);
      return;
    }

    if (formData.password.length < 8) {
      const msg = 'Пароль повинен містити мінімум 8 символів';
      setLocalError(msg);
      toast.warning(msg);
      return;
    }

    if (formData.password !== formData.passwordConfirm) {
      const msg = 'Паролі не збігаються';
      setLocalError(msg);
      toast.warning(msg);
      return;
    }

    setLoading(true);
    const success = await register(
      formData.email,
      formData.username,
      formData.password,
      formData.passwordConfirm,
      formData.firstName,
      formData.lastName
    );
    setLoading(false);

    if (success) {
      toast.success('Реєстрація успішна! Тепер увійдіть до свого облікового запису.');
      navigate('/login');
    } else {
      const msg = error || 'Помилка реєстрації. Спробуйте ще раз.';
      setLocalError(msg);
      toast.error(msg);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-container">
        <div className="auth-card">
          <h1>🎬 CinemaHub</h1>
          <h2>Register</h2>

          {localError && <div className="error-message">{localError}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email">Email Address *</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="your@email.com"
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="username">Username *</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="username"
                disabled={loading}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="firstName">First Name</label>
                <input
                  type="text"
                  id="firstName"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleChange}
                  placeholder="John"
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="lastName">Last Name</label>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleChange}
                  placeholder="Doe"
                  disabled={loading}
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="password">Password * (min. 8 characters)</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                disabled={loading}
                required
                minLength="8"
              />
            </div>

            <div className="form-group">
              <label htmlFor="passwordConfirm">Confirm Password *</label>
              <input
                type="password"
                id="passwordConfirm"
                name="passwordConfirm"
                value={formData.passwordConfirm}
                onChange={handleChange}
                placeholder="••••••••"
                disabled={loading}
                required
              />
            </div>

            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Registering...' : 'Register'}
            </button>
          </form>

          <p className="auth-link">
            Already have an account? <Link to="/login">Login here</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;
