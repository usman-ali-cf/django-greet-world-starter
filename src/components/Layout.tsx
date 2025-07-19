
import { useState } from 'react'
import { useParams, Link, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  IconButton, 
  Drawer, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText,
  Box,
  Button
} from '@mui/material'
import {
  Menu,
  Home,
  ArrowBack,
  Logout,
  Upload,
  Settings,
  Power,
  Hub,
  Cable,
  Dashboard
} from '@mui/icons-material'
import logoImage from '@/img/Logo.png'

interface LayoutProps {
  title?: string;
  children: React.ReactNode;
}

export default function Layout({ title = "Progetto", children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { id } = useParams()
  const location = useLocation()
  const { logout } = useAuth()
  const isHomePage = location.pathname === '/'

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  const handleLogout = () => {
    logout()
  }

  const menuItems = [
    { text: 'Home', icon: <Home />, path: '/' },
    ...(id ? [
      { text: 'Torna al Progetto', icon: <ArrowBack />, path: `/project/${id}` },
      { text: 'Carica File Utenze', icon: <Upload />, path: `/project/${id}/upload-utilities` },
      { text: 'Configura Utenze', icon: <Settings />, path: `/project/${id}/configure-utilities` },
      { text: 'Configura Utenze di Potenza', icon: <Power />, path: `/project/${id}/configure-power` },
      { text: 'Crea Nodi e PLC', icon: <Hub />, path: `/project/${id}/create-nodes` },
      { text: 'Assegna I/O ai Nodi', icon: <Cable />, path: `/project/${id}/assign-io` },
      { text: 'Configura Quadro Elettrico', icon: <Dashboard />, path: `/project/${id}/configure-panel` }
    ] : [])
  ]

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', bgcolor: '#ffffff' }}>
      <AppBar 
        position="static" 
        elevation={0}
        sx={{ 
          bgcolor: '#ffffff', 
          borderBottom: '1px solid #e0e0e0',
          color: '#1a1a1a'
        }}
      >
        <Toolbar>
          <IconButton
            edge="start"
            onClick={toggleSidebar}
            sx={{ mr: 2, color: '#1a1a1a' }}
          >
            <Menu />
          </IconButton>
          
          <Typography variant="h6" component="h1" sx={{ flexGrow: 1, fontWeight: 600 }}>
            {title}
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            {!isHomePage && (
              <Button
                component={Link}
                to="/"
                startIcon={<Home />}
                sx={{ color: '#1a1a1a' }}
              >
                Home
              </Button>
            )}
            {id && (
              <Button
                component={Link}
                to={`/project/${id}`}
                startIcon={<ArrowBack />}
                sx={{ color: '#1a1a1a' }}
              >
                Torna al Progetto
              </Button>
            )}
            <Button
              onClick={handleLogout}
              startIcon={<Logout />}
              sx={{ 
                color: '#1a1a1a',
                px: 3,
                py: 1.5,
                '&:hover': {
                  color: '#ffffff',
                  bgcolor: '#032952'
                }
              }}
            >
              Logout
            </Button>
          </Box>
          
          <Box component="img" src={logoImage} alt="Logo" sx={{ height: 40, ml: 2 }} />
        </Toolbar>
      </AppBar>

      <Box sx={{ display: 'flex', flex: 1 }}>
        <Drawer
          variant="temporary"
          anchor="left"
          open={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          sx={{
            '& .MuiDrawer-paper': {
              width: 280,
              bgcolor: '#032952',
              borderRight: '1px solid #e0e0e0'
            }
          }}
        >
          <List sx={{ pt: 2 }}>
            {menuItems.map((item) => (
              <ListItem
                key={item.path}
                component={Link}
                to={item.path}
                onClick={() => setSidebarOpen(false)}
                sx={{
                  mx: 1,
                  mb: 0.5,
                  borderRadius: 1,
                  color: '#ffffff',
                  '&:hover': {
                    bgcolor: 'rgba(255, 255, 255, 0.1)',
                    color: '#ffffff',
                    '& .MuiListItemIcon-root': {
                      color: '#ffffff'
                    },
                    '& .MuiListItemText-primary': {
                      color: '#ffffff'
                    }
                  },
                  ...(location.pathname === item.path && {
                    bgcolor: 'rgba(255, 255, 255, 0.15)',
                    '& .MuiListItemIcon-root': {
                      color: '#ffffff'
                    },
                    '& .MuiListItemText-primary': {
                      color: '#ffffff',
                      fontWeight: 600
                    }
                  })
                }}
              >
                <ListItemIcon sx={{ minWidth: 40, color: '#ffffff' }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText 
                  primary={item.text} 
                  sx={{ 
                    '& .MuiListItemText-primary': {
                      color: '#ffffff'
                    }
                  }}
                />
              </ListItem>
            ))}
          </List>
        </Drawer>

        <Box 
          component="main" 
          sx={{ 
            flexGrow: 1, 
            bgcolor: '#ffffff',
            minHeight: isHomePage ? 'auto' : 'auto'
          }}
        >
          {children}
        </Box>
      </Box>
    </Box>
  )
}
