import React from 'react'
import logoImage from '@/img/Logo.png'

interface HeaderProps {
  title: string
  projectId?: string
  onToggleSidebar: () => void
}

const Header: React.FC<HeaderProps> = ({ title, projectId, onToggleSidebar }) => {
  const handleLogout = () => {
    localStorage.removeItem('access_token')
    window.location.href = '/login'
  }

  return (
    <header className="header">
      <div className="header-left">
        <button
          onClick={onToggleSidebar}
          className="sidebar-toggle"
        >
          ☰
        </button>
        <h1>{title}</h1>
      </div>
      
      <nav className="header-nav">
        <a href="/">🏠 Home</a>
        {projectId && (
          <a href={`/project/${projectId}`}>🔙 Torna al Progetto</a>
        )}
        <button onClick={handleLogout} style={{ background: '#032952', border: 'none', color: 'white', cursor: 'pointer', padding: '8px 12px' }}>
          🚪 Logout
        </button>
      </nav>
      
      <img 
        src={logoImage} 
        alt="Logo"
        className="logo-app"
      />
    </header>
  )
}

export default Header
