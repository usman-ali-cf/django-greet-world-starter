import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import ProjectManagement from './components/ProjectManagement'
import ProjectDetail from './components/ProjectDetail'
import PlaceholderPage from './components/PlaceholderPage'
import CreateNodesPage from './components/CreateNodesPage'
import AssignIOPage from './components/AssignIOPage'
// Background image handled by CSS with static path

function App() {
  return (
    <Router>
      <Routes>
        {/* Main project management page */}
        <Route path="/" element={
          <Layout title="Gestione Progetto">
            <ProjectManagement />
          </Layout>
        } />
        
        {/* Project detail page */}
        <Route path="/project/:id" element={
          <Layout title="Dettagli Progetto">
            <ProjectDetail />
          </Layout>
        } />
        
        {/* Project-specific pages - placeholders for now */}
        <Route path="/project/:id/upload-utilities" element={
          <Layout title="Carica File Utenze">
            <PlaceholderPage pageName="Carica File Utenze" />
          </Layout>
        } />
        
        <Route path="/project/:id/configure-utilities" element={
          <Layout title="Configura Utenze">
            <PlaceholderPage pageName="Configura Utenze" />
          </Layout>
        } />
        
        <Route path="/project/:id/configure-power" element={
          <Layout title="Configura Utenze di Potenza">
            <PlaceholderPage pageName="Configura Utenze di Potenza" />
          </Layout>
        } />
        
        <Route path="/project/:id/create-nodes" element={
          <Layout title="Crea Nodi e PLC">
            <CreateNodesPage />
          </Layout>
        } />
        
        <Route path="/project/:id/assign-io" element={
          <Layout title="Assegna I/O ai Nodi">
            <AssignIOPage />
          </Layout>
        } />
        
        <Route path="/project/:id/configure-panel" element={
          <Layout title="Configura Quadro Elettrico">
            <PlaceholderPage pageName="Configura Quadro Elettrico" />
          </Layout>
        } />
      </Routes>
    </Router>
  )
}

export default App