import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LayoutDashboard, Users, LogOut } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) return null;

  return (
    <nav className="card" style={{ borderRadius: '0', borderLeft: '0', borderRight: '0', borderTop: '0', padding: '1rem 2rem' }}>
      <div className="flex justify-between items-center" style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div className="flex items-center gap-2">
          <Link to="/dashboard" className="flex items-center gap-2" style={{ textDecoration: 'none', color: 'var(--primary)', fontWeight: 'bold', fontSize: '1.25rem' }}>
            <LayoutDashboard size={24} />
            <span>TaskFlow</span>
          </Link>
        </div>
        
        <div className="flex items-center gap-4">
          <Link to="/dashboard" className="flex items-center gap-1" style={{ textDecoration: 'none', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            Dashboard
          </Link>
          
          {user.role === 'admin' && (
            <Link to="/admin" className="flex items-center gap-1" style={{ textDecoration: 'none', color: 'var(--text-muted)', fontSize: '0.875rem' }}>
              <Users size={18} />
              Admin
            </Link>
          )}
          
          <div className="flex items-center gap-2 ml-4" style={{ paddingLeft: '1rem', borderLeft: '1px solid var(--border)' }}>
            <span style={{ fontSize: '0.875rem', fontWeight: '500' }}>{user.name}</span>
            <button 
              onClick={handleLogout} 
              className="secondary" 
              style={{ width: 'auto', padding: '0.5rem', display: 'flex', alignItems: 'center' }}
              title="Logout"
            >
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
