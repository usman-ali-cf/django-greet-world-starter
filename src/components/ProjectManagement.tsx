
import React, { useState, useEffect } from 'react'
import { apiFetch } from '../utils/api'

interface Project {
  id_prg: number
  nome_progetto: string
  descrizione: string
  data_creazione: string
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

  const handleOpenProject = (projectId: number) => {
    window.location.href = `/project/${projectId}`
  }

  useEffect(() => {
    loadProjects()
  }, [])

  return (
    <div className="container">
      <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '30px', color: '#333' }}>
        Gestione Progetto
      </h1>

      {/* Action Buttons */}
      <div style={{ marginBottom: '30px' }}>
        <button
          onClick={() => setIsModalOpen(true)}
          className="btn"
          style={{ marginRight: '15px' }}
        >
          + Nuovo Progetto
        </button>
        <button
          onClick={loadProjects}
          className="btn"
        >
          Aggiorna Lista
        </button>
      </div>

      {error && (
        <div className="alert alert-danger" style={{ 
          backgroundColor: '#f8d7da', 
          border: '1px solid #f5c6cb', 
          color: '#721c24', 
          padding: '12px', 
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          {error}
        </div>
      )}

      {/* Section Title */}
      <h2 style={{ fontSize: '20px', fontWeight: 'normal', marginBottom: '20px', color: '#333' }}>
        Seleziona un progetto o creane uno nuovo
      </h2>

      <h3 style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '15px', color: '#333' }}>
        Progetti disponibili
      </h3>

      {/* Projects Table */}
      <div className="listaProgetti" style={{ backgroundColor: '#f9f9f9', padding: '20px', borderRadius: '8px', border: '1px solid #ccc' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#032952', color: 'white' }}>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>
                Nome progetto
              </th>
              <th style={{ padding: '12px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>
                Descrizione
              </th>
              <th style={{ padding: '12px', textAlign: 'center', borderBottom: '1px solid #ddd' }}>
                Azioni
              </th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={3} style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
                  Caricamento...
                </td>
              </tr>
            ) : projects.length === 0 ? (
              <tr>
                <td colSpan={3} style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
                  Nessun progetto trovato. Crea un nuovo progetto per iniziare.
                </td>
              </tr>
            ) : (
              projects.map((project) => (
                <tr 
                  key={project.id_prg} 
                  style={{ 
                    cursor: 'pointer',
                    transition: 'background-color 0.3s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = '#f1f1f1'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = 'transparent'
                  }}
                >
                  <td style={{ padding: '12px', borderBottom: '1px solid #ddd' }}>
                    {project.nome_progetto}
                  </td>
                  <td style={{ padding: '12px', borderBottom: '1px solid #ddd' }}>
                    {project.descrizione}
                  </td>
                  <td style={{ padding: '12px', borderBottom: '1px solid #ddd', textAlign: 'center' }}>
                    <button
                      onClick={() => handleOpenProject(project.id_prg)}
                      className="btn"
                      style={{ 
                        marginRight: '6px',
                        fontSize: '14px',
                        padding: '6px 12px'
                      }}
                    >
                      Apri
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleDeleteProject(project.id_prg)
                      }}
                      className="btn"
                      style={{ 
                        fontSize: '14px',
                        padding: '6px 12px'
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
      </div>

      {/* Modal for creating new project */}
      {isModalOpen && (
        <div className="popup-overlay" style={{ display: 'flex' }}>
          <div className="popup-content">
            <h3 style={{ marginBottom: '20px', fontSize: '20px', fontWeight: 'bold' }}>Nuovo Progetto</h3>
            <form 
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
              <div style={{ marginBottom: '15px' }}>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                  Nome Progetto:
                </label>
                <input
                  type="text"
                  name="nome_progetto"
                  required
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #ccc',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>
              <div style={{ marginBottom: '20px' }}>
                <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                  Descrizione:
                </label>
                <textarea
                  name="descrizione_progetto"
                  required
                  rows={3}
                  style={{
                    width: '100%',
                    padding: '8px',
                    border: '1px solid #ccc',
                    borderRadius: '4px',
                    fontSize: '14px',
                    resize: 'vertical'
                  }}
                ></textarea>
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
                <button
                  type="button"
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
