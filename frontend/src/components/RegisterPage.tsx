import { useState, ChangeEvent } from 'react'
import { api, ApiError } from '@/services/api'
import { UserCreate } from '@/types/api'
import '../styles/Auth.css'

interface RegisterPageProps {
  onSuccess?: () => void
}

export const RegisterPage = ({ onSuccess }: RegisterPageProps) => {
  const [formData, setFormData] = useState<UserCreate>({
    name: '',
    email: '',
    password: '',
    role_id: 1,
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'role_id' ? parseInt(value) : value,
    }))
  }

  const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await api.createUser(formData)
      setFormData({ name: '', email: '', password: '', role_id: 1 })
      onSuccess?.()
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('Failed to create user')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h1>Register</h1>
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input
              id="name"
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              id="email"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              id="password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label htmlFor="role">Role:</label>
            <select name="role_id" value={formData.role_id} onChange={handleChange} disabled={loading}>
              <option value={1}>User</option>
              <option value={2}>Admin</option>
            </select>
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Register'}
          </button>
        </form>
      </div>
    </div>
  )
}
