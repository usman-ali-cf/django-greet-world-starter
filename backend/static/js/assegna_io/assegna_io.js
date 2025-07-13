import { renderDataTable } from '../standard/tables.js';
import { renderDataTableMulti } from '../standard/tables-multi.js';
import { apiFetch } from '../standard/api.js';

/* Colonne moduli (singola selezione) */
const columnsModuli = [
  { header: "Slot", field: "slot" },
  { header: "Nome HW", field: "nome_hw" },
  { header: "Tipo HW", field: "tipo" }
];

/* Colonne IO (multiselezione) */
const columnsIOunassigned = [
  { header: "", field: "selezionato", type: "checkbox" },
  { header: "Commento IO", field: "descrizione" }
];
const columnsIOassigned = [
  { header: "", field: "selezionato", type: "checkbox" },
  { header: "Commento IO", field: "descrizione" }
];

// Variabili globali
let selectedNodo = null;
let selectedModulo = null; // useremo item.id_nodo_hw
let tipoModulo = null;

document.addEventListener('DOMContentLoaded', init);

function init() {
  console.log("Multiselezione init");

  // Pulsanti
  addClickListener('btnAggiornaNodi', loadNodi);
  addClickListener('btnAggiornaIO', loadIOunassigned);
  addClickListener('btnAssegnaIO', assegnaIOalModulo);
  addClickListener('btnRimuoviIO', rimuoviIOdalModulo);
  addClickListener('btnAssegnazioneAutomatica', assegnazioneAutomatica);
  //addClickListener('btnExportIO', esportaIOinExcel);
  addClickListener('btnGeneraSchema', esportaSchemainExcel);
  addClickListener('btnExportIO', () => exportaIO('xml'));

  // Gestione "Seleziona Tutto" per Unassigned
  const selectAllUnassigned = document.getElementById('selectAllUnassigned');
  if (selectAllUnassigned) {
    selectAllUnassigned.addEventListener('change', () => {
      const rows = document.querySelectorAll('#tabella-io-unassigned tr');
      rows.forEach(row => {
        if (selectAllUnassigned.checked) {
          row.classList.add('selected');
        } else {
          row.classList.remove('selected');
        }
      });
    });
  }

  const selectAllAssigned = document.getElementById('selectAllAssigned');
  if (selectAllAssigned) {
    selectAllAssigned.addEventListener('change', () => {
      const rows = document.querySelectorAll('#tabella-io-assigned tr');
      rows.forEach(row => {
        if (selectAllAssigned.checked) {
          row.classList.add('selected');
        } else {
          row.classList.remove('selected');
        }
      });
    });
  }

  // Filtro su Commento IO per Unassigned
  const filterInput = document.getElementById('filterUnassigned');
  if (filterInput) {
    filterInput.addEventListener('input', () => {
      filterTable('tabella-io-unassigned', filterInput.value);
    });
  }

    // Filtro su Commento IO per assigned
    const filterInput_assigned = document.getElementById('filterAssigned');
    if (filterInput_assigned) {
      filterInput_assigned.addEventListener('input', () => {
        filterTable('tabella-io-assigned', filterInput_assigned.value);
      });
    }
  loadNodi();
}

function addClickListener(id, handler) {
  const btn = document.getElementById(id);
  if (!btn) {
    console.warn(`Bottone #${id} non trovato`);
    return;
  }
  btn.addEventListener('click', handler);
  console.log(`Listener aggiunto a #${id}`);
}

/* Carica nodi */
async function loadNodi() {
  try {
    const nodi = await apiFetch('/api/lista_nodi');
    const selNodo = document.getElementById('selectNodo');
    selNodo.innerHTML = '';
    nodi.forEach(n => {
      const opt = document.createElement('option');
      opt.value = n.id_nodo;
      opt.textContent = n.nome_nodo;
      selNodo.appendChild(opt);
    });
    if (nodi.length > 0) {
      selectedNodo = nodi[0].id_nodo;
      selNodo.value = selectedNodo;
      await loadModuliNodo(selectedNodo);
    }
    selNodo.addEventListener('change', async (e) => {
      selectedNodo = e.target.value;
      selectedModulo = null;
      tipoModulo = null;
      await loadModuliNodo(selectedNodo);
      // Svuota le tabelle IO
      renderDataTableMulti({
        containerSelector: '#tabella-io-unassigned',
        columns: columnsIOunassigned,
        data: []
      });
      renderDataTableMulti({
        containerSelector: '#tabella-io-assigned',
        columns: columnsIOassigned,
        data: []
      });
    });
    console.log("Nodi caricati");
  } catch (err) {
    console.error("Errore loadNodi:", err);
  }
}

/* Carica moduli per il nodo selezionato */
async function loadModuliNodo(idNodo) {
  try {
    const data = await apiFetch(`/api/hw_nodo_list?id_nodo=${idNodo}`);
    renderDataTable({
      containerSelector: '#tabella-moduli',
      columns: columnsModuli,
      data,
      onRowClick: (item, tr) => {
        // Selezione singola
        tr.parentNode.querySelectorAll('tr').forEach(r => r.classList.remove('selected'));
        tr.classList.add('selected');
        selectedModulo = item.id_nodo_hw; // da JOIN con t_cat_hw
        tipoModulo = item.tipo;
        console.log("Modulo selezionato:", selectedModulo, "Tipo:", tipoModulo);
        loadIOunassigned();
        loadIOassigned(selectedNodo, selectedModulo);
      },
      postRender: (tbody, data) => {
        // Se desideri impostare attributi
        tbody.querySelectorAll('tr').forEach((tr, idx) => {
          if (data[idx].id_nodo_hw) {
            tr.setAttribute('data-id', data[idx].id_nodo_hw);
          }
        });
      }
    });
  } catch (err) {
    console.error("Errore loadModuliNodo:", err);
  }
}

/* Carica IO non assegnati (multiselezione) */
async function loadIOunassigned() {
  if (!selectedModulo || !tipoModulo) {
    console.warn("Modulo/tipo non selezionati, tabella unassigned vuota");
    renderDataTableMulti({ containerSelector: '#tabella-io-unassigned', columns: columnsIOunassigned, data: [] });
    return;
  }
  try {
    const data = await apiFetch(`/api/io_unassigned?tipo=${encodeURIComponent(tipoModulo)}`);
    console.log("Ricevuti IO non assegnati:", data);
    renderDataTableMulti({
      containerSelector: '#tabella-io-unassigned',
      columns: columnsIOunassigned,
      data,
      postRender: (tbody, data) => {
        // Imposta data-id su ogni riga
        tbody.querySelectorAll('tr').forEach((tr, idx) => {
          const record = data[idx];
          if (record?.id_io) {
            tr.setAttribute('data-id', record.id_io);
          }
        });
      }
    });
  } catch (err) {
    console.error("Errore loadIOunassigned:", err);
  }
}

/* Carica IO assegnati al modulo */
async function loadIOassigned(idNodo, idModuloHW) {
  if (!idModuloHW) {
    console.warn("Modulo non selezionato, tabella assigned vuota");
    renderDataTableMulti({ containerSelector: '#tabella-io-assigned', columns: columnsIOassigned, data: [] });
    return;
  }
  try {
    const data = await apiFetch(`/api/io_assigned?id_modulo=${idModuloHW}&id_nodo=${idNodo}`);
    console.log("Ricevuti IO assegnati:", data);
    renderDataTableMulti({
      containerSelector: '#tabella-io-assigned',
      columns: columnsIOassigned,
      data,
      postRender: (tbody, data) => {
        tbody.querySelectorAll('tr').forEach((tr, idx) => {
          const record = data[idx];
          if (record?.id_io) {
            tr.setAttribute('data-id', record.id_io);
          }
        });
      }
    });
  } catch (err) {
    console.error("Errore loadIOassigned:", err);
  }
}

/* Assegna IO multipli */
async function assegnaIOalModulo() {
  if (!selectedModulo) {
    alert("Seleziona un modulo dalla tabella moduli");
    return;
  }
  const rowsSelected = document.querySelectorAll('#tabella-io-unassigned tr.selected');
  if (rowsSelected.length === 0) {
    alert("Nessun IO selezionato in 'IO Non Assegnati'");
    return;
  }
  const ids = Array.from(rowsSelected).map(tr => tr.getAttribute('data-id'));
  try {
    for (const idIO of ids) {
      const payload = { id_io: idIO, id_modulo: selectedModulo };
      const response = await apiFetch('/api/io_assign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      // Se l'API restituisce un campo "error", mostra l'errore
      if (response.error) {
        alert("Operazione non consentita: " + response.error);
        return; // interrompi l'assegnazione
      }
      // Se l'API restituisce un messaggio che indica che la condizione non è soddisfatta,
      // ad esempio "Capacità superata..." oppure "Tipo di IO non corrisponde..."
      if (response.message && (response.message.indexOf("Capacità superata") !== -1 ||
          response.message.indexOf("non corrisponde") !== -1)) {
        alert(response.message);
        loadIOunassigned();
        loadIOassigned(selectedNodo, selectedModulo);
        return; // interrompi l'assegnazione
      }
      
      console.log("Assegnato IO:", idIO);
    }
    loadIOunassigned();
    loadIOassigned(selectedNodo, selectedModulo);
  } catch (err) {
    console.error("Errore assegnaIOalModulo:", err);
  }
}


/* Rimuovi IO multipli */
async function rimuoviIOdalModulo() {
  if (!selectedModulo) {
    alert("Seleziona un modulo dalla tabella moduli");
    return;
  }
  const rowsSelected = document.querySelectorAll('#tabella-io-assigned tr.selected');
  if (rowsSelected.length === 0) {
    alert("Nessun IO selezionato in 'IO Assegnati'");
    return;
  }
  const ids = Array.from(rowsSelected).map(tr => tr.getAttribute('data-id'));
  try {
    for (const idIO of ids) {
      await apiFetch(`/api/io_assign?id_io=${idIO}`, { method: 'DELETE' });
      console.log("Rimosso IO:", idIO);
    }
    loadIOunassigned();
    loadIOassigned(selectedNodo, selectedModulo);
  } catch (err) {
    console.error("Errore rimuoviIOdalModulo:", err);
  }
}

/* Filtra righe di una tabella in base al testo nel commento IO (colonna 1) */
function filterTable(tbodyId, filterText) {
  const tbody = document.getElementById(tbodyId);
  if (!tbody) return;
  const rows = tbody.querySelectorAll('tr');
  const lowerFilter = filterText.toLowerCase();
  rows.forEach(row => {
    // indice 1 = colonna "Commento IO"
    const commentCell = row.cells[1]?.textContent?.toLowerCase() || "";
    if (commentCell.includes(lowerFilter)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
}
async function assegnazioneAutomatica() {
  // Controlla che sia stato selezionato un nodo
  if (!selectedNodo) {
    alert("Seleziona un nodo prima di procedere con l'assegnazione automatica.");
    return;
  }
  
  // Costruisci il payload da inviare; l'id_prg viene recuperato dal server via sessione
  const payload = { id_nodo: selectedNodo };
  
  try {
    const response = await apiFetch('/api/assegna_io_automatico', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (response.success) {
      alert(response.message);
    } else {
      alert("Errore: " + response.message);
    }
    
    // Aggiorna le tabelle degli IO dopo l'assegnazione
    loadIOunassigned();
    if (selectedModulo) loadIOassigned(selectedNodo, selectedModulo);
  } catch (err) {
    console.error("Errore nell'assegnazione automatica:", err);
    alert("Si è verificato un errore durante l'assegnazione automatica.");
  }
}


async function esportaIOinExcel() {
  try {
    const response = await apiFetch('/api/export_io', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
      
    });

    if (response.message) {
      window.location.href = '/download/export_io.xml';
;

      // Se vuoi anche forzare il download, potresti fare:
      // window.location.href = '/download/export_io.xlsx';
    } else {
      alert("⚠️ Export completato, ma senza messaggio di conferma.");
    }

  } catch (err) {
    console.error("Errore durante esportazione Excel:", err);
    alert("❌ Errore durante l'esportazione del file.");
  }
}

async function esportaSchemainExcel() {
  try {
    const response = await apiFetch('/api/genera_schema', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });

    if (response.message && response.file) {
      // Usa il file restituito (ad es. "schema_elettrico_6.csv") e genera l'URL corretto
      window.location.href = '/download/' + response.file;
    } else {
      alert("⚠️ Export completato, ma senza messaggio di conferma.");
    }
  } catch (err) {
    console.error("Errore durante esportazione Excel:", err);
    alert("❌ Errore durante l'esportazione del file.");
  }
}


async function exportaIO(format = 'xml') {
  try {
    const response = await apiFetch(`/api/export_io?format=${format}`, {
      method: 'POST'
    });

    if (response.file) {
      // scarica il file appena creato
      window.location.href = '/download/' + response.file;
    } else {
      alert("Export completato, ma senza file restituito.");
    }
  } catch (err) {
    console.error("Errore durante l'esportazione IO:", err);
    alert("❌ Errore durante l'esportazione IO.");
  }
}
