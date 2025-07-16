
import React, { useState, useEffect } from 'react'
import { apiFetch } from '../utils/api'

interface Project {
  id_prg: number
  nome_progetto: string
  descrizione_progetto: string
  data_creazione: string
  url_dettaglio: string
}

const ProjectManagement: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(false)
  const [showCreateForm, setShowCreateForm] = useState(false)
  const [formData, setFormData] = useState({
    nome_progetto: '',
    descrizione_progetto: ''
  })

  const loadProjects = async () => {
    try {
      setLoading(true)
      const data = await apiFetch('/api/progetti')
      setProjects(data)
    } catch (error) {
      console.error('Error loading projects:', error)
    } finally {
      setLoading(false)
    }
  }

  const createProject = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await apiFetch('/api/progetti', {
        method: 'POST',
        body: JSON.stringify(formData)
      })
      setShowCreateForm(false)
      setFormData({ nome_progetto: '', descrizione_progetto: '' })
      loadProjects()
    } catch (error) {
      console.error('Error creating project:', error)
    }
  }

  const deleteProject = async (id: number, nome: string) => {
    if (!confirm(`Eliminare il progetto «${nome}»?`)) return
    try {
      await apiFetch(`/api/progetti/${id}`, { method: 'DELETE' })
      loadProjects()
    } catch (error) {
      console.error('Error deleting project:', error)
    }
  }

  useEffect(() => {
    loadProjects()
  }, [])

  if (loading) {
    return <div className="text-center p-8">Caricamento...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Gestione Progetto</h1>
        <div className="space-x-2">
          <button
            onClick={() => setShowCreateForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            + Nuovo Progetto
          </button>
          <button
            onClick={loadProjects}
            className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
          >
            Aggiorna Lista
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Nome progetto
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Descrizione
              </th>
              <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Azioni
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {projects.map((project) => (
              <tr key={project.id_prg} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {project.nome_progetto}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {project.descrizione_progetto}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-center space-x-2">
                  <button
                    onClick={() => window.location.href = `/project/${project.id_prg}`}
                    className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700"
                  >
                    Apri
                  </button>
                  <button
                    onClick={() => deleteProject(project.id_prg, project.nome_progetto)}
                    className="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700"
                  >
                    Elimina
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Create Project Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold mb-4">Crea Nuovo Progetto</h3>
            <form onSubmit={createProject} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nome progetto
                </label>
                <input
                  type="text"
                  value={formData.nome_progetto}
                  onChange={(e) => setFormData({ ...formData, nome_progetto: e.target.value })}
                  required
                  className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Descrizione
                </label>
                <textarea
                  value={formData.descrizione_progetto}
                  onChange={(e) => setFormData({ ...formData, descrizione_progetto: e.target.value })}
                  required
                  rows={3}
                  className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
                >
                  Annulla
                </button>
                <button
                  type="submit"
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  Salva
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProjectManagement
