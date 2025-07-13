import { useState, useEffect } from 'react'
import { apiFetch } from '../utils/api'

interface CreateProjectModalProps {
  isOpen: boolean
  onClose: () => void
  onProjectCreated: () => void
}

export default function CreateProjectModal({ isOpen, onClose, onProjectCreated }: CreateProjectModalProps) {
  const [projectName, setProjectName] = useState('')
  const [projectDescription, setProjectDescription] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const name = projectName.trim()
    const description = projectDescription.trim()
    
    if (!name || !description) return

    try {
      setIsSubmitting(true)
      await apiFetch('/api/progetti', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nome_progetto: name,
          descrizione_progetto: description
        })
      })
      
      // Reset form and close modal
      setProjectName('')
      setProjectDescription('')
      onClose()
      onProjectCreated()
    } catch (error) {
      console.error('Error creating project:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleClose = () => {
    setProjectName('')
    setProjectDescription('')
    onClose()
  }

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        handleClose()
      }
    }

    document.addEventListener('keyup', handleEscape)
    return () => document.removeEventListener('keyup', handleEscape)
  }, [isOpen])

  useEffect(() => {
    if (isOpen) {
      // Focus on the name input when modal opens
      setTimeout(() => {
        const nameInput = document.getElementById('projectName')
        nameInput?.focus()
      }, 100)
    }
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div className="popup-overlay fixed top-0 left-0 w-screen h-screen bg-black/50 flex items-center justify-center z-[9999]">
      <div className="popup-content bg-white p-5 rounded-lg w-[400px] max-w-[90%] shadow-xl">
        <h4 className="text-lg font-bold mb-4">Crea Nuovo Progetto</h4>
        
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="projectName" className="block mb-2 font-medium">
              Nome progetto
            </label>
            <input
              id="projectName"
              type="text"
              required
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
              disabled={isSubmitting}
            />
          </div>

          <div className="mb-6">
            <label htmlFor="projectDescription" className="block mb-2 font-medium">
              Descrizione
            </label>
            <textarea
              id="projectDescription"
              rows={3}
              required
              value={projectDescription}
              onChange={(e) => setProjectDescription(e.target.value)}
              className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:border-blue-500 resize-vertical"
              disabled={isSubmitting}
            />
          </div>

          <div className="flex justify-end gap-3">
            <button
              type="button"
              className="btn-cancel bg-gray-500 text-white border-none px-5 py-3 cursor-pointer rounded text-base transition-colors hover:bg-gray-600"
              onClick={handleClose}
              disabled={isSubmitting}
            >
              Annulla
            </button>
            <button
              type="submit"
              className="btn bg-[#ca0909] text-white border-none px-5 py-3 cursor-pointer rounded text-base transition-colors hover:bg-[#850404] disabled:opacity-50"
              disabled={isSubmitting}
            >
              {isSubmitting ? 'Salvataggio...' : 'Salva'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}