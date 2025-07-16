
import React, { useState, useEffect } from 'react'
import { apiFetch } from '../utils/api'
import CreateProjectModal from './CreateProjectModal'

interface Project {
  id_prg: number
  nome_progetto: string
  descrizione: string
  data_creazione: string
  utente?: string
}

const ProjectManagement: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  const loadProjects = async () => {
    try {
      setLoading(true)
      const data = await apiFetch('/api/projects/')
      setProjects(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Errore nel caricamento dei progetti')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadProjects()
  }, [])

  const handleCreateProject = async (projectData: { nome_progetto: string; descrizione: string }) => {
    try {
      await apiFetch('/api/projects/', {
        method: 'POST',
        body: JSON.stringify(projectData)
      })
      await loadProjects() // Reload projects
      setIsModalOpen(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Errore nella creazione del progetto')
    }
  }

  const handleDeleteProject = async (projectId: number) => {
    if (!confirm('Sei sicuro di voler eliminare questo progetto?')) {
      return
    }

    try {
      await apiFetch(`/api/projects/${projectId}`, {
        method: 'DELETE'
      })
      await loadProjects() // Reload projects
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Errore nell\'eliminazione del progetto')
    }
  }

  if (loading) {
    return <div className="text-center p-8">Caricamento...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Gestione Progetti</h1>
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
        >
          Nuovo Progetto
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Nome Progetto
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Descrizione
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Data Creazione
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Utente
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Azioni
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {projects.map((project) => (
                <tr key={project.id_prg} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {project.nome_progetto}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900">
                      {project.descrizione}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {new Date(project.data_creazione).toLocaleDateString('it-IT')}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {project.utente || '-'}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <a
                      href={`/project/${project.id_prg}`}
                      className="text-blue-600 hover:text-blue-900"
                    >
                      Visualizza
                    </a>
                    <button
                      onClick={() => handleDeleteProject(project.id_prg)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Elimina
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {isModalOpen && (
        <CreateProjectModal
          onClose={() => setIsModalOpen(false)}
          onCreate={handleCreateProject}
        />
      )}
    </div>
  )
}

export default ProjectManagement
