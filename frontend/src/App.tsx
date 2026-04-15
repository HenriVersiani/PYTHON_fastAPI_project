import { useState } from 'react'
import { useAuth } from '@/context/AuthContext'
import { LoginPage } from '@/components/LoginPage'
import { RegisterPage } from '@/components/RegisterPage'
import { UserListPage } from '@/components/UserListPage'
import './App.css'

type Page = 'login' | 'register' | 'users'

function App() {
  const { isAuthenticated, logout, user } = useAuth()
  const [currentPage, setCurrentPage] = useState<Page>('login')

  if (!isAuthenticated) {
    return (
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="logo">FastAPI App</h1>
            <div className="nav-buttons">
              <button
                className={currentPage === 'login' ? 'active' : ''}
                onClick={() => setCurrentPage('login')}
              >
                Login
              </button>
              <button
                className={currentPage === 'register' ? 'active' : ''}
                onClick={() => setCurrentPage('register')}
              >
                Register
              </button>
            </div>
          </div>
        </nav>
        <main>
          {currentPage === 'login' && (
            <LoginPage />
          )}
          {currentPage === 'register' && (
            <RegisterPage onSuccess={() => setCurrentPage('login')} />
          )}
        </main>
      </div>
    )
  }

  return (
    <div className="app authenticated">
      <nav className="navbar">
        <div className="nav-container">
          <h1 className="logo">FastAPI App</h1>
          <div className="user-info">
            <span>Welcome, {user?.name}!</span>
          </div>
          <div className="nav-buttons">
            <button
              className={currentPage === 'users' ? 'active' : ''}
              onClick={() => setCurrentPage('users')}
            >
              Users
            </button>
            <button onClick={logout} className="logout-btn">
              Logout
            </button>
          </div>
        </div>
      </nav>
      <main>
        {currentPage === 'users' && <UserListPage />}
      </main>
    </div>
  )
}

export default App
