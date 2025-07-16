
import { useState, useEffect } from 'react'
import { Outlet, useParams, Link } from 'react-router-dom'
import logoImage from '@/img/Logo.png'

interface LayoutProps {
  title?: string
}

export default function Layout({ title = "Progetto" }: LayoutProps) {
  const [sidebarHidden, setSidebarHidden] = useState(false)
  const { id } = useParams()

  const toggleSidebar = () => {
    setSidebarHidden(!sidebarHidden)
    document.body.classList.toggle('sidebar-hidden')
    console.log("Sidebar toggle", sidebarHidden)
  }

  useEffect(() => {
    // Handle responsive behavior
    const handleResize = () => {
      if (window.innerWidth <= 768) {
        setSidebarHidden(true)
        document.body.classList.add('sidebar-hidden')
        console.log("Sidebar hidden")
      } else {
        setSidebarHidden(false)
        document.body.classList.remove('sidebar-hidden')
        console.log("Sidebar visible")
      }
    }

    handleResize()
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    window.location.href = '/login'
  }

  return (
    <div className="min-h-screen flex flex-col">
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
          <Link to="/">🏠 Home</Link>
          {id && (
            <Link to={`/project/${id}`}>🔙 Torna al Progetto</Link>
          )}
          <button 
            onClick={handleLogout} 
            style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer' }}
          >
            🚪 Logout
          </button>
        </nav>
        
        <img 
          src={logoImage} 
          alt="Logo"
          className="logo-app"
        />
      </header>

      <div className="flex flex-1">
        {/* Sidebar */}
        <div id="sidebar" className={`sidebar ${sidebarHidden ? 'hidden' : ''}`}>
          <nav className="sidebar-nav">
            <Link to="/">🏠 Home</Link>
            {id && (
              <>
                <Link to={`/project/${id}`}>🔙 Torna al Progetto</Link>
                <Link to={`/project/${id}/upload-utilities`}>📁 Carica File Utenze</Link>
                <Link to={`/project/${id}/configure-utilities`}>🛠️ Configura Utenze</Link>
                <Link to={`/project/${id}/configure-power`}>⚡ Configura Utenze di Potenza</Link>
                <Link to={`/project/${id}/create-nodes`}>🖧 Crea Nodi e PLC</Link>
                <Link to={`/project/${id}/assign-io`}>🔗 Assegna I/O ai Nodi</Link>
                <Link to={`/project/${id}/configure-panel`}>🗄️ Configura Quadro Elettrico</Link>
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
    </div>
  )
}
