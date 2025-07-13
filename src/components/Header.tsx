import { Link } from 'react-router-dom'
// Use static path for now - will work with the existing Flask static files

interface HeaderProps {
  title: string
  projectId?: string
  onToggleSidebar: () => void
}

export default function Header({ title, projectId, onToggleSidebar }: HeaderProps) {
  return (
    <header className="header relative flex items-center justify-between min-h-[100px] text-white box-border p-5 md:px-10">
      {/* Background image and overlay handled by CSS */}
      <style jsx>{`
        .header {
          background-image: url('/static/img/schema_elettrico.png');
          background-size: 100%;
          background-position: center;
          animation: headerZoomOut 5s ease-out forwards;
        }
        .header::before {
          content: "";
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: rgba(3, 41, 82, 0.6);
          pointer-events: none;
        }
        .header > * {
          z-index: 1;
        }
        @keyframes headerZoomOut {
          from { background-size: 120%; }
          to { background-size: 100%; }
        }
      `}</style>

      <button 
        className="sidebar-toggle bg-none border-none text-white text-[28px] cursor-pointer z-[1001] mr-4"
        onClick={onToggleSidebar}
      >
        ☰
      </button>

      <div className="header-left">
        <h1 className="text-2xl m-0">{title}</h1>
      </div>

      <nav className="header-nav flex gap-4 mr-[250px]">
        <Link 
          to="/" 
          className="text-white text-base px-3 py-2 rounded transition-colors hover:bg-white/20 no-underline"
        >
          🏠 Home
        </Link>
        {projectId && (
          <Link 
            to={`/project/${projectId}`}
            className="text-white text-base px-3 py-2 rounded transition-colors hover:bg-white/20 no-underline"
          >
            🔙 Torna al Progetto
          </Link>
        )}
      </nav>

      <img 
        className="logo-app absolute top-2.5 right-5 w-[250px] h-auto z-[1000]"
        src="/static/img/Logo.png"
        alt="Logo"
      />
    </header>
  )
}