import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiFetch } from '../utils/api'
import CreateProjectModal from './CreateProjectModal'
// Use static path for now - will work with the existing Flask static files

interface Project {
  id_prg: number
  nome: string
  descrizione: string
  url_dettaglio: string
}

export default function ProjectManagement() {
  const [projects, setProjects] = useState<Project[]>([])
  const [selectedRow, setSelectedRow] = useState<HTMLTableRowElement | null>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

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

  const deleteProject = async (id: number, name: string) => {
    if (!confirm(`Eliminare il progetto «${name}»?`)) return
    
    try {
      await apiFetch(`/api/progetti/${id}`, { method: 'DELETE' })
      await loadProjects()
    } catch (error) {
      console.error('Error deleting project:', error)
    }
  }

  const handleRowClick = (event: React.MouseEvent<HTMLTableRowElement>) => {
    // Remove selection from all rows
    document.querySelectorAll('#listaProgetti tr').forEach(row => {
      row.classList.remove('selected')
    })
    
    // Select current row
    const row = event.currentTarget
    row.classList.add('selected')
    setSelectedRow(row)
  }

  const openProject = (project: Project) => {
    // Navigate to project detail page
    navigate(`/project/${project.id_prg}`)
  }

  useEffect(() => {
    loadProjects()
  }, [])

  return (
    <>
      <header className="mb-8">
        <h1 className="text-2xl font-bold mb-4">Gestione Progetto</h1>

        <nav className="mb-4">
          <ul className="nav-buttons flex gap-4 list-none">
            <li>
              <button 
                className="btn bg-[#ca0909] text-white border-none px-5 py-3 cursor-pointer rounded text-base transition-colors hover:bg-[#850404]"
                onClick={() => setShowCreateModal(true)}
              >
                + Nuovo Progetto
              </button>
            </li>
            <li>
              <button 
                className="btn bg-[#ca0909] text-white border-none px-5 py-3 cursor-pointer rounded text-base transition-colors hover:bg-[#850404]"
                onClick={loadProjects}
              >
                Aggiorna Lista
              </button>
            </li>
          </ul>
        </nav>

        <img 
          className="logo-app w-[250px] h-auto"
          src="/static/img/Logo.png"
          alt="Logo"
        />
      </header>

      <main>
        <h2 className="text-xl mb-6">Seleziona un progetto o creane uno nuovo</h2>

        <section>
          <h3 className="text-lg mb-4">Progetti disponibili</h3>

          <table className="table w-full border-collapse text-sm">
            <thead>
              <tr>
                <th className="sticky top-0 bg-[#032952] text-white z-10 p-3 text-left border-b border-gray-300">
                  Nome progetto
                </th>
                <th className="sticky top-0 bg-[#032952] text-white z-10 p-3 text-left border-b border-gray-300">
                  Descrizione
                </th>
                <th className="sticky top-0 bg-[#032952] text-white z-10 p-3 text-center border-b border-gray-300">
                  Azioni
                </th>
              </tr>
            </thead>
            <tbody id="listaProgetti">
              {loading ? (
                <tr>
                  <td colSpan={3} className="p-3 text-center">
                    Caricamento progetti...
                  </td>
                </tr>
              ) : projects.length === 0 ? (
                <tr>
                  <td colSpan={3} className="p-3 text-center">
                    Nessun progetto disponibile
                  </td>
                </tr>
              ) : (
                projects.map((project) => (
                  <tr 
                    key={project.id_prg}
                    className="cursor-pointer transition-colors hover:bg-gray-100"
                    onClick={handleRowClick}
                  >
                    <td className="p-3 border-b border-gray-300 whitespace-nowrap">
                      {project.nome}
                    </td>
                    <td className="p-3 border-b border-gray-300 whitespace-nowrap">
                      {project.descrizione}
                    </td>
                    <td className="p-3 border-b border-gray-300 text-center">
                      <button
                        className="btn-apri bg-[#ca0909] text-white border-none px-4 py-2 cursor-pointer rounded text-sm transition-colors hover:bg-[#850404] mr-2"
                        onClick={(e) => {
                          e.stopPropagation()
                          openProject(project)
                        }}
                      >
                        Apri
                      </button>
                      <button
                        className="btn-elimina bg-[#ca0909] text-white border-none px-4 py-2 cursor-pointer rounded text-sm transition-colors hover:bg-[#850404]"
                        onClick={(e) => {
                          e.stopPropagation()
                          deleteProject(project.id_prg, project.nome)
                        }}
                      >
                        Elimina
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </section>
      </main>

      <CreateProjectModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onProjectCreated={loadProjects}
      />
    </>
  )
}