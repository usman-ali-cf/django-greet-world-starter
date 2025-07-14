import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { apiFetch } from '../utils/api'

interface HardwareItem {
  id_hw: number
  nome_hw: string
  descrizione_hw: string
  tipo: string
  DI: number
  DO: number
  AI: number
  AO: number
  F_DI: number
  F_DO: number
  Ox: number
  Oy: number
  L: number
  H: number
  blocco_grafico?: string
}

interface Node {
  id_nodo: number
  nome_nodo: string
  tipo_nodo: string
  descrizione?: string
  id_prg: number
  id_quadro?: number
}

interface HardwareNode {
  id_nodo_hw: number
  id_nodo: number
  id_hw: number
  slot: number
  quantita: number
  nome_hw: string
  tipo: string
  DI: number
  DO: number
}

export default function CreateNodesPage() {
  const { id } = useParams<{ id: string }>()
  const projectId = parseInt(id || '0')

  // State management
  const [hardwareCatalog, setHardwareCatalog] = useState<HardwareItem[]>([])
  const [nodes, setNodes] = useState<Node[]>([])
  const [selectedNode, setSelectedNode] = useState<number | null>(null)
  const [nodeHardware, setNodeHardware] = useState<HardwareNode[]>([])
  const [selectedHardware, setSelectedHardware] = useState<HardwareItem | null>(null)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [loading, setLoading] = useState(false)

  // Form state for node creation
  const [newNodeName, setNewNodeName] = useState('')
  const [newNodeDescription, setNewNodeDescription] = useState('')

  // Load data on component mount
  useEffect(() => {
    loadHardwareCatalog()
    loadNodes()
  }, [])

  // Load node hardware when selected node changes
  useEffect(() => {
    if (selectedNode) {
      loadNodeHardware(selectedNode)
    }
  }, [selectedNode])

  const loadHardwareCatalog = async () => {
    try {
      const data = await apiFetch('/api/hardware/catalog')
      setHardwareCatalog(data)
    } catch (error) {
      console.error('Error loading hardware catalog:', error)
    }
  }

  const loadNodes = async () => {
    try {
      const data = await apiFetch(`/api/nodes/project/${projectId}`)
      setNodes(data)
      if (data.length > 0 && !selectedNode) {
        setSelectedNode(data[0].id_nodo)
      }
    } catch (error) {
      console.error('Error loading nodes:', error)
    }
  }

  const loadNodeHardware = async (nodeId: number) => {
    try {
      const data = await apiFetch(`/api/hardware/node/${nodeId}`)
      setNodeHardware(data)
    } catch (error) {
      console.error('Error loading node hardware:', error)
    }
  }

  const createNode = async () => {
    if (!newNodeName.trim()) {
      alert('Inserisci un nome per il nodo')
      return
    }

    setLoading(true)
    try {
      const nodeData = {
        nome_nodo: newNodeName,
        descrizione: newNodeDescription,
        id_prg: projectId,
        tipo_nodo: 'PLC'
      }

      await apiFetch('/api/nodes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(nodeData)
      })

      // Reset form and reload data
      setNewNodeName('')
      setNewNodeDescription('')
      setShowCreateModal(false)
      await loadNodes()
    } catch (error) {
      console.error('Error creating node:', error)
      alert('Errore nella creazione del nodo')
    } finally {
      setLoading(false)
    }
  }

  const assignHardwareToNode = async () => {
    if (!selectedNode || !selectedHardware) {
      alert('Seleziona un nodo e un hardware')
      return
    }

    try {
      const assignData = {
        id_nodo: selectedNode,
        id_hw: selectedHardware.id_hw,
        quantita: 1
      }

      await apiFetch('/api/hardware/node', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(assignData)
      })

      // Reload node hardware
      await loadNodeHardware(selectedNode)
      setSelectedHardware(null)
    } catch (error) {
      console.error('Error assigning hardware:', error)
      alert('Errore nell\'assegnazione dell\'hardware')
    }
  }

  const removeHardwareFromNode = async (hardwareNodeId: number) => {
    if (!confirm('Sei sicuro di voler rimuovere questo hardware?')) {
      return
    }

    try {
      await apiFetch(`/api/hardware/node/${hardwareNodeId}`, {
        method: 'DELETE'
      })

      // Reload node hardware
      if (selectedNode) {
        await loadNodeHardware(selectedNode)
      }
    } catch (error) {
      console.error('Error removing hardware:', error)
      alert('Errore nella rimozione dell\'hardware')
    }
  }

  const createAutomaticPLC = async () => {
    try {
      const response = await apiFetch(`/api/nodes/plc/auto/${projectId}`, {
        method: 'POST'
      })

      if (response.message) {
        alert(response.message)
        await loadNodes()
      } else if (response.error) {
        alert('Errore: ' + response.error)
      }
    } catch (error) {
      console.error('Error creating automatic PLC:', error)
      alert('Errore nella creazione automatica del PLC')
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-foreground">Crea Nodi e PLC</h1>
        <div className="flex gap-2">
          <button
            onClick={() => setShowCreateModal(true)}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
          >
            Crea Nuovo Nodo
          </button>
          <button
            onClick={createAutomaticPLC}
            className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md hover:bg-secondary/90 transition-colors"
          >
            Creazione Automatica PLC
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Panel - Hardware Catalog */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-semibold text-foreground">Catalogo Hardware</h2>
            <button
              onClick={loadHardwareCatalog}
              className="px-3 py-1 text-sm bg-muted text-muted-foreground rounded hover:bg-muted/80 transition-colors"
            >
              Aggiorna
            </button>
          </div>
          
          <div className="border border-border rounded-lg overflow-hidden">
            <div className="bg-muted px-4 py-2 font-medium text-muted-foreground text-sm">
              <div className="grid grid-cols-2 gap-4">
                <span>Nome HW</span>
                <span>Descrizione</span>
              </div>
            </div>
            <div className="max-h-96 overflow-y-auto">
              {hardwareCatalog.map((hw) => (
                <div
                  key={hw.id_hw}
                  className={`px-4 py-2 cursor-pointer border-b border-border hover:bg-muted/50 transition-colors ${
                    selectedHardware?.id_hw === hw.id_hw ? 'bg-primary/10 border-primary' : ''
                  }`}
                  onClick={() => setSelectedHardware(hw)}
                >
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <span className="font-medium text-foreground">{hw.nome_hw}</span>
                    <span className="text-muted-foreground">{hw.descrizione_hw}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Panel - Node Management */}
        <div className="space-y-4">
          {/* Node Selection */}
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Seleziona Nodo
            </label>
            <select
              value={selectedNode || ''}
              onChange={(e) => setSelectedNode(Number(e.target.value))}
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

          {/* Assign Hardware Button */}
          <button
            onClick={assignHardwareToNode}
            disabled={!selectedNode || !selectedHardware}
            className="w-full px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Assegna Hardware al Nodo
          </button>

          {/* Assigned Hardware */}
          <div>
            <h3 className="text-md font-semibold text-foreground mb-2">Hardware Assegnato</h3>
            <div className="border border-border rounded-lg overflow-hidden">
              <div className="bg-muted px-4 py-2 font-medium text-muted-foreground text-sm">
                <div className="grid grid-cols-4 gap-2">
                  <span>Nome HW</span>
                  <span>Slot</span>
                  <span>DI</span>
                  <span>DO</span>
                </div>
              </div>
              <div className="max-h-64 overflow-y-auto">
                {nodeHardware.map((hw) => (
                  <div
                    key={hw.id_nodo_hw}
                    className="px-4 py-2 border-b border-border hover:bg-muted/50 transition-colors"
                  >
                    <div className="grid grid-cols-4 gap-2 text-sm items-center">
                      <span className="font-medium text-foreground">{hw.nome_hw}</span>
                      <span className="text-muted-foreground">{hw.slot}</span>
                      <span className="text-muted-foreground">{hw.DI}</span>
                      <span className="text-muted-foreground">{hw.DO}</span>
                    </div>
                    <button
                      onClick={() => removeHardwareFromNode(hw.id_nodo_hw)}
                      className="mt-1 px-2 py-1 text-xs bg-destructive text-destructive-foreground rounded hover:bg-destructive/90 transition-colors"
                    >
                      Elimina
                    </button>
                  </div>
                ))}
                {nodeHardware.length === 0 && (
                  <div className="px-4 py-8 text-center text-muted-foreground">
                    Nessun hardware assegnato
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Create Node Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-card border border-border rounded-lg shadow-lg w-full max-w-md mx-4">
            <div className="px-6 py-4 border-b border-border">
              <h3 className="text-lg font-semibold text-card-foreground">Crea Nuovo Nodo</h3>
            </div>
            <div className="px-6 py-4 space-y-4">
              <div>
                <label className="block text-sm font-medium text-card-foreground mb-2">
                  Nome Nodo *
                </label>
                <input
                  type="text"
                  value={newNodeName}
                  onChange={(e) => setNewNodeName(e.target.value)}
                  className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="Inserisci nome nodo"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-card-foreground mb-2">
                  Descrizione
                </label>
                <textarea
                  value={newNodeDescription}
                  onChange={(e) => setNewNodeDescription(e.target.value)}
                  className="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                  rows={3}
                  placeholder="Inserisci descrizione (opzionale)"
                />
              </div>
            </div>
            <div className="px-6 py-4 border-t border-border flex justify-end gap-2">
              <button
                onClick={() => setShowCreateModal(false)}
                className="px-4 py-2 text-sm border border-border rounded-md hover:bg-muted transition-colors"
              >
                Annulla
              </button>
              <button
                onClick={createNode}
                disabled={loading || !newNodeName.trim()}
                className="px-4 py-2 text-sm bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? 'Creazione...' : 'Crea Nodo'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}