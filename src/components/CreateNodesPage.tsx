
import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { apiFetch } from '../utils/api'
import DataTable from './DataTable'

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
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [loading, setLoading] = useState(true)

  const loadCatalogoHW = async () => {
    try {
      const data = await apiFetch('/api/catalogo_hw')
      setHardware(data)
    } catch (error) {
      console.error("Errore caricamento catalogo hw:", error)
    }
  }

  const loadNodi = async () => {
    try {
      const nodi = await apiFetch('/api/lista_nodi')
      setNodes(nodi)
      if (nodi.length > 0) {
        setSelectedNodo(nodi[0].id_nodo.toString())
        await loadHWAssegnato(nodi[0].id_nodo)
      }
    } catch (error) {
      console.error("Errore caricamento nodi:", error)
    }
  }

  const loadHWAssegnato = async (idNodo: number) => {
    try {
      const data = await apiFetch(`/api/hw_nodo_list?id_nodo=${idNodo}`)
      setNodeHardware(data)
    } catch (error) {
      console.error("Errore caricamento HW assegnato:", error)
    }
  }

  const creaNuovoNodo = async (formData: { nome_nodo: string; descrizione: string }) => {
    try {
      const payload = {
        id_prg: parseInt(id || '1'),
        nome_nodo: formData.nome_nodo,
        descrizione: formData.descrizione
      }
      await apiFetch('/api/crea_nodo', {
        method: 'POST',
        body: JSON.stringify(payload)
      })
      await loadNodi()
      setIsModalOpen(false)
    } catch (error) {
      console.error("Errore nella creazione nodo:", error)
    }
  }

  const assegnaHardwareAlNodo = async () => {
    if (!selectedNodo) {
      alert("Seleziona un nodo dall'elenco (o creane uno).")
      return
    }
    if (!selectedHW) {
      alert("Seleziona un hardware dalla tabella di sinistra.")
      return
    }

    try {
      const payload = {
        id_nodo: parseInt(selectedNodo),
        id_hw: selectedHW.id_hw,
        quantita: 1
      }
      await apiFetch('/api/hw_nodo_add', {
        method: 'POST',
        body: JSON.stringify(payload)
      })
      await loadHWAssegnato(parseInt(selectedNodo))
    } catch (error) {
      console.error("Errore assegnazione HW:", error)
    }
  }

  const eliminaHWAssegnato = async (idNodoHw: number) => {
    if (!confirm("Sei sicuro di voler eliminare questo HW assegnato?")) return
    
    try {
      await apiFetch(`/api/hw_nodo_list/${idNodoHw}`, {
        method: 'DELETE'
      })
      await loadHWAssegnato(parseInt(selectedNodo))
    } catch (error) {
      console.error("Errore eliminazione HW:", error)
    }
  }

  const creaPlcAutomatico = async () => {
    try {
      const response = await apiFetch('/api/crea_plc_automatico', {
        method: 'POST'
      })
      
      if (response.message) {
        alert(response.message)
        loadNodi()
      } else if (response.error) {
        alert("Errore: " + response.error)
      }
    } catch (err) {
      console.error("Errore nella creazione automatica PLC:", err)
      alert("Si è verificato un errore nella creazione automatica del PLC.")
    }
  }

  const addActionButtons = (data: NodeHardware[]) => {
    const tbody = document.querySelector('#tabella-hw-nodo tbody')
    if (!tbody) return

    const rows = tbody.querySelectorAll('tr')
    rows.forEach((row, index) => {
      const item = data[index]
      if (!item) return
      
      const cellAzioni = row.lastElementChild as HTMLTableCellElement
      const btnDelete = document.createElement("button")
      btnDelete.textContent = "Elimina"
      btnDelete.className = "btn-delete-hw"
      btnDelete.addEventListener("click", () => eliminaHWAssegnato(item.id_nodo_hw))
      
      cellAzioni.innerHTML = ""
      cellAzioni.appendChild(btnDelete)
    })
  }

  const handleHWRowClick = (item: Hardware, tr: HTMLTableRowElement) => {
    tr.parentNode?.querySelectorAll('tr').forEach(r => r.classList.remove('selected'))
    tr.classList.add('selected')
    setSelectedHW(item)
  }

  const handleNodeChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const nodeId = e.target.value
    setSelectedNodo(nodeId)
    await loadHWAssegnato(parseInt(nodeId))
  }

  useEffect(() => {
    const initPage = async () => {
      await loadCatalogoHW()
      await loadNodi()
      setLoading(false)
    }
    initPage()
  }, [])

  if (loading) {
    return <div className="text-center p-8">Caricamento...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header with buttons */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Crea Nodi e PLC</h2>
        <div className="space-x-2">
          <button 
            id="btnApriPopup"
            onClick={() => setIsModalOpen(true)}
            className="btn"
          >
            Crea Nuovo Nodo
          </button>
          <button 
            id="btnCreazioneAutomaticaPLC"
            onClick={creaPlcAutomatico}
            className="btn"
          >
            Creazione Automatica PLC
          </button>
          <button 
            id="aggiorna-lista-hw"
            onClick={loadCatalogoHW}
            className="btn"
          >
            Aggiorna Lista HW
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Left side - Hardware Catalog */}
        <div className="catalogo-hardware">
          <h3>Catalogo Hardware</h3>
          <DataTable
            columns={columnsCatalogoHW}
            data={hardware}
            onRowClick={handleHWRowClick}
            containerSelector="#tabella-hw"
          />
          <table style={{ display: 'none' }}>
            <tbody id="tabella-hw"></tbody>
          </table>
        </div>

        {/* Right side - Node Configuration */}
        <div className="form-configurazione-nodo">
          <h3>Configurazione Nodo</h3>
          
          <div className="seleziona-nodo">
            <label htmlFor="selectNodo">Seleziona Nodo:</label>
            <select 
              id="selectNodo" 
              value={selectedNodo} 
              onChange={handleNodeChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              {nodes.map(node => (
                <option key={node.id_nodo} value={node.id_nodo}>
                  {node.nome_nodo}
                </option>
              ))}
            </select>
          </div>

          <div className="mt-4">
            <button 
              id="btnAssegnaHW"
              onClick={assegnaHardwareAlNodo}
              className="btn w-full"
            >
              Assegna Hardware al Nodo
            </button>
          </div>

          <div className="tabella-hw-assegnato mt-4">
            <h4>Hardware Assegnato</h4>
            <DataTable
              columns={columnsHWAssegnato}
              data={nodeHardware}
              postRender={addActionButtons}
              containerSelector="#tabella-hw-nodo"
            />
            <table style={{ display: 'none' }}>
              <tbody id="tabella-hw-nodo"></tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Modal for creating new node */}
      {isModalOpen && (
        <div id="popupOverlay" className="popup-overlay" style={{ display: 'flex' }}>
          <div className="popup-content">
            <h3>Crea Nuovo Nodo</h3>
            <form 
              onSubmit={(e) => {
                e.preventDefault()
                const formData = new FormData(e.currentTarget)
                const nome_nodo = formData.get('nome_nodo') as string
                const descrizione = formData.get('descrizione') as string
                if (nome_nodo) {
                  creaNuovoNodo({ nome_nodo, descrizione })
                }
              }}
            >
              <div className="mb-4">
                <label htmlFor="nomeNodoPopup" className="block text-gray-700 mb-2">Nome Nodo:</label>
                <input
                  type="text"
                  id="nomeNodoPopup"
                  name="nome_nodo"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>
              <div className="mb-4">
                <label htmlFor="descrNodoPopup" className="block text-gray-700 mb-2">Descrizione:</label>
                <textarea
                  id="descrNodoPopup"
                  name="descrizione"
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
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
                  Crea Nodo
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default CreateNodesPage
