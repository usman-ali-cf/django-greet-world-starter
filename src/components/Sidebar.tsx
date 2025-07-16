
import React from 'react'

interface SidebarProps {
  projectId?: string
  hidden: boolean
}

const Sidebar: React.FC<SidebarProps> = ({ projectId, hidden }) => {
  const menuItems = [
    { href: '/', label: '🏠 Home', show: true },
    { href: `/project/${projectId}`, label: '🔙 Torna al Progetto', show: !!projectId },
    { href: `/project/${projectId}/upload-utilities`, label: '📁 Carica File Utenze', show: !!projectId },
    { href: `/project/${projectId}/configure-utilities`, label: '🛠️ Configura Utenze', show: !!projectId },
    { href: `/project/${projectId}/configure-power`, label: '⚡ Configura Utenze di Potenza', show: !!projectId },
    { href: `/project/${projectId}/create-nodes`, label: '🖧 Crea Nodi e PLC', show: !!projectId },
    { href: `/project/${projectId}/assign-io`, label: '🔗 Assegna I/O ai Nodi', show: !!projectId },
    { href: `/project/${projectId}/configure-panel`, label: '🗄️ Configura Quadro Elettrico', show: !!projectId }
  ]

  if (hidden) {
    return null
  }

  return (
    <div className="fixed left-0 top-16 bottom-0 w-64 bg-gray-50 border-r border-gray-200 overflow-y-auto z-40">
      <nav className="p-4">
        <div className="space-y-2">
          {menuItems.filter(item => item.show).map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="block px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100 transition-colors"
            >
              {item.label}
            </a>
          ))}
        </div>
      </nav>
    </div>
  )
}

export default Sidebar
