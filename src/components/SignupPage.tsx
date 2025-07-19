
import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Container,
  Alert,
  Avatar
} from '@mui/material'
import { PersonAdd, Person, Email, Lock } from '@mui/icons-material'
import Logo from '../img/Logo.png'
import { apiFetch } from '../utils/api'

const SignupPage: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    full_name: ''
  })
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  
  const navigate = useNavigate()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      const response = await apiFetch('/auth/signup', {
        method: 'POST',
        body: JSON.stringify(formData)
      })

      // Store the token
      if (response.access_token) {
        localStorage.setItem('access_token', response.access_token)
        navigate('/', { replace: true })
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registrazione fallita')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        bgcolor: '#ffffff',
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
              bgcolor: '#032952',
              p: 4,
              textAlign: 'center'
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
              Registrati
            </Typography>
            <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.8)', mt: 1 }}>
              Crea il tuo account per iniziare
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
                label="Nome Completo"
                name="full_name"
                variant="outlined"
                value={formData.full_name}
                onChange={handleChange}
                required
                sx={{ mb: 3 }}
                InputProps={{
                  startAdornment: <Person sx={{ color: '#9e9e9e', mr: 1 }} />
                }}
              />

              <TextField
                fullWidth
                label="Username"
                name="username"
                variant="outlined"
                value={formData.username}
                onChange={handleChange}
                required
                autoComplete="username"
                sx={{ mb: 3 }}
                InputProps={{
                  startAdornment: <Person sx={{ color: '#9e9e9e', mr: 1 }} />
                }}
              />

              <TextField
                fullWidth
                label="Email"
                name="email"
                type="email"
                variant="outlined"
                value={formData.email}
                onChange={handleChange}
                required
                autoComplete="email"
                sx={{ mb: 3 }}
                InputProps={{
                  startAdornment: <Email sx={{ color: '#9e9e9e', mr: 1 }} />
                }}
              />

              <TextField
                fullWidth
                label="Password"
                name="password"
                type="password"
                variant="outlined"
                value={formData.password}
                onChange={handleChange}
                required
                autoComplete="new-password"
                sx={{ mb: 4 }}
                InputProps={{
                  startAdornment: <Lock sx={{ color: '#9e9e9e', mr: 1 }} />
                }}
              />

              <Button
                type="submit"
                fullWidth
                variant="contained"
                size="large"
                disabled={isLoading}
                startIcon={<PersonAdd />}
                sx={{
                  py: 1.5,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  bgcolor: '#032952',
                  '&:hover': { bgcolor: '#021e3a' },
                  '&:disabled': { bgcolor: '#e0e0e0' },
                  mb: 3
                }}
              >
                {isLoading ? 'Registrazione in corso...' : 'Registrati'}
              </Button>

              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="body2" sx={{ color: '#666' }}>
                  Hai già un account?{' '}
                  <Link 
                    to="/login" 
                    style={{ 
                      color: '#032952', 
                      textDecoration: 'none',
                      fontWeight: 600
                    }}
                  >
                    Accedi qui
                  </Link>
                </Typography>
              </Box>
            </form>
          </CardContent>
        </Card>
      </Container>
    </Box>
  )
}

export default SignupPage
