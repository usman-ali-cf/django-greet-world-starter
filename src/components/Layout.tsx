import { useState, useEffect } from 'react'
import { Outlet, useParams } from 'react-router-dom'
import Header from './Header'
import Sidebar from './Sidebar'

interface LayoutProps {
  title?: string
}

export default function Layout({ title = "Progetto" }: LayoutProps) {
  const [sidebarHidden, setSidebarHidden] = useState(false)
  const { id } = useParams()

  const toggleSidebar = () => {
    setSidebarHidden(!sidebarHidden)
  }

  useEffect(() => {
    // Handle responsive behavior
    const handleResize = () => {
      if (window.innerWidth <= 768) {
        setSidebarHidden(true)
      }
    }

    handleResize()
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return (
    <div className={`min-h-screen flex flex-col overflow-hidden ${sidebarHidden ? 'sidebar-hidden' : ''}`}>
      <Header 
        title={title} 
        projectId={id}
        onToggleSidebar={toggleSidebar}
      />
      <Sidebar 
        projectId={id}
        hidden={sidebarHidden}
      />
      <main className={`main-content flex-1 transition-all duration-300 ease-in-out overflow-auto ${
        sidebarHidden ? 'ml-0' : 'ml-[250px]'
      } p-5`}>
        <div className="max-w-[1200px] mx-auto bg-white rounded-lg shadow-lg p-5">
          <Outlet />
        </div>
      </main>
    </div>
  )
}