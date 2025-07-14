import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { apiFetch } from '../utils/api'

interface Node {
  id_nodo: number
  nome_nodo: string
  tipo_nodo: string
}

interface Module {
  id_nodo_hw: number
  id_nodo: number
  id_hw: number
  slot: number
  nome_hw: string
  tipo: string
}

interface IOItem {
  id_io: number
  codice: string
  descrizione: string
  tipo: string
  id_modulo?: number
  indirizzo?: string
  note?: string
  id_prg: number
}

export default function AssignIOPage() {
  const { id } = useParams<{ id: string }>()
  const projectId = parseInt(id || '0')

  // State management
  const [nodes, setNodes] = useState<Node[]>([])
  const [modules, setModules] = useState<Module[]>([])
  const [unassignedIO, setUnassignedIO] = useState<IOItem[]>([])
  const [assignedIO, setAssignedIO] = useState<IOItem[]>([])
  
  const [selectedNode, setSelectedNode] = useState<number | null>(null)
  const [selectedModule, setSelectedModule] = useState<number | null>(null)
  const [selectedModuleType, setSelectedModuleType] = useState<string>('')
  
  const [selectedUnassignedIds, setSelectedUnassignedIds] = useState<Set<number>>(new Set())
  const [selectedAssignedIds, setSelectedAssignedIds] = useState<Set<number>>(new Set())
  
  const [unassignedFilter, setUnassignedFilter] = useState('')
  const [assignedFilter, setAssignedFilter] = useState('')
  
  const [loading, setLoading] = useState(false)

  // Load nodes on component mount
  useEffect(() => {
    loadNodes()
  }, [])

  // Load modules when node changes
  useEffect(() => {
    if (selectedNode) {
      loadModules(selectedNode)
    } else {
      setModules([])
      setUnassignedIO([])
      setAssignedIO([])
    }
  }, [selectedNode])

  // Load IO when module changes
  useEffect(() => {
    if (selectedModule && selectedModuleType) {
      loadUnassignedIO()
      loadAssignedIO(selectedModule, selectedNode!)
    } else {
      setUnassignedIO([])
      setAssignedIO([])
    }
  }, [selectedModule, selectedModuleType])

  const loadNodes = async () => {
    try {
      const data = await apiFetch(`/api/nodes/project/${projectId}`)
      setNodes(data)
      if (data.length > 0) {
        setSelectedNode(data[0].id_nodo)
      }
    } catch (error) {
      console.error('Error loading nodes:', error)
    }
  }

  const loadModules = async (nodeId: number) => {
    try {
      const data = await apiFetch(`/api/hardware/node/${nodeId}`)
      setModules(data)
      setSelectedModule(null)
      setSelectedModuleType('')
    } catch (error) {
      console.error('Error loading modules:', error)
    }
  }

  const loadUnassignedIO = async () => {
    try {
      const data = await apiFetch(`/api/io/unassigned?project_id=${projectId}&tipo=${encodeURIComponent(selectedModuleType)}`)
      setUnassignedIO(data)
    } catch (error) {
      console.error('Error loading unassigned IO:', error)
    }
  }

  const loadAssignedIO = async (moduleId: number, nodeId: number) => {
    try {
      const data = await apiFetch(`/api/io/assigned?module_id=${moduleId}&node_id=${nodeId}`)
      setAssignedIO(data)
    } catch (error) {
      console.error('Error loading assigned IO:', error)
    }
  }

  const handleModuleSelect = (module: Module) => {
    setSelectedModule(module.id_nodo_hw)
    setSelectedModuleType(module.tipo)
    setSelectedUnassignedIds(new Set())
    setSelectedAssignedIds(new Set())
  }

  const toggleUnassignedSelection = (ioId: number) => {
    const newSelection = new Set(selectedUnassignedIds)
    if (newSelection.has(ioId)) {
      newSelection.delete(ioId)
    } else {
      newSelection.add(ioId)
    }
    setSelectedUnassignedIds(newSelection)
  }

  const toggleAssignedSelection = (ioId: number) => {
    const newSelection = new Set(selectedAssignedIds)
    if (newSelection.has(ioId)) {
      newSelection.delete(ioId)
    } else {
      newSelection.add(ioId)
    }
    setSelectedAssignedIds(newSelection)
  }

  const selectAllUnassigned = (select: boolean) => {
    if (select) {
      const filteredIds = filteredUnassignedIO.map(io => io.id_io)
      setSelectedUnassignedIds(new Set(filteredIds))
    } else {
      setSelectedUnassignedIds(new Set())
    }
  }

  const selectAllAssigned = (select: boolean) => {
    if (select) {
      const filteredIds = filteredAssignedIO.map(io => io.id_io)
      setSelectedAssignedIds(new Set(filteredIds))
    } else {
      setSelectedAssignedIds(new Set())
    }
  }

  const assignIO = async () => {
    if (!selectedModule || selectedUnassignedIds.size === 0) {
      alert('Seleziona un modulo e almeno un I/O non assegnato')
      return
    }

    setLoading(true)
    try {
      for (const ioId of selectedUnassignedIds) {
        const assignData = {
          id_io: ioId,
          id_modulo: selectedModule
        }

        const response = await apiFetch('/api/io/assign', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(assignData)
        })

        if (response.error) {
          alert('Operazione non consentita: ' + response.error)
          return
        }
      }

      // Refresh data
      await loadUnassignedIO()
      await loadAssignedIO(selectedModule, selectedNode!)
      setSelectedUnassignedIds(new Set())
    } catch (error) {
      console.error('Error assigning IO:', error)
      alert('Errore nell\'assegnazione I/O')
    } finally {
      setLoading(false)
    }
  }

  const unassignIO = async () => {
    if (selectedAssignedIds.size === 0) {
      alert('Seleziona almeno un I/O assegnato da rimuovere')
      return
    }

    setLoading(true)
    try {
      for (const ioId of selectedAssignedIds) {
        await apiFetch(`/api/io/assign/${ioId}`, {
          method: 'DELETE'
        })
      }

      // Refresh data
      await loadUnassignedIO()
      await loadAssignedIO(selectedModule!, selectedNode!)
      setSelectedAssignedIds(new Set())
    } catch (error) {
      console.error('Error unassigning IO:', error)
      alert('Errore nella rimozione I/O')
    } finally {
      setLoading(false)
    }
  }

  const autoAssignIO = async () => {
    if (!selectedNode) {
      alert('Seleziona un nodo')
      return
    }

    try {
      const response = await apiFetch(`/api/io/assign/auto?node_id=${selectedNode}&project_id=${projectId}`, {
        method: 'POST'
      })

      if (response.success) {
        alert(response.message)
        await loadUnassignedIO()
        if (selectedModule) {
          await loadAssignedIO(selectedModule, selectedNode)
        }
      } else {
        alert('Errore: ' + response.message)
      }
    } catch (error) {
      console.error('Error in auto assignment:', error)
      alert('Errore nell\'assegnazione automatica')
    }
  }

  // Filter functions
  const filteredUnassignedIO = unassignedIO.filter(io =>
    io.descrizione.toLowerCase().includes(unassignedFilter.toLowerCase())
  )

  const filteredAssignedIO = assignedIO.filter(io =>
    io.descrizione.toLowerCase().includes(assignedFilter.toLowerCase())
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-foreground">Assegna I/O ai Nodi</h1>
        <button
          onClick={autoAssignIO}
          className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md hover:bg-secondary/90 transition-colors"
        >
          Assegnazione Automatica
        </button>
      </div>

      {/* Node and Module Selection */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            Seleziona Nodo
          </label>
          <select
            value={selectedNode || ''}
            onChange={(e) => setSelectedNode(Number(e.target.value) || null)}
            className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
          >
            <option value="">Seleziona un nodo...</option>
            {nodes.map((node) => (
              <option key={node.id_nodo} value={node.id_nodo}>
                {node.nome_nodo}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-foreground mb-2">
            Moduli Hardware
          </label>
          <div className="border border-border rounded-lg max-h-32 overflow-y-auto">
            {modules.map((module) => (
              <div
                key={module.id_nodo_hw}
                className={`px-3 py-2 cursor-pointer border-b border-border hover:bg-muted/50 transition-colors ${
                  selectedModule === module.id_nodo_hw ? 'bg-primary/10 border-primary' : ''
                }`}
                onClick={() => handleModuleSelect(module)}
              >
                <div className="grid grid-cols-3 gap-2 text-sm">
                  <span className="font-medium text-foreground">Slot {module.slot}</span>
                  <span className="text-muted-foreground">{module.nome_hw}</span>
                  <span className="text-muted-foreground">{module.tipo}</span>
                </div>
              </div>
            ))}
            {modules.length === 0 && selectedNode && (
              <div className="px-3 py-4 text-center text-muted-foreground text-sm">
                Nessun modulo disponibile per questo nodo
              </div>
            )}
          </div>
        </div>
      </div>

      {/* IO Management */}
      {selectedModule && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Unassigned IO */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold text-foreground">I/O Non Assegnati</h3>
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  onChange={(e) => selectAllUnassigned(e.target.checked)}
                  className="rounded border-border"
                />
                <span className="text-sm text-muted-foreground">Seleziona tutti</span>
              </div>
            </div>
            
            <input
              type="text"
              placeholder="Filtra per descrizione..."
              value={unassignedFilter}
              onChange={(e) => setUnassignedFilter(e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />

            <div className="border border-border rounded-lg overflow-hidden">
              <div className="bg-muted px-4 py-2 font-medium text-muted-foreground text-sm">
                <div className="grid grid-cols-3 gap-4">
                  <span>Selezione</span>
                  <span>Commento I/O</span>
                  <span>Tipo</span>
                </div>
              </div>
              <div className="max-h-96 overflow-y-auto">
                {filteredUnassignedIO.map((io) => (
                  <div
                    key={io.id_io}
                    className={`px-4 py-2 border-b border-border hover:bg-muted/50 transition-colors ${
                      selectedUnassignedIds.has(io.id_io) ? 'bg-primary/10' : ''
                    }`}
                  >
                    <div className="grid grid-cols-3 gap-4 text-sm items-center">
                      <input
                        type="checkbox"
                        checked={selectedUnassignedIds.has(io.id_io)}
                        onChange={() => toggleUnassignedSelection(io.id_io)}
                        className="rounded border-border"
                      />
                      <span className="text-foreground">{io.descrizione}</span>
                      <span className="text-muted-foreground">{io.tipo}</span>
                    </div>
                  </div>
                ))}
                {filteredUnassignedIO.length === 0 && (
                  <div className="px-4 py-8 text-center text-muted-foreground">
                    Nessun I/O non assegnato
                  </div>
                )}
              </div>
            </div>

            <button
              onClick={assignIO}
              disabled={loading || selectedUnassignedIds.size === 0}
              className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Assegnazione...' : 'Assegna I/O →'}
            </button>
          </div>

          {/* Assigned IO */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold text-foreground">I/O Assegnati</h3>
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  onChange={(e) => selectAllAssigned(e.target.checked)}
                  className="rounded border-border"
                />
                <span className="text-sm text-muted-foreground">Seleziona tutti</span>
              </div>
            </div>

            <input
              type="text"
              placeholder="Filtra per descrizione..."
              value={assignedFilter}
              onChange={(e) => setAssignedFilter(e.target.value)}
              className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />

            <div className="border border-border rounded-lg overflow-hidden">
              <div className="bg-muted px-4 py-2 font-medium text-muted-foreground text-sm">
                <div className="grid grid-cols-3 gap-4">
                  <span>Selezione</span>
                  <span>Commento I/O</span>
                  <span>Tipo</span>
                </div>
              </div>
              <div className="max-h-96 overflow-y-auto">
                {filteredAssignedIO.map((io) => (
                  <div
                    key={io.id_io}
                    className={`px-4 py-2 border-b border-border hover:bg-muted/50 transition-colors ${
                      selectedAssignedIds.has(io.id_io) ? 'bg-primary/10' : ''
                    }`}
                  >
                    <div className="grid grid-cols-3 gap-4 text-sm items-center">
                      <input
                        type="checkbox"
                        checked={selectedAssignedIds.has(io.id_io)}
                        onChange={() => toggleAssignedSelection(io.id_io)}
                        className="rounded border-border"
                      />
                      <span className="text-foreground">{io.descrizione}</span>
                      <span className="text-muted-foreground">{io.tipo}</span>
                    </div>
                  </div>
                ))}
                {filteredAssignedIO.length === 0 && (
                  <div className="px-4 py-8 text-center text-muted-foreground">
                    Nessun I/O assegnato a questo modulo
                  </div>
                )}
              </div>
            </div>

            <button
              onClick={unassignIO}
              disabled={loading || selectedAssignedIds.size === 0}
              className="w-full px-4 py-2 bg-destructive text-destructive-foreground rounded-md hover:bg-destructive/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? 'Rimozione...' : '← Rimuovi I/O'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}