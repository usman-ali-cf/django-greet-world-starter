import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { Link } from 'react-router-dom'
import { apiFetch } from '../utils/api'

interface Project {
  id_prg: number
  nome_progetto: string
  descrizione: string
  data_creazione: string
}

export default function ProjectDetail() {
  const { id } = useParams<{ id: string }>()
  const [project, setProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadProject = async () => {
      if (!id) return
      
      try {
        setLoading(true)
        const data = await apiFetch(`/api/progetti/${id}`)
        setProject(data)
      } catch (error) {
        console.error('Error loading project:', error)
      } finally {
        setLoading(false)
      }
    }

    loadProject()
  }, [id])

  if (loading) {
    return <div className="text-center py-8">Caricamento progetto...</div>
  }

  if (!project) {
    return <div className="text-center py-8">Progetto non trovato</div>
  }

  return (
    <main>
      <h2 className="text-2xl font-bold mb-4">{project.nome_progetto}</h2>
      <p className="mb-2"><strong>Descrizione:</strong> {project.descrizione}</p>
      <p className="mb-6"><strong>Data di Creazione:</strong> {project.data_creazione}</p>
      
      <section>
        <h3 className="text-xl font-semibold mb-4">Opzioni di Configurazione</h3>
        <ul className="space-y-3">
          <li>
            <Link 
              to={`/project/${project.id_prg}/upload-utilities`}
              className="inline-block text-blue-600 hover:text-blue-800 underline"
            >
              Carica File Utenze
            </Link>
          </li>
          <li>
            <Link 
              to={`/project/${project.id_prg}/configure-utilities`}
              className="inline-block text-blue-600 hover:text-blue-800 underline"
            >
              Configura Utenze
            </Link>
          </li>
          <li>
            <Link 
              to={`/project/${project.id_prg}/configure-power`}
              className="inline-block text-blue-600 hover:text-blue-800 underline"
            >
              Configura Utenze di Potenza
            </Link>
          </li>
          <li>
            <Link 
              to={`/project/${project.id_prg}/create-nodes`}
              className="inline-block text-blue-600 hover:text-blue-800 underline"
            >
              Crea Nodi e PLC
            </Link>
          </li>
          <li>
            <Link 
              to={`/project/${project.id_prg}/assign-io`}
              className="inline-block text-blue-600 hover:text-blue-800 underline"
            >
              Assegna I/O ai Nodi
            </Link>
          </li>
          <li>
            <Link 
              to={`/project/${project.id_prg}/configure-panel`}
              className="inline-block text-blue-600 hover:text-blue-800 underline"
            >
              Crea Quadro Elettrico
            </Link>
          </li>
        </ul>
      </section>
    </main>
  )
}