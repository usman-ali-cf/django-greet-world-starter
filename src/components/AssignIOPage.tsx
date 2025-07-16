
import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { apiFetch } from '../utils/api'
import DataTable from './DataTable'
import DataTableMulti from './DataTableMulti'

interface Node {
  id_nodo: number
  nome_nodo: string
}

interface Module {
  id_nodo_hw: number
  slot: number
  nome_hw: string
  tipo: string
}

interface IOData {
  id_io: number
  descrizione: string
  selezionato?: boolean
}

const columnsModuli = [
  { header: "Slot", field: "slot" },
  { header: "Nome HW", field: "nome_hw" },
  { header: "Tipo HW", field: "tipo" }
]

const columnsIOunassigned = [
  { header: "", field: "selezionato", type: "checkbox" },
  { header: "Commento IO", field: "descrizione" }
]

const columnsIOassigned = [
  { header: "", field: "selezionato", type: "checkbox" },
  { header: "Commento IO", field: "descrizione" }
]

const AssignIOPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const [nodes, setNodes] = useState<Node[]>([])
  const [modules, setModules] = useState<Module[]>([])
  const [unassignedIO, setUnassignedIO] = useState<IOData[]>([])
  const [assignedIO, setAssignedIO] = useState<IOData[]>([])
  const [selectedNodo, setSelectedNodo] = useState<string>('')
  const [selectedModulo, setSelectedModulo] = useState<number | null>(null)
  const [tipoModulo, setTipoModulo] = useState<string>('')
  const [filterUnassigned, setFilterUnassigned] = useState('')
  const [filterAssigned, setFilterAssigned] = useState('')
  const [loading, setLoading] = useState(true)

  const loadNodi = async () => {
    try {
      const nodi = await apiFetch('/api/lista_nodi')
      setNodes(nodi)
      if (nodi.length > 0) {
        setSelectedNodo(nodi[0].id_nodo.toString())
        await loadModuliNodo(nodi[0].id_nodo)
      }
    } catch (err) {
      console.error("Errore loadNodi:", err)
    }
  }

  const loadModuliNodo = async (idNodo: number) => {
    try {
      const data = await apiFetch(`/api/hw_nodo_list?id_nodo=${idNodo}`)
      setModules(data)
      // Reset selection
      setSelectedModulo(null)
      setTipoModulo('')
      setUnassignedIO([])
      setAssignedIO([])
    } catch (err) {
      console.error("Errore loadModuliNodo:", err)
    }
  }

  const loadIOunassigned = async () => {
    if (!selectedModulo || !tipoModulo) {
      setUnassignedIO([])
      return
    }
    try {
      const data = await apiFetch(`/api/io_unassigned?tipo=${encodeURIComponent(tipoModulo)}`)
      setUnassignedIO(data)
    } catch (err) {
      console.error("Errore loadIOunassigned:", err)
    }
  }

  const loadIOassigned = async (idNodo: number, idModuloHW: number) => {
    if (!idModuloHW) {
      setAssignedIO([])
      return
    }
    try {
      const data = await apiFetch(`/api/io_assigned?id_modulo=${idModuloHW}&id_nodo=${idNodo}`)
      setAssignedIO(data)
    } catch (err) {
      console.error("Errore loadIOassigned:", err)
    }
  }

  const assegnaIOalModulo = async () => {
    if (!selectedModulo) {
      alert("Seleziona un modulo dalla tabella moduli")
      return
    }
    const rowsSelected = document.querySelectorAll('#tabella-io-unassigned tr.selected')
    if (rowsSelected.length === 0) {
      alert("Nessun IO selezionato in 'IO Non Assegnati'")
      return
    }
    
    const ids = Array.from(rowsSelected).map(tr => tr.getAttribute('data-id'))
    try {
      for (const idIO of ids) {
        const payload = { id_io: idIO, id_modulo: selectedModulo }
        const response = await apiFetch('/api/io_assign', {
          method: 'POST',
          body: JSON.stringify(payload)
        })
        
        if (response.error) {
          alert("Operazione non consentita: " + response.error)
          return
        }
        if (response.message && (response.message.indexOf("Capacità superata") !== -1 ||
            response.message.indexOf("non corrisponde") !== -1)) {
          alert(response.message)
          loadIOunassigned()
          loadIOassigned(parseInt(selectedNodo), selectedModulo)
          return
        }
      }
      loadIOunassigned()
      loadIOassigned(parseInt(selectedNodo), selectedModulo)
    } catch (err) {
      console.error("Errore assegnaIOalModulo:", err)
    }
  }

  const rimuoviIOdalModulo = async () => {
    if (!selectedModulo) {
      alert("Seleziona un modulo dalla tabella moduli")
      return
    }
    const rowsSelected = document.querySelectorAll('#tabella-io-assigned tr.selected')
    if (rowsSelected.length === 0) {
      alert("Nessun IO selezionato in 'IO Assegnati'")
      return
    }
    
    const ids = Array.from(rowsSelected).map(tr => tr.getAttribute('data-id'))
    try {
      for (const idIO of ids) {
        await apiFetch(`/api/io_assign?id_io=${idIO}`, { method: 'DELETE' })
      }
      loadIOunassigned()
      loadIOassigned(parseInt(selectedNodo), selectedModulo)
    } catch (err) {
      console.error("Errore rimuoviIOdalModulo:", err)
    }
  }

  const assegnazioneAutomatica = async () => {
    if (!selectedNodo) {
      alert("Seleziona un nodo prima di procedere con l'assegnazione automatica.")
      return
    }
    
    const payload = { id_nodo: parseInt(selectedNodo) }
    
    try {
      const response = await apiFetch('/api/assegna_io_automatico', {
        method: 'POST',
        body: JSON.stringify(payload)
      })
      
      if (response.success) {
        alert(response.message)
      } else {
        alert("Errore: " + response.message)
      }
      
      loadIOunassigned()
      if (selectedModulo) loadIOassigned(parseInt(selectedNodo), selectedModulo)
    } catch (err) {
      console.error("Errore nell'assegnazione automatica:", err)
      alert("Si è verificato un errore durante l'assegnazione automatica.")
    }
  }

  const exportaIO = async (format = 'xml') => {
    try {
      const response = await apiFetch(`/api/export_io?format=${format}`, {
        method: 'POST'
      })

      if (response.file) {
        window.location.href = '/download/' + response.file
      } else {
        alert("Export completato, ma senza file restituito.")
      }
    } catch (err) {
      console.error("Errore durante l'esportazione IO:", err)
      alert("❌ Errore durante l'esportazione IO.")
    }
  }

  const esportaSchemainExcel = async () => {
    try {
      const response = await apiFetch('/api/genera_schema', {
        method: 'POST'
      })

      if (response.message && response.file) {
        window.location.href = '/download/' + response.file
      } else {
        alert("⚠️ Export completato, ma senza messaggio di conferma.")
      }
    } catch (err) {
      console.error("Errore durante esportazione Excel:", err)
      alert("❌ Errore durante l'esportazione del file.")
    }
  }

  const handleNodeChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const nodeId = e.target.value
    setSelectedNodo(nodeId)
    setSelectedModulo(null)
    setTipoModulo('')
    await loadModuliNodo(parseInt(nodeId))
    setUnassignedIO([])
    setAssignedIO([])
  }

  const handleModuleRowClick = (item: Module, tr: HTMLTableRowElement) => {
    tr.parentNode?.querySelectorAll('tr').forEach(r => r.classList.remove('selected'))
    tr.classList.add('selected')
    setSelectedModulo(item.id_nodo_hw)
    setTipoModulo(item.tipo)
    // Load IO data for this module
    loadIOunassigned()
    loadIOassigned(parseInt(selectedNodo), item.id_nodo_hw)
  }

  const handleSelectAllUnassigned = (e: React.ChangeEvent<HTMLInputElement>) => {
    const rows = document.querySelectorAll('#tabella-io-unassigned tr')
    rows.forEach(row => {
      if (e.target.checked) {
        row.classList.add('selected')
      } else {
        row.classList.remove('selected')
      }
    })
  }

  const handleSelectAllAssigned = (e: React.ChangeEvent<HTMLInputElement>) => {
    const rows = document.querySelectorAll('#tabella-io-assigned tr')
    rows.forEach(row => {
      if (e.target.checked) {
        row.classList.add('selected')
      } else {
        row.classList.remove('selected')
      }
    })
  }

  useEffect(() => {
    loadNodi().finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    loadIOunassigned()
  }, [selectedModulo, tipoModulo])

  if (loading) {
    return <div className="text-center p-8">Caricamento...</div>
  }

  return (
    <div className="space-y-6">
      {/* Header with buttons */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Assegna I/O ai Nodi</h2>
        <div className="space-x-2">
          <button 
            id="btnAggiornaNodi"
            onClick={loadNodi}
            className="btn"
          >
            Aggiorna Nodi
          </button>
          <button 
            id="btnAggiornaIO"
            onClick={loadIOunassigned}
            className="btn"
          >
            Aggiorna IO
          </button>
          <button 
            id="btnAssegnazioneAutomatica"
            onClick={assegnazioneAutomatica}
            className="btn"
          >
            Assegnazione Automatica
          </button>
          <button 
            id="btnExportIO"
            onClick={() => exportaIO('xml')}
            className="btn"
          >
            Export IO
          </button>
          <button 
            id="btnGeneraSchema"
            onClick={esportaSchemainExcel}
            className="btn"
          >
            Genera Schema
          </button>
        </div>
      </div>

      {/* Node Selection */}
      <div className="seleziona-nodo">
        <label htmlFor="selectNodo">Seleziona Nodo:</label>
        <select 
          id="selectNodo" 
          value={selectedNodo} 
          onChange={handleNodeChange}
          className="ml-2 px-3 py-2 border border-gray-300 rounded-md"
        >
          {nodes.map(node => (
            <option key={node.id_nodo} value={node.id_nodo}>
              {node.nome_nodo}
            </option>
          ))}
        </select>
      </div>

      {/* Main Grid Layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px' }}>
        {/* Modules Table */}
        <div className="tabella-moduli">
          <h3>Moduli</h3>
          <DataTable
            columns={columnsModuli}
            data={modules}
            onRowClick={handleModuleRowClick}
            containerSelector="#tabella-moduli"
          />
          <table style={{ display: 'none' }}>
            <tbody id="tabella-moduli"></tbody>
          </table>
        </div>

        {/* Unassigned IO */}
        <div className="tabella-io-non-assegnati">
          <div className="flex justify-between items-center mb-2">
            <h3>IO Non Assegnati</h3>
            <label>
              <input 
                type="checkbox" 
                id="selectAllUnassigned"
                onChange={handleSelectAllUnassigned}
              />
              Seleziona Tutto
            </label>
          </div>
          <input
            type="text"
            id="filterUnassigned"
            placeholder="Filtra per commento..."
            value={filterUnassigned}
            onChange={(e) => setFilterUnassigned(e.target.value)}
            className="w-full px-3 py-1 border border-gray-300 rounded-md mb-2"
          />
          <DataTableMulti
            columns={columnsIOunassigned}
            data={unassignedIO.filter(item => 
              item.descrizione.toLowerCase().includes(filterUnassigned.toLowerCase())
            )}
            containerSelector="#tabella-io-unassigned"
          />
          <table style={{ display: 'none' }}>
            <tbody id="tabella-io-unassigned"></tbody>
          </table>
          <button 
            id="btnAssegnaIO"
            onClick={assegnaIOalModulo}
            className="btn w-full mt-2"
          >
            Assegna IO →
          </button>
        </div>

        {/* Assigned IO */}
        <div className="tabella-io-assegnati">
          <div className="flex justify-between items-center mb-2">
            <h3>IO Assegnati</h3>
            <label>
              <input 
                type="checkbox" 
                id="selectAllAssigned"
                onChange={handleSelectAllAssigned}
              />
              Seleziona Tutto
            </label>
          </div>
          <input
            type="text"
            id="filterAssigned"
            placeholder="Filtra per commento..."
            value={filterAssigned}
            onChange={(e) => setFilterAssigned(e.target.value)}
            className="w-full px-3 py-1 border border-gray-300 rounded-md mb-2"
          />
          <DataTableMulti
            columns={columnsIOassigned}
            data={assignedIO.filter(item => 
              item.descrizione.toLowerCase().includes(filterAssigned.toLowerCase())
            )}
            containerSelector="#tabella-io-assigned"
          />
          <table style={{ display: 'none' }}>
            <tbody id="tabella-io-assigned"></tbody>
          </table>
          <button 
            id="btnRimuoviIO"
            onClick={rimuoviIOdalModulo}
            className="btn w-full mt-2"
          >
            ← Rimuovi IO
          </button>
        </div>
      </div>
    </div>
  )
}

export default AssignIOPage
