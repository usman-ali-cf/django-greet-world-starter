
import React, { useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate, useLocation } from 'react-router-dom'
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Container,
  Alert,
  Paper,
  Avatar
} from '@mui/material'
import { Login, Person } from '@mui/icons-material'
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
      const redirectTo = (location.state as any)?.from?.pathname || '/'
      navigate(redirectTo, { replace: true })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        bgcolor: '#fafafa',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        p: 2
      }}
    >
      <Container maxWidth="sm">
        <Card 
          elevation={0}
          sx={{ 
            border: '1px solid #e0e0e0',
            borderRadius: 3,
            overflow: 'hidden'
          }}
        >
          <Box
            sx={{
              bgcolor: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
              p: 4,
              textAlign: 'center',
              bgcolor: '#1976d2'
            }}
          >
            <Avatar
              sx={{
                width: 80,
                height: 80,
                mx: 'auto',
                mb: 2,
                bgcolor: 'white',
                p: 1
              }}
            >
              <img 
                src={Logo} 
                alt="Logo" 
                style={{ width: '100%', height: '100%', objectFit: 'contain' }}
              />
            </Avatar>
            <Typography variant="h4" component="h1" sx={{ color: 'white', fontWeight: 600 }}>
              Benvenuto
            </Typography>
            <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.8)', mt: 1 }}>
              Accedi al tuo account per continuare
            </Typography>
          </Box>

          <CardContent sx={{ p: 4 }}>
            <form onSubmit={handleSubmit}>
              {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                  {error}
                </Alert>
              )}

              <TextField
                fullWidth
                label="Username"
                variant="outlined"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                autoComplete="username"
                sx={{ mb: 3 }}
                InputProps={{
                  startAdornment: <Person sx={{ color: '#9e9e9e', mr: 1 }} />
                }}
              />

              <TextField
                fullWidth
                label="Password"
                type="password"
                variant="outlined"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
                sx={{ mb: 4 }}
              />

              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={isLoading}
                startIcon={<Login />}
                sx={{
                  py: 1.5,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  bgcolor: '#1976d2',
                  '&:hover': { bgcolor: '#1565c0' },
                  '&:disabled': { bgcolor: '#e0e0e0' }
                }}
              >
                {isLoading ? 'Accesso in corso...' : 'Accedi'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </Container>
    </Box>
  )
}

export default LoginPage
