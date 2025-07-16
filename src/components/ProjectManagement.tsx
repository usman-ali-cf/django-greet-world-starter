
import React, { useState, useEffect } from 'react'
import { apiFetch } from '../utils/api'
import DataTable from './DataTable'

interface Project {
  id_prg: number
  nome_progetto: string
  descrizione: string
  data_creazione: string
  url_dettaglio?: string
}

const columnsProgetti = [
  { header: "Nome progetto", field: "nome_progetto" },
  { header: "Descrizione", field: "descrizione" },
  { header: "Azioni", field: "id_prg" }
]

const ProjectManagement: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  const loadProjects = async () => {
    try {
      setLoading(true)
      const data = await apiFetch('/api/projects/')
      // Add url_dettaglio to each project
      const projectsWithUrls = data.map((project: Project) => ({
        ...project,
        url_dettaglio: `/project/${project.id_prg}`
      }))
      setProjects(projectsWithUrls)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Errore nel caricamento dei progetti')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateProject = async (projectData: { nome_progetto: string; descrizione: string }) => {
    try {
      await apiFetch('/api/projects/', {
        method: 'POST',
        body: JSON.stringify(projectData)
      })
      await loadProjects()
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
      await loadProjects()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Errore nell\'eliminazione del progetto')
    }
  }

  const addActionButtons = (projects: Project[]) => {
    const tbody = document.querySelector('#listaProgetti tbody')
    if (!tbody) return

    const rows = tbody.querySelectorAll('tr')
    rows.forEach((row, idx) => {
      const proj = projects[idx]
      if (!proj) return
      
      const td = row.lastElementChild as HTMLTableCellElement

      const btnOpen = document.createElement("button")
      btnOpen.textContent = "Apri"
      btnOpen.className = "btn-apri"
      btnOpen.addEventListener("click", () => {
        window.location.href = proj.url_dettaglio || `/project/${proj.id_prg}`
      })

      const btnDel = document.createElement("button")
      btnDel.textContent = "Elimina"
      btnDel.className = "btn-elimina"
      btnDel.style.marginLeft = "6px"
      btnDel.addEventListener("click", () => handleDeleteProject(proj.id_prg))

      td.style.textAlign = "center"
      td.innerHTML = ""
      td.append(btnOpen, btnDel)
    })
  }

  const handleRowClick = (item: Project, tr: HTMLTableRowElement) => {
    tr.parentNode?.querySelectorAll('tr').forEach(r => r.classList.remove('selected'))
    tr.classList.add('selected')
  }

  useEffect(() => {
    loadProjects()
  }, [])

  if (loading) {
    return <div className="text-center p-8">Caricamento...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header with buttons */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Lista Progetti</h2>
        <div className="space-x-2">
          <button 
            id="btnNuovoProgetto"
            onClick={() => setIsModalOpen(true)}
            className="btn"
          >
            Nuovo Progetto
          </button>
          <button 
            id="btnAggiornaProgetti"
            onClick={loadProjects}
            className="btn"
          >
            Aggiorna
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Projects Table */}
      <div className="listaProgetti">
        <DataTable
          columns={columnsProgetti}
          data={projects}
          onRowClick={handleRowClick}
          postRender={addActionButtons}
          containerSelector="#listaProgetti"
        />
        <table style={{ display: 'none' }}>
          <tbody id="listaProgetti"></tbody>
        </table>
      </div>

      {/* Modal for creating new project */}
      {isModalOpen && (
        <div id="popupNuovoProj" className="popup-overlay" style={{ display: 'flex' }}>
          <div className="popup-content">
            <h3>Nuovo Progetto</h3>
            <form 
              id="formNuovoProgetto"
              onSubmit={(e) => {
                e.preventDefault()
                const formData = new FormData(e.currentTarget)
                const nome = formData.get('nome_progetto') as string
                const desc = formData.get('descrizione_progetto') as string
                if (nome && desc) {
                  handleCreateProject({ nome_progetto: nome, descrizione: desc })
                }
              }}
            >
              <div className="mb-4">
                <label htmlFor="inpNomeProj" className="block text-gray-700 mb-2">Nome Progetto:</label>
                <input
                  type="text"
                  id="inpNomeProj"
                  name="nome_progetto"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div className="mb-4">
                <label htmlFor="txtDescProj" className="block text-gray-700 mb-2">Descrizione:</label>
                <textarea
                  id="txtDescProj"
                  name="descrizione_progetto"
                  required
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                ></textarea>
              </div>
              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  id="btnChiudiPopup"
                  onClick={() => setIsModalOpen(false)}
                  className="btn-cancel"
                >
                  Annulla
                </button>
                <button type="submit" className="btn">
                  Crea Progetto
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
