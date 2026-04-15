import { useEffect, useState } from 'react'
import { api, ApiError } from '@/services/api'
import { useAuth } from '@/context/AuthContext'
import { User } from '@/types/api'
import '../styles/UserList.css'

export const UserListPage = () => {
  const { token, user: currentUser } = useAuth()
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const data = await api.listUsers(token || undefined)
        setUsers(data)
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message)
        } else {
          setError('Failed to load users')
        }
      } finally {
        setLoading(false)
      }
    }

    fetchUsers()
  }, [token])

  const handleDelete = async (userId: number) => {
    if (!confirm('Are you sure?')) return

    try {
      await api.deleteUser(userId, token || undefined)
      setUsers(users.filter((u) => u.id !== userId))
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      }
    }
  }

  if (loading) return <div className="container">Loading...</div>
  if (error) return <div className="container error-message">{error}</div>

  return (
    <div className="container">
      <h1>Users</h1>
      <div className="users-grid">
        {users.map((u) => (
          <div key={u.id} className="user-card">
            <h3>{u.name}</h3>
            <p>Email: {u.email}</p>
            <p>Role: {u.role_id === 1 ? 'User' : 'Admin'}</p>
            {currentUser?.role_id === 2 && (
              <div className="user-actions">
                <button onClick={() => handleDelete(u.id)} className="btn-delete">
                  Delete
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
