
import { useState, useEffect } from 'react'
import { Outlet, useParams, Link, useLocation } from 'react-router-dom'
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
  const isHomePage = location.pathname === '/'

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    window.location.href = '/login'
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
      {/* Header - only show for non-home pages */}
      {!isHomePage && (
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
              <Button
                component={Link}
                to="/"
                startIcon={<Home />}
                sx={{ color: '#1a1a1a' }}
              >
                Home
              </Button>
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
                sx={{ color: '#1a1a1a' }}
              >
                Logout
              </Button>
            </Box>
            
            <Box component="img" src={logoImage} alt="Logo" sx={{ height: 40, ml: 2 }} />
          </Toolbar>
        </AppBar>
      )}

      <Box sx={{ display: 'flex', flex: 1 }}>
        {/* Sidebar */}
        <Drawer
          variant="temporary"
          anchor="left"
          open={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          sx={{
            '& .MuiDrawer-paper': {
              width: 280,
              bgcolor: '#fafafa',
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
                  '&:hover': {
                    bgcolor: '#e3f2fd'
                  },
                  ...(location.pathname === item.path && {
                    bgcolor: '#e3f2fd',
                    '& .MuiListItemIcon-root': {
                      color: '#1976d2'
                    },
                    '& .MuiListItemText-primary': {
                      color: '#1976d2',
                      fontWeight: 600
                    }
                  })
                }}
              >
                <ListItemIcon sx={{ minWidth: 40 }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
          </List>
        </Drawer>

        {/* Main Content */}
        <Box 
          component="main" 
          sx={{ 
            flexGrow: 1, 
            bgcolor: '#ffffff',
            minHeight: isHomePage ? '100vh' : 'auto'
          }}
        >
          {children}
        </Box>
      </Box>
    </Box>
  )
}
