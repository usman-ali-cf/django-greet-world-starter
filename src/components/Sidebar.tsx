import { Link } from 'react-router-dom'

interface SidebarProps {
  projectId?: string
  hidden: boolean
}

export default function Sidebar({ projectId, hidden }: SidebarProps) {
  return (
    <div className={`sidebar fixed left-0 top-0 w-[250px] h-screen bg-[#032952] pt-15 transition-transform duration-300 ease-in-out z-[1000] ${
      hidden ? '-translate-x-full' : 'translate-x-0'
    }`}>
      <nav className="sidebar-nav">
        <Link 
          to="/" 
          className="block text-white p-4 text-lg no-underline transition-colors hover:bg-white/20"
        >
          🏠 Home
        </Link>
        
        {projectId && (
          <>
            <Link 
              to={`/project/${projectId}`}
              className="block text-white p-4 text-lg no-underline transition-colors hover:bg-white/20"
            >
              🔙 Torna al Progetto
            </Link>
            <Link 
              to={`/project/${projectId}/upload-utilities`}
              className="block text-white p-4 text-lg no-underline transition-colors hover:bg-white/20"
            >
              📁 Carica File Utenze
            </Link>
            <Link 
              to={`/project/${projectId}/configure-utilities`}
              className="block text-white p-4 text-lg no-underline transition-colors hover:bg-white/20"
            >
              🛠️ Configura Utenze
            </Link>
            <Link 
              to={`/project/${projectId}/configure-power`}
              className="block text-white p-4 text-lg no-underline transition-colors hover:bg-white/20"
            >
              ⚡ Configura Utenze di Potenza
            </Link>
            <Link 
              to={`/project/${projectId}/create-nodes`}
              className="block text-white p-4 text-lg no-underline transition-colors hover:bg-white/20"
            >
              🖧 Crea Nodi e PLC
            </Link>
            <Link 
              to={`/project/${projectId}/assign-io`}
              className="block text-white p-4 text-lg no-underline transition-colors hover:bg-white/20"
            >
              🔗 Assegna I/O ai Nodi
            </Link>
            <Link 
              to={`/project/${projectId}/configure-panel`}
              className="block text-white p-4 text-lg no-underline transition-colors hover:bg-white/20"
            >
              🗄️ Configura Quadro Elettrico
            </Link>
          </>
        )}
      </nav>
    </div>
  )
}