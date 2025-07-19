
import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { apiFetch } from '../utils/api'
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  Container,
  Chip,
  CircularProgress,
  Alert
} from '@mui/material'
import {
  Upload,
  Settings,
  Power,
  Hub,
  Cable,
  Dashboard
} from '@mui/icons-material'

interface Project {
  id_prg: number
  nome_progetto: string
  descrizione: string
  data_creazione: string
}

const ProjectDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const [project, setProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadProject = async () => {
      try {
        const data = await apiFetch(`/api/projects/${id}`)
        setProject(data)
      } catch (error) {
        console.error('Error loading project:', error)
      } finally {
        setLoading(false)
      }
    }

    if (id) {
      loadProject()
    }
  }, [id])

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
        <CircularProgress />
      </Container>
    )
  }

  if (!project) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Alert severity="error">Progetto non trovato</Alert>
      </Container>
    )
  }

  const menuItems = [
    {
      title: 'Carica File Utenze',
      path: `/project/${id}/upload-utilities`,
      icon: <Upload />,
      description: 'Carica un file Excel con le utenze del progetto',
      color: '#1976d2'
    },
    {
      title: 'Configura Utenze',
      path: `/project/${id}/configure-utilities`,
      icon: <Settings />,
      description: 'Configura le utenze caricate',
      color: '#388e3c'
    },
    {
      title: 'Configura Utenze di Potenza',
      path: `/project/${id}/configure-power`,
      icon: <Power />,
      description: 'Configura le utenze di potenza',
      color: '#f57c00'
    },
    {
      title: 'Crea Nodi e PLC',
      path: `/project/${id}/create-nodes`,
      icon: <Hub />,
      description: 'Crea e gestisci nodi e PLC',
      color: '#7b1fa2'
    },
    {
      title: 'Assegna I/O ai Nodi',
      path: `/project/${id}/assign-io`,
      icon: <Cable />,
      description: 'Assegna I/O ai moduli dei nodi',
      color: '#d32f2f'
    },
    {
      title: 'Configura Quadro Elettrico',
      path: `/project/${id}/configure-panel`,
      icon: <Dashboard />,
      description: 'Configura il quadro elettrico',
      color: '#303f9f'
    }
  ]

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Card elevation={0} sx={{ mb: 4, border: '1px solid #e0e0e0', backgroundColor: '#032952' }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600, color: '#fff' }}>
            {project.nome_progetto}
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3, fontSize: '1.1rem', color: '#fff' }}>
            {project.descrizione}
          </Typography>
          <Chip 
            label={`Creato il: ${new Date(project.data_creazione).toLocaleDateString('it-IT')}`}
            variant="outlined"
            size="small"
            sx={{ bgcolor: '#f5f5f5', color: '#000', border: '1px solid #000', padding: '4px 8px' }}
          />
        </CardContent>
      </Card>

      <Card elevation={0} sx={{ border: '1px solid #e0e0e0' }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom sx={{ fontWeight: 600, mb: 3 }}>
            Opzioni di Configurazione
          </Typography>
          <Grid container spacing={3}>
            {menuItems.map((item) => (
              <Grid item xs={12} sm={6} md={4} key={item.path}>
                <Card 
                  elevation={0}
                  sx={{ 
                    height: '100%',
                    cursor: 'pointer',
                    border: '1px solid #e0e0e0',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: '0 8px 25px rgba(0,0,0,0.1)',
                      borderColor: item.color
                    }
                  }}
                  onClick={() => window.location.href = item.path}
                >
                  <CardContent sx={{ p: 3, textAlign: 'center', height: '100%', display: 'flex', flexDirection: 'column' }}>
                    <Box sx={{ color: item.color, mb: 2 }}>
                      {React.cloneElement(item.icon, { sx: { fontSize: 40 } })}
                    </Box>
                    <Typography variant="h6" component="h3" gutterBottom sx={{ fontWeight: 600, mb: 1 }}>
                      {item.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ flexGrow: 1 }}>
                      {item.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>
    </Container>
  )
}

export default ProjectDetail
