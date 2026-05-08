import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axiosInstance from '../api/axiosInstance';
import { useAuth } from '../context/AuthContext';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await axiosInstance.post('/auth/login', { email, password });
      const { access_token, refresh_token } = response.data.data;
      
      // Fetch user profile after login
      const profileResponse = await axiosInstance.get('/auth/me', {
        headers: { Authorization: `Bearer ${access_token}` }
      });
      const userProfile = profileResponse.data.data;
      
      login(access_token, refresh_token, userProfile);
      
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '450px', marginTop: '100px' }}>
      <div className="card">
        <h2 className="text-center" style={{ marginBottom: '2rem' }}>Login</h2>
        {error && <div className="error-message text-center" style={{ marginBottom: '1rem' }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="name@company.com"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="••••••••"
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Sign In'}
          </button>
        </form>
        <div className="mt-4 text-center">
          <p style={{ fontSize: '0.875rem' }}>
            Don't have an account? <Link to="/register" style={{ color: 'var(--primary)', fontWeight: '600' }}>Register</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
