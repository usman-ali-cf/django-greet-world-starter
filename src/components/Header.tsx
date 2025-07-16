
import React from 'react'
import { useAuth } from '../contexts/AuthContext'

interface HeaderProps {
  title: string
  projectId?: string
  onToggleSidebar: () => void
}

const Header: React.FC<HeaderProps> = ({ title, projectId, onToggleSidebar }) => {
  const { logout } = useAuth()

  const handleLogout = () => {
    logout()
    window.location.href = '/login'
  }

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-4 py-3 flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-md hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          ☰
        </button>
        <h1 className="text-xl font-semibold text-gray-900">{title}</h1>
      </div>
      
      <nav className="flex items-center space-x-4">
        <a 
          href="/" 
          className="text-blue-600 hover:text-blue-800 flex items-center space-x-1"
        >
          <span>🏠</span>
          <span>Home</span>
        </a>
        {projectId && (
          <a 
            href={`/project/${projectId}`}
            className="text-blue-600 hover:text-blue-800 flex items-center space-x-1"
          >
            <span>🔙</span>
            <span>Torna al Progetto</span>
          </a>
        )}
        <button
          onClick={handleLogout}
          className="text-red-600 hover:text-red-800 flex items-center space-x-1"
        >
          <span>🚪</span>
          <span>Logout</span>
        </button>
      </nav>
      
      <img 
        src="/api/placeholder/50/50" 
        alt="Logo"
        className="h-10 w-10 rounded"
      />
    </header>
  )
}

export default Header
