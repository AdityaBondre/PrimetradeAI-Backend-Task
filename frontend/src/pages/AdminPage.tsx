import React, { useState, useEffect } from 'react';
import axiosInstance from '../api/axiosInstance';
import { UserCheck, UserMinus, Shield, ShieldAlert, Trash2 } from 'lucide-react';

interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  is_active: boolean;
  created_at: string;
}

const AdminPage = () => {
  const [users, setUsers] = useState<UserProfile[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchUsers = async () => {
    try {
      const response = await axiosInstance.get('/admin/users');
      setUsers(response.data.data);
    } catch (err) {
      console.error('Failed to fetch users', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleToggleStatus = async (user: UserProfile) => {
    try {
      await axiosInstance.patch(`/admin/users/${user.id}`, { is_active: !user.is_active });
      fetchUsers();
    } catch (err) {
      alert('Failed to update user status');
    }
  };

  const handleToggleRole = async (user: UserProfile) => {
    const newRole = user.role === 'admin' ? 'user' : 'admin';
    try {
      await axiosInstance.patch(`/admin/users/${user.id}/role`, { role: newRole });
      fetchUsers();
    } catch (err) {
      alert('Failed to update user role');
    }
  };

  const handleDeleteUser = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this user? This will also delete all their tasks.')) return;
    try {
      await axiosInstance.delete(`/admin/users/${id}`);
      fetchUsers();
    } catch (err) {
      alert('Failed to delete user');
    }
  };

  if (loading) return <div className="container text-center">Loading user management...</div>;

  return (
    <div className="container">
      <div style={{ marginBottom: '2rem' }}>
        <h1>User Management</h1>
        <p style={{ color: 'var(--text-muted)' }}>Manage platform users, roles, and account status.</p>
      </div>

      <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead style={{ backgroundColor: '#f1f5f9' }}>
            <tr>
              <th style={{ padding: '1rem' }}>User</th>
              <th style={{ padding: '1rem' }}>Email</th>
              <th style={{ padding: '1rem' }}>Role</th>
              <th style={{ padding: '1rem' }}>Status</th>
              <th style={{ padding: '1rem' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} style={{ borderTop: '1px solid var(--border)' }}>
                <td style={{ padding: '1rem' }}>
                  <div style={{ fontWeight: '600' }}>{u.name}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Joined {new Date(u.created_at).toLocaleDateString()}</div>
                </td>
                <td style={{ padding: '1rem' }}>{u.email}</td>
                <td style={{ padding: '1rem' }}>
                  <span style={{ 
                    fontSize: '0.75rem', 
                    padding: '0.2rem 0.5rem', 
                    borderRadius: '1rem', 
                    backgroundColor: u.role === 'admin' ? '#e0e7ff' : '#f1f5f9',
                    color: u.role === 'admin' ? 'var(--primary)' : 'var(--text-muted)',
                    fontWeight: '600',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                    width: 'fit-content'
                  }}>
                    {u.role === 'admin' ? <Shield size={12} /> : <UserCheck size={12} />}
                    {u.role}
                  </span>
                </td>
                <td style={{ padding: '1rem' }}>
                  <span style={{ 
                    fontSize: '0.75rem', 
                    color: u.is_active ? 'var(--success)' : 'var(--danger)',
                    fontWeight: '600'
                  }}>
                    {u.is_active ? 'Active' : 'Deactivated'}
                  </span>
                </td>
                <td style={{ padding: '1rem' }}>
                  <div className="flex gap-2">
                    <button 
                      onClick={() => handleToggleRole(u)} 
                      className="secondary" 
                      style={{ width: 'auto', padding: '0.4rem' }}
                      title={u.role === 'admin' ? "Demote to User" : "Promote to Admin"}
                    >
                      {u.role === 'admin' ? <ShieldAlert size={16} /> : <Shield size={16} />}
                    </button>
                    <button 
                      onClick={() => handleToggleStatus(u)} 
                      className="secondary" 
                      style={{ width: 'auto', padding: '0.4rem' }}
                      title={u.is_active ? "Deactivate User" : "Activate User"}
                    >
                      {u.is_active ? <UserMinus size={16} color="var(--danger)" /> : <UserCheck size={16} color="var(--success)" />}
                    </button>
                    <button 
                      onClick={() => handleDeleteUser(u.id)} 
                      className="secondary" 
                      style={{ width: 'auto', padding: '0.4rem', color: 'var(--danger)' }}
                      title="Delete User"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminPage;
