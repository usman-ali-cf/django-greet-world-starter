
import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { apiFetch } from '../utils/api'
import DataTable from './DataTable'
import DataTableMulti from './DataTableMulti'
import './AssignIOPage.css'

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
      const nodi = await apiFetch(`/api/lista_nodi?id_prg=${id}`)
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
      const data = await apiFetch(`/io/unassigned?project_id=${id}&tipo=${encodeURIComponent(tipoModulo)}`)
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
      const data = await apiFetch(`/io/assigned?module_id=${idModuloHW}&node_id=${idNodo}`)
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
    const rowsSelected = document.querySelectorAll('.io-panel:first-child .io-table-row.selected')
    if (rowsSelected.length === 0) {
      alert("Nessun IO selezionato in 'IO Non Assegnati'")
      return
    }
    
    const ids = Array.from(rowsSelected).map(tr => tr.getAttribute('data-id'))
    try {
      for (const idIO of ids) {
        const payload = { id_io: parseInt(idIO!), id_modulo: selectedModulo }
        const response = await apiFetch('/io/assign', {
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
    const rowsSelected = document.querySelectorAll('.io-panel:last-child .io-table-row.selected')
    if (rowsSelected.length === 0) {
      alert("Nessun IO selezionato in 'IO Assegnati'")
      return
    }
    
    const ids = Array.from(rowsSelected).map(tr => tr.getAttribute('data-id'))
    try {
      for (const idIO of ids) {
        await apiFetch(`/io/assign/${idIO}`, { method: 'DELETE' })
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
    
    try {
      const response = await apiFetch(`/io/assign/auto?node_id=${parseInt(selectedNodo)}&project_id=${id}`, {
        method: 'POST'
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
      const response = await apiFetch(`/api/export_io?format=${format}&id_prg=${id}`, {
        method: 'POST'
      })

      if (response.status === 200) {
        // Directly navigate to the download endpoint
        window.location.href = `http://localhost:8000/api/download/export_io.${format}`
      } else {
        alert("Errore durante l'esportazione: " + (response.message || 'Errore sconosciuto'))
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
    const rows = document.querySelectorAll('.io-panel:first-child .io-table-row')
    rows.forEach(row => {
      if (e.target.checked) {
        row.classList.add('selected')
      } else {
        row.classList.remove('selected')
      }
    })
  }

  const handleSelectAllAssigned = (e: React.ChangeEvent<HTMLInputElement>) => {
    const rows = document.querySelectorAll('.io-panel:last-child .io-table-row')
    rows.forEach(row => {
      if (e.target.checked) {
        row.classList.add('selected')
      } else {
        row.classList.remove('selected')
      }
    })
  }

  const handleIORowClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const row = e.currentTarget
    row.classList.toggle('selected')
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
    <div className="assign-io-page">
      {/* Top Section - IO Panels */}
      <div className="io-panels-section">
        {/* Left Panel - IO Non Assegnati */}
        <div className="io-panel">
          <div className="io-panel-header">
            <h3 className="io-panel-title">IO Non Assegnati</h3>
            <button className="btn-update-io" onClick={loadIOunassigned}>
              Aggiorna IO
            </button>
          </div>
          
          <div className="io-panel-controls">
            <label className="select-all-label">
              <input 
                type="checkbox" 
                onChange={handleSelectAllUnassigned}
                className="select-all-checkbox"
              />
              Seleziona Tutto
            </label>
            <input
              type="text"
              placeholder="Filtra per Commento IO"
              value={filterUnassigned}
              onChange={(e) => setFilterUnassigned(e.target.value)}
              className="io-filter-input"
            />
          </div>
          
          <div className="io-table-container">
            <div className="io-table-header">
              <span>Commento IO</span>
            </div>
            <div className="io-table-content">
              {unassignedIO.filter(item => 
                item.descrizione.toLowerCase().includes(filterUnassigned.toLowerCase())
              ).map((io) => (
                <div key={io.id_io} className="io-table-row" data-id={io.id_io} onClick={handleIORowClick}>
                  <span className="io-comment">{io.descrizione}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Middle Transfer Buttons */}
        <div className="transfer-buttons">
          <button 
            className="transfer-btn transfer-right"
            onClick={assegnaIOalModulo}
            title="Assegna IO al Modulo"
          >
            &gt;
          </button>
          <button 
            className="transfer-btn transfer-left"
            onClick={rimuoviIOdalModulo}
            title="Rimuovi IO dal Modulo"
          >
            &lt;
          </button>
        </div>

        {/* Right Panel - IO Assegnati al Modulo */}
        <div className="io-panel">
          <div className="io-panel-header">
            <h3 className="io-panel-title">IO Assegnati al Modulo</h3>
          </div>
          
          <div className="io-panel-controls">
            <label className="select-all-label">
              <input 
                type="checkbox" 
                onChange={handleSelectAllAssigned}
                className="select-all-checkbox"
              />
              Seleziona Tutto
            </label>
            <input
              type="text"
              placeholder="Filtra per Commento IO"
              value={filterAssigned}
              onChange={(e) => setFilterAssigned(e.target.value)}
              className="io-filter-input"
            />
          </div>
          
          <div className="io-table-container">
            <div className="io-table-header">
              <span>Commento IO</span>
            </div>
            <div className="io-table-content">
              {assignedIO.filter(item => 
                item.descrizione.toLowerCase().includes(filterAssigned.toLowerCase())
              ).map((io) => (
                <div key={io.id_io} className="io-table-row" data-id={io.id_io} onClick={handleIORowClick}>
                  <span className="io-comment">{io.descrizione}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Section - Modules Table */}
      <div className="modules-section">
        <div className="modules-header">
          <h3 className="modules-title">Moduli (Hardware) del Nodo – Assegna I/O ai Moduli</h3>
        </div>
        
        <div className="modules-controls">
          <label className="node-select-label">
            Seleziona Nodo:
            <select 
              value={selectedNodo} 
              onChange={handleNodeChange}
              className="node-select"
            >
              {nodes.map(node => (
                <option key={node.id_nodo} value={node.id_nodo}>
                  {node.nome_nodo}
                </option>
              ))}
            </select>
          </label>
          
          <div className="modules-buttons">
            <button className="btn-module" onClick={loadNodi}>
              Aggiorna Nodi
            </button>
            <button className="btn-module" onClick={assegnazioneAutomatica}>
              Assegnazione automatica
            </button>
            <button className="btn-module" onClick={() => exportaIO('xml')}>
              📊 Esporta Excel
            </button>
            <button className="btn-module" onClick={esportaSchemainExcel}>
              Genera File Schema Elettrico
            </button>
          </div>
        </div>
        
        <div className="modules-table-container">
          <div className="modules-table-header">
            <span className="header-slot">Slot</span>
            <span className="header-nome">Nome HW</span>
            <span className="header-tipo">Tipo</span>
          </div>
          <div className="modules-table-content">
            {modules.map((module) => (
              <div 
                key={module.id_nodo_hw} 
                className={`module-row ${selectedModulo === module.id_nodo_hw ? 'selected' : ''}`}
                onClick={() => {
                  setSelectedModulo(module.id_nodo_hw)
                  setTipoModulo(module.tipo)
                  loadIOunassigned()
                  loadIOassigned(parseInt(selectedNodo), module.id_nodo_hw)
                }}
              >
                <span className="module-slot">{module.slot}</span>
                <span className="module-nome">{module.nome_hw}</span>
                <span className="module-tipo">{module.tipo}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AssignIOPage
