import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Menu, X, LogOut } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

interface HeaderProps {
  title: string
  projectId?: string
  onToggleSidebar: () => void
}

export default function Header({ title, projectId, onToggleSidebar }: HeaderProps) {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768)
    }

    handleResize()
    window.addEventListener('resize', handleResize)

    return () => window.removeEventListener('resize', handleResize)
  }, [])
  const { user, logout } = useAuth()

  const handleLogout = () => {
    logout()
  }

  return (
    <header className="header bg-white shadow-lg border-b border-gray-200 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-r from-blue-50 via-blue-100 to-blue-50 opacity-50"></div>
      <div className="container mx-auto px-4 h-full relative z-10">
        <div className="flex items-center justify-between h-full">
          {/* Left section */}
          <div className="flex items-center space-x-4">
            <button
              onClick={onToggleSidebar}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
              aria-label="Toggle sidebar"
            >
              <Menu className="h-6 w-6 text-gray-600" />
            </button>
            
            <Link to="/" className="flex items-center space-x-3">
              <img 
                src="/static/img/Logo.png" 
                alt="Logo" 
                className="h-10 w-auto"
              />
              <div>
                <h1 className="text-xl font-bold text-gray-800">{title}</h1>
                {projectId && (
                  <p className="text-sm text-gray-600">Progetto ID: {projectId}</p>
                )}
              </div>
            </Link>
          </div>

          {/* Right section */}
          <div className="flex items-center space-x-4">
            {user && (
              <div className="flex items-center space-x-3">
                <span className="text-sm text-gray-600">
                  Benvenuto, {user.full_name || user.username}
                </span>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <LogOut className="h-4 w-4" />
                  <span>Esci</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
