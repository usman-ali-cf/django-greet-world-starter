
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
      await apiFetch('/api/nodes/', {
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
      await apiFetch('/api/hardware/node', {
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
      const response = await apiFetch(`/api/nodes/plc/auto/${id}`, {
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
    <div style={{ overflowX: 'auto', width: '100%', height: 'calc(100vh - 64px)', overflowY: 'auto' }}>
      <div className="space-y-6" style={{ minWidth: 900, display: 'flex', flexDirection: 'column', gap: '24px' }}>
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

        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
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
      </div>

      {/* Modal for creating new node */}
      {isModalOpen && (
        <div id="popupOverlay" className="popup-overlay" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(30, 41, 59, 0.35)', zIndex: 1000 }}>
          <div className="popup-content" style={{ position: 'relative', background: 'rgba(255,255,255,0.97)', borderRadius: '1.5rem', boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.18)', padding: '2.5rem 2rem 2rem 2rem', minWidth: 350, maxWidth: 400, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', border: '1.5px solid #e0e7ef', transition: 'all 0.2s' }}>
            <button
              type="button"
              aria-label="Chiudi"
              onClick={() => setIsModalOpen(false)}
              style={{ position: 'absolute', top: 18, right: 18, background: 'none', border: 'none', fontSize: 22, color: '#64748b', cursor: 'pointer', transition: 'color 0.2s' }}
              onMouseOver={e => (e.currentTarget.style.color = '#ef4444')}
              onMouseOut={e => (e.currentTarget.style.color = '#64748b')}
            >
              ×
            </button>
            <h3 style={{ fontSize: '1.5rem', fontWeight: 700, color: '#1e293b', marginBottom: '1.2rem', textAlign: 'center', letterSpacing: 0.01 }}>Crea Nuovo Nodo</h3>
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
              style={{ display: 'flex', flexDirection: 'column', gap: '1.2rem' }}
            >
              <div>
                <label htmlFor="nomeNodoPopup" style={{ display: 'block', color: '#334155', fontWeight: 600, marginBottom: 6 }}>Nome Nodo</label>
                <input
                  type="text"
                  id="nomeNodoPopup"
                  name="nome_nodo"
                  required
                  style={{ width: '100%', padding: '0.85rem 1rem', borderRadius: '0.9rem', border: '1.5px solid #cbd5e1', background: '#f8fafc', fontSize: '1.05rem', color: '#1e293b', outline: 'none', transition: 'border 0.2s, box-shadow 0.2s' }}
                  onFocus={e => (e.currentTarget.style.border = '1.5px solid #6366f1')}
                  onBlur={e => (e.currentTarget.style.border = '1.5px solid #cbd5e1')}
                />
              </div>
              <div>
                <label htmlFor="descrNodoPopup" style={{ display: 'block', color: '#334155', fontWeight: 600, marginBottom: 6 }}>Descrizione</label>
                <textarea
                  id="descrNodoPopup"
                  name="descrizione"
                  rows={3}
                  style={{ width: '100%', padding: '0.85rem 1rem', borderRadius: '0.9rem', border: '1.5px solid #cbd5e1', background: '#f8fafc', fontSize: '1.05rem', color: '#1e293b', outline: 'none', transition: 'border 0.2s, box-shadow 0.2s', resize: 'vertical' }}
                  onFocus={e => (e.currentTarget.style.border = '1.5px solid #6366f1')}
                  onBlur={e => (e.currentTarget.style.border = '1.5px solid #cbd5e1')}
                ></textarea>
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.7rem', marginTop: 8 }}>
                <button
                  type="button"
                  id="btnChiudiPopup"
                  onClick={() => setIsModalOpen(false)}
                  style={{ padding: '0.7rem 1.3rem', borderRadius: '0.9rem', border: 'none', background: '#e2e8f0', color: '#334155', fontWeight: 600, fontSize: '1.05rem', cursor: 'pointer', transition: 'background 0.2s' }}
                  onMouseOver={e => (e.currentTarget.style.background = '#ca0909')}
                  onMouseOut={e => (e.currentTarget.style.background = '#ca0909')}
                >
                  Annulla
                </button>
                <button type="submit" style={{ padding: '0.7rem 1.3rem', borderRadius: '0.9rem', border: 'none', background: 'linear-gradient(90deg, #ca0909 0%,rgb(214, 88, 88) 100%)', color: '#fff', fontWeight: 700, fontSize: '1.05rem', cursor: 'pointer', boxShadow: '0 1px 4px #ca0909', transition: 'background 0.2s, box-shadow 0.2s' }}>
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
