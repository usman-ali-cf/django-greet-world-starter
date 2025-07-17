
import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate, useLocation } from 'react-router-dom'
import Logo from '../img/Logo.png'

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await login(username, password)
      // Redirect to intended page or dashboard
      const redirectTo = (location.state as any)?.from?.pathname || '/'
      navigate(redirectTo, { replace: true })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="custom-login-page">
      <div className="custom-login-blur custom-login-blur1" />
      <div className="custom-login-blur custom-login-blur2" />
      <div className="custom-login-card">
        <img src={Logo} alt="Logo" className="custom-login-logo" />
        <h2 className="custom-login-title">Accedi al tuo account</h2>
        <form className="custom-login-form" onSubmit={handleSubmit}>
          {error && (
            <div className="custom-login-error">{error}</div>
          )}
          <input
            id="username"
            name="username"
            type="text"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="custom-login-input"
            placeholder="Username"
            autoComplete="username"
          />
          <input
            id="password"
            name="password"
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="custom-login-input"
            placeholder="Password"
            autoComplete="current-password"
          />
          <button
            type="submit"
            disabled={isLoading}
            className="custom-login-button"
          >
            {isLoading ? 'Accesso in corso...' : 'Accedi'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default LoginPage
