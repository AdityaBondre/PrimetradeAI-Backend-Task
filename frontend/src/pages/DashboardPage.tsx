import { useState, useEffect } from 'react';
import axiosInstance from '../api/axiosInstance';
import { Plus, Trash2, Edit2, CheckCircle, Clock, AlertCircle } from 'lucide-react';

interface Task {
  id: string;
  title: string;
  description: string;
  status: 'todo' | 'in_progress' | 'done';
  priority: 'low' | 'medium' | 'high';
  created_at: string;
}

const DashboardPage = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [currentTask, setCurrentTask] = useState<Partial<Task> | null>(null);
  
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState<'todo' | 'in_progress' | 'done'>('todo');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>('medium');

  const fetchTasks = async () => {
    try {
      const response = await axiosInstance.get('/tasks/');
      setTasks(response.data.data);
    } catch (err) {
      console.error('Failed to fetch tasks', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (currentTask?.id) {
        await axiosInstance.put(`/tasks/${currentTask.id}`, { title, description, status, priority });
      } else {
        await axiosInstance.post('/tasks/', { title, description, status, priority });
      }
      fetchTasks();
      closeModal();
    } catch (err) {
      alert('Failed to save task');
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;
    try {
      await axiosInstance.delete(`/tasks/${id}`);
      fetchTasks();
    } catch (err) {
      alert('Failed to delete task');
    }
  };

  const openModal = (task?: Task) => {
    if (task) {
      setCurrentTask(task);
      setTitle(task.title);
      setDescription(task.description || '');
      setStatus(task.status);
      setPriority(task.priority);
    } else {
      setCurrentTask(null);
      setTitle('');
      setDescription('');
      setStatus('todo');
      setPriority('medium');
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setCurrentTask(null);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'done': return <CheckCircle size={16} color="var(--success)" />;
      case 'in_progress': return <Clock size={16} color="var(--primary)" />;
      default: return <AlertCircle size={16} color="var(--text-muted)" />;
    }
  };

  if (loading) return <div className="container text-center">Loading tasks...</div>;

  return (
    <div className="container">
      <div className="flex justify-between items-center" style={{ marginBottom: '2rem' }}>
        <h1>My Tasks</h1>
        <button onClick={() => openModal()} style={{ width: 'auto' }} className="flex items-center gap-2">
          <Plus size={20} />
          <span>Add Task</span>
        </button>
      </div>

      <div className="flex gap-2" style={{ marginBottom: '1.5rem' }}>
        {/* Filters could go here */}
      </div>

      <div className="grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.5rem' }}>
        {tasks.map((task) => (
          <div key={task.id} className="card" style={{ padding: '1.5rem' }}>
            <div className="flex justify-between items-start" style={{ marginBottom: '1rem' }}>
              <div className="flex items-center gap-2">
                {getStatusIcon(task.status)}
                <span style={{ fontSize: '0.75rem', fontWeight: '600', textTransform: 'uppercase', color: 'var(--text-muted)' }}>
                  {task.status.replace('_', ' ')}
                </span>
              </div>
              <div className="flex gap-2">
                <button onClick={() => openModal(task)} className="secondary" style={{ width: 'auto', padding: '0.4rem' }}>
                  <Edit2 size={16} />
                </button>
                <button onClick={() => handleDelete(task.id)} className="secondary" style={{ width: 'auto', padding: '0.4rem', color: 'var(--danger)' }}>
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
            
            <h3 style={{ marginBottom: '0.5rem' }}>{task.title}</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '1rem', minHeight: '3em' }}>
              {task.description || 'No description provided.'}
            </p>
            
            <div className="flex justify-between items-center mt-4 pt-4" style={{ borderTop: '1px solid var(--border)' }}>
              <span style={{ 
                fontSize: '0.75rem', 
                padding: '0.2rem 0.5rem', 
                borderRadius: '1rem', 
                backgroundColor: task.priority === 'high' ? '#fee2e2' : task.priority === 'medium' ? '#fef3c7' : '#f0fdf4',
                color: task.priority === 'high' ? '#991b1b' : task.priority === 'medium' ? '#92400e' : '#166534',
                fontWeight: '600'
              }}>
                {task.priority} priority
              </span>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                {new Date(task.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
        ))}
      </div>

      {tasks.length === 0 && (
        <div className="card text-center" style={{ padding: '4rem' }}>
          <p style={{ color: 'var(--text-muted)' }}>No tasks found. Create one to get started!</p>
        </div>
      )}

      {showModal && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100
        }}>
          <div className="card" style={{ width: '100%', maxWidth: '500px' }}>
            <h2>{currentTask ? 'Edit Task' : 'New Task'}</h2>
            <form onSubmit={handleSubmit} className="mt-4">
              <div className="form-group">
                <label>Title</label>
                <input value={title} onChange={(e) => setTitle(e.target.value)} required />
              </div>
              <div className="form-group">
                <label>Description</label>
                <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} style={{ width: '100%', padding: '0.75rem', borderRadius: '0.5rem', border: '1px solid var(--border)' }} />
              </div>
              <div className="flex gap-2">
                <div className="form-group" style={{ flex: 1 }}>
                  <label>Status</label>
                  <select value={status} onChange={(e) => setStatus(e.target.value as any)}>
                    <option value="todo">Todo</option>
                    <option value="in_progress">In Progress</option>
                    <option value="done">Done</option>
                  </select>
                </div>
                <div className="form-group" style={{ flex: 1 }}>
                  <label>Priority</label>
                  <select value={priority} onChange={(e) => setPriority(e.target.value as any)}>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>
              <div className="flex gap-2 mt-4">
                <button type="button" onClick={closeModal} className="secondary">Cancel</button>
                <button type="submit">Save Task</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
