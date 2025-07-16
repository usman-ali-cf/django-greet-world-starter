
import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { apiFetch } from '../utils/api'

interface Project {
  id_prg: number
  nome_progetto: string
  descrizione: string
  data_creazione: string
}

const ProjectDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const [project, setProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadProject = async () => {
      try {
        const data = await apiFetch(`/api/progetto/${id}`)
        setProject(data)
      } catch (error) {
        console.error('Error loading project:', error)
      } finally {
        setLoading(false)
      }
    }

    if (id) {
      loadProject()
    }
  }, [id])

  if (loading) {
    return <div className="text-center p-8">Caricamento...</div>
  }

  if (!project) {
    return <div className="text-center p-8">Progetto non trovato</div>
  }

  const menuItems = [
    {
      title: 'Carica File Utenze',
      path: `/project/${id}/upload-utilities`,
      icon: '📁',
      description: 'Carica un file Excel con le utenze del progetto'
    },
    {
      title: 'Configura Utenze',
      path: `/project/${id}/configure-utilities`,
      icon: '🛠️',
      description: 'Configura le utenze caricate'
    },
    {
      title: 'Configura Utenze di Potenza',
      path: `/project/${id}/configure-power`,
      icon: '⚡',
      description: 'Configura le utenze di potenza'
    },
    {
      title: 'Crea Nodi e PLC',
      path: `/project/${id}/create-nodes`,
      icon: '🖧',
      description: 'Crea e gestisci nodi e PLC'
    },
    {
      title: 'Assegna I/O ai Nodi',
      path: `/project/${id}/assign-io`,
      icon: '🔗',
      description: 'Assegna I/O ai moduli dei nodi'
    },
    {
      title: 'Configura Quadro Elettrico',
      path: `/project/${id}/configure-panel`,
      icon: '🗄️',
      description: 'Configura il quadro elettrico'
    }
  ]

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">{project.nome_progetto}</h1>
        <p className="text-gray-600 mb-4">{project.descrizione}</p>
        <p className="text-sm text-gray-500">
          <strong>Data di Creazione:</strong> {new Date(project.data_creazione).toLocaleDateString('it-IT')}
        </p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Opzioni di Configurazione</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {menuItems.map((item) => (
            <button
              key={item.path}
              onClick={() => window.location.href = item.path}
              className="p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:shadow-md transition-all text-left"
            >
              <div className="flex items-center mb-2">
                <span className="text-2xl mr-3">{item.icon}</span>
                <h3 className="font-medium text-gray-900">{item.title}</h3>
              </div>
              <p className="text-sm text-gray-600">{item.description}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default ProjectDetail
