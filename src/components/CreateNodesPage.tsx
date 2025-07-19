
import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { apiFetch } from '../utils/api'
import DataTable from './DataTable'
import './CreateNodesPage.css';

interface Hardware {
  id_hw: number
  nome_hw: string
  descrizione_hw: string
}

interface Node {
  id_nodo: number
  nome_nodo: string
  descrizione?: string
}

interface NodeHardware {
  id_nodo_hw: number
  nome_hw: string
  slot: number
  DI: number
  DO: number
}

const columnsCatalogoHW = [
  { header: "Nome HW", field: "nome_hw" },
  { header: "Descrizione", field: "descrizione_hw" }
]

const columnsHWAssegnato = [
  { header: "Nome HW", field: "nome_hw" },
  { header: "Slot", field: "slot" },
  { header: "DI", field: "DI" },
  { header: "DO", field: "DO" },
  { header: "Azioni", field: "id_nodo_hw" }
]

const CreateNodesPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const [hardware, setHardware] = useState<Hardware[]>([])
  const [nodes, setNodes] = useState<Node[]>([])
  const [nodeHardware, setNodeHardware] = useState<NodeHardware[]>([])
  const [selectedHW, setSelectedHW] = useState<Hardware | null>(null)
  const [selectedNodo, setSelectedNodo] = useState<string>('')
  const [loading, setLoading] = useState(true)
  const [assigning, setAssigning] = useState(false)
  const [autoPlcLoading, setAutoPlcLoading] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [hardwareToDelete, setHardwareToDelete] = useState<NodeHardware | null>(null)

  // Fetch nodes
  const loadNodi = async () => {
    try {
      const nodi = await apiFetch(`/api/lista_nodi?id_prg=${id}`)
      setNodes(nodi)
      if (nodi.length > 0) {
        setSelectedNodo(nodi[0].id_nodo.toString())
        await loadHWAssegnato(nodi[0].id_nodo)
      }
    } catch (error) {
      setNodes([])
    }
  }

  // Fetch hardware catalog
  const loadCatalogoHW = async () => {
    try {
      const data = await apiFetch('/api/catalogo_hw')
      setHardware(data)
    } catch (error) {
      setHardware([])
    }
  }

  // Fetch hardware assigned to node
  const loadHWAssegnato = async (idNodo: number) => {
    try {
      const data = await apiFetch(`/api/hw_nodo_list?id_nodo=${idNodo}`)
      setNodeHardware(data)
    } catch (error) {
      setNodeHardware([])
    }
  }

  // Assign hardware to node
  const assegnaHardwareAlNodo = async () => {
    if (!selectedNodo || !selectedHW) return
    setAssigning(true)
    try {
      await apiFetch('/api/hw_nodo_add', {
        method: 'POST',
        body: JSON.stringify({ 
          id_nodo: parseInt(selectedNodo), 
          id_hw: selectedHW.id_hw,
          id_prg: parseInt(id || '0')
        })
      })
      await loadHWAssegnato(parseInt(selectedNodo))
    } finally {
      setAssigning(false)
    }
  }

  // Delete hardware from node
  const eliminaHWAssegnato = async (hardware: NodeHardware) => {
    setHardwareToDelete(hardware)
    setShowDeleteModal(true)
  }

  // Confirm hardware deletion
  const confirmDelete = async () => {
    if (!hardwareToDelete) return
    try {
      await apiFetch(`/api/hw_nodo_list/${hardwareToDelete.id_nodo_hw}`, { method: 'DELETE' })
      await loadHWAssegnato(parseInt(selectedNodo))
    } finally {
      setShowDeleteModal(false)
      setHardwareToDelete(null)
    }
  }

  // Cancel hardware deletion
  const cancelDelete = () => {
    setShowDeleteModal(false)
    setHardwareToDelete(null)
  }

  // Automatic PLC creation
  const creaPlcAutomatico = async () => {
    setAutoPlcLoading(true)
    try {
      const response = await apiFetch('/api/crea_plc_automatico', {
        method: 'POST',
        body: JSON.stringify({ id_prg: parseInt(id || '0') })
      })
      if (response.message) {
        alert(response.message)
      }
      await loadNodi()
      if (selectedNodo) await loadHWAssegnato(parseInt(selectedNodo))
    } finally {
      setAutoPlcLoading(false)
    }
  }

  // Node change
  const handleNodeChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const nodeId = e.target.value
    setSelectedNodo(nodeId)
    await loadHWAssegnato(parseInt(nodeId))
  }

  useEffect(() => {
    (async () => {
      setLoading(true)
      await loadCatalogoHW()
      await loadNodi()
      setLoading(false)
    })()
  }, [])

  return (
    <div className="create-nodes-root">
      <div className="create-nodes-header">
        <div className="node-management">
          <label htmlFor="node-select">Select Existing Node:</label>
          <select id="node-select" value={selectedNodo} onChange={handleNodeChange}>
            {nodes.map(n => (
              <option key={n.id_nodo} value={n.id_nodo}>{n.nome_nodo}</option>
            ))}
          </select>
          <button className="btn update-btn" onClick={() => selectedNodo && loadHWAssegnato(parseInt(selectedNodo))}>Update</button>
        </div>
        <button className="btn auto-plc-btn" onClick={creaPlcAutomatico} disabled={autoPlcLoading}>
          {autoPlcLoading ? 'Creating...' : 'Automatic PLC Creation'}
        </button>
      </div>
      <div className="create-nodes-content">
        <div className="hardware-catalog-section">
          <div className="section-header">
            <span>Hardware Catalog</span>
            <button className="btn update-btn" onClick={loadCatalogoHW}>Update</button>
          </div>
          <table className="hardware-catalog-table">
            <thead>
              <tr>
                <th>HW Name</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {hardware.map(hw => (
                <tr key={hw.id_hw} className={selectedHW?.id_hw === hw.id_hw ? 'selected' : ''} onClick={() => setSelectedHW(hw)}>
                  <td>{hw.nome_hw}</td>
                  <td>{hw.descrizione_hw}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="assign-btn-section">
          <button className="btn assign-btn" onClick={assegnaHardwareAlNodo} disabled={!selectedHW || !selectedNodo || assigning}>
            &gt;
          </button>
        </div>
        <div className="assigned-hardware-section">
          <div className="section-header">
            <span>Hardware Assigned to Node</span>
          </div>
          <table className="assigned-hardware-table">
            <thead>
              <tr>
                <th>HW Name</th>
                <th>Slot</th>
                <th>FROM</th>
                <th>DO</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {nodeHardware.map(hw => (
                <tr key={hw.id_nodo_hw}>
                  <td>{hw.nome_hw}</td>
                  <td>{hw.slot}</td>
                  <td>{hw.DI}</td>
                  <td>{hw.DO}</td>
                  <td>
                    <button className="btn delete-btn" onClick={() => eliminaHWAssegnato(hw)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteModal && hardwareToDelete && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>Confirm Deletion</h2>
            <p>Are you sure you want to delete hardware "{hardwareToDelete.nome_hw}" from this node?</p>
            <button className="btn confirm-btn" onClick={confirmDelete}>Confirm</button>
            <button className="btn cancel-btn" onClick={cancelDelete}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  )
}

export default CreateNodesPage;
