
import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Layout from './components/Layout'
import ProjectManagement from './components/ProjectManagement'
import ProjectDetail from './components/ProjectDetail'
import PlaceholderPage from './components/PlaceholderPage'
import CreateNodesPage from './components/CreateNodesPage'
import AssignIOPage from './components/AssignIOPage'
import LoginPage from './components/LoginPage'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Login page */}
          <Route path="/login" element={<LoginPage />} />
          
          {/* Protected routes */}
          <Route path="/" element={
            <ProtectedRoute>
              <Layout title="Gestione Progetto">
                <ProjectManagement />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/project/:id" element={
            <ProtectedRoute>
              <Layout title="Dettagli Progetto">
                <ProjectDetail />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/project/:id/upload-utilities" element={
            <ProtectedRoute>
              <Layout title="Carica File Utenze">
                <PlaceholderPage pageName="Carica File Utenze" />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/project/:id/configure-utilities" element={
            <ProtectedRoute>
              <Layout title="Configura Utenze">
                <PlaceholderPage pageName="Configura Utenze" />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/project/:id/configure-power" element={
            <ProtectedRoute>
              <Layout title="Configura Utenze di Potenza">
                <PlaceholderPage pageName="Configura Utenze di Potenza" />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/project/:id/create-nodes" element={
            <ProtectedRoute>
              <Layout title="Crea Nodi e PLC">
                <CreateNodesPage />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/project/:id/assign-io" element={
            <ProtectedRoute>
              <Layout title="Assegna I/O ai Nodi">
                <AssignIOPage />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/project/:id/configure-panel" element={
            <ProtectedRoute>
              <Layout title="Configura Quadro Elettrico">
                <PlaceholderPage pageName="Configura Quadro Elettrico" />
              </Layout>
            </ProtectedRoute>
          } />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
