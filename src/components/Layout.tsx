
import { useState, useEffect } from 'react'
import { Outlet, useParams } from 'react-router-dom'

interface LayoutProps {
  title?: string
}

export default function Layout({ title = "Progetto" }: LayoutProps) {
  const [sidebarHidden, setSidebarHidden] = useState(false)
  const { id } = useParams()

  const toggleSidebar = () => {
    setSidebarHidden(!sidebarHidden)
    document.body.classList.toggle('sidebar-hidden')
  }

  useEffect(() => {
    // Handle responsive behavior
    const handleResize = () => {
      if (window.innerWidth <= 768) {
        setSidebarHidden(true)
        document.body.classList.add('sidebar-hidden')
      }
    }

    handleResize()
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return (
    <div className="min-h-screen flex flex-col overflow-hidden">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <button 
            className="sidebar-toggle"
            onClick={toggleSidebar}
          >
            ☰
          </button>
          <h1>{title}</h1>
        </div>
        
        <nav className="header-nav">
          <a href="/">🏠 Home</a>
          {id && (
            <a href={`/project/${id}`}>🔙 Torna al Progetto</a>
          )}
        </nav>
        
        <img 
          src="/static/img/Logo.png" 
          alt="Logo"
          className="logo-app"
        />
      </header>

      {/* Sidebar */}
      <div className={`sidebar ${sidebarHidden ? 'hidden' : ''}`}>
        <nav className="sidebar-nav">
          <a href="/">🏠 Home</a>
          {id && (
            <>
              <a href={`/project/${id}`}>🔙 Torna al Progetto</a>
              <a href={`/project/${id}/upload-utilities`}>📁 Carica File Utenze</a>
              <a href={`/project/${id}/configure-utilities`}>🛠️ Configura Utenze</a>
              <a href={`/project/${id}/configure-power`}>⚡ Configura Utenze di Potenza</a>
              <a href={`/project/${id}/create-nodes`}>🖧 Crea Nodi e PLC</a>
              <a href={`/project/${id}/assign-io`}>🔗 Assegna I/O ai Nodi</a>
              <a href={`/project/${id}/configure-panel`}>🗄️ Configura Quadro Elettrico</a>
            </>
          )}
        </nav>
      </div>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
