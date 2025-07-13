




// static/js/crea_nodo/crea_nodo.js

import { renderDataTable } from '../standard/tables.js';
import { apiFetch } from '../standard/api.js';

// Colonne per la tabella "Catalogo HW"
const columnsCatalogoHW = [
  { header: "Nome HW", field: "nome_hw" },
  { header: "Descrizione", field: "descrizione_hw" }
];

// Colonne per la tabella HW Assegnato
// Abbiamo rimosso "Slot", perché il backend lo gestisce in automatico
const columnsHWAssegnato = [
  { header: "Nome HW", field: "nome_hw" },
  { header: "Slot", field: "slot" },
  { header: "DI", field: "DI" },
  { header: "DO", field: "DO" },
  { header: "Azioni", field: "id_nodo_hw" } // nessun type qui
];


let selectedHW = null;   // HW selezionato dalla tabella a sinistra
let selectedNodo = null; // ID del nodo selezionato dal <select>

// Al caricamento pagina
document.addEventListener('DOMContentLoaded', () => {
  const popupOverlay = document.getElementById('popupOverlay');
  const btnApriPopup = document.getElementById('btnApriPopup');
  const btnChiudiPopup = document.getElementById('btnChiudiPopup');

  // Apri popup
  btnApriPopup.addEventListener('click', () => {
    popupOverlay.style.display = 'flex';
  });

  // Chiudi popup
  btnChiudiPopup.addEventListener('click', () => {
    popupOverlay.style.display = 'none';
  });

  // Se clicchi fuori dal contenuto, chiudi popup
  popupOverlay.addEventListener('click', (e) => {
    if (e.target === popupOverlay) {
      popupOverlay.style.display = 'none';
    }
  });

  // Il resto del tuo codice di inizializzazione (loadNodi, loadCatalogoHW, etc.)
  // ...
});

document.addEventListener('DOMContentLoaded', async () => {
  await loadCatalogoHW();
  await loadNodi();

 
  document.getElementById('btnCreazioneAutomaticaPLC')?.addEventListener('click', creaPlcAutomatico);
  document.getElementById('aggiorna-lista-hw')?.addEventListener('click', loadCatalogoHW);
  document.getElementById('btnCreaNodo')?.addEventListener('click', creaNuovoNodo);
  document.getElementById('btnAssegnaHW')?.addEventListener('click', assegnaHardwareAlNodo);
});

/**
 * Carica il catalogo hardware
 */
async function loadCatalogoHW() {
  try {
    const data = await apiFetch('/api/catalogo_hw');
    renderDataTable({
      containerSelector: '#tabella-hw',
      columns: columnsCatalogoHW,
      data: data,
      onRowClick: (item, tr) => {
        // Rimuove la selezione da tutte le righe
        tr.parentNode.querySelectorAll('tr').forEach(r => r.classList.remove('selected'));
        // Aggiunge la selezione alla riga cliccata
        tr.classList.add('selected');
      
        // Salva la selezione logica
        selectedHW = item;
        console.log("Selezionato hardware ID:", item.id_hw);
      }
      
    });
  } catch (error) {
    console.error("Errore caricamento catalogo hw:", error);
  }
}

/**
 * Carica la lista dei nodi
 */
async function loadNodi() {
  try {
    const nodi = await apiFetch('/api/lista_nodi');
    const selectNodo = document.getElementById('selectNodo');
    selectNodo.innerHTML = '';
    nodi.forEach(n => {
      const opt = document.createElement('option');
      opt.value = n.id_nodo;
      opt.textContent = n.nome_nodo;
      selectNodo.appendChild(opt);
    });
    if (nodi.length > 0) {
      selectedNodo = nodi[0].id_nodo;
      selectNodo.value = selectedNodo;
      await loadHWAssegnato(selectedNodo);
    }
    selectNodo.addEventListener('change', async (evt) => {
      selectedNodo = evt.target.value;
      await loadHWAssegnato(selectedNodo);
    });
  } catch (error) {
    console.error("Errore caricamento nodi:", error);
  }
}

/**
 * Carica la tabella HW assegnato per il nodo
 */
async function loadHWAssegnato(idNodo) {
  try {
    const data = await apiFetch(`/api/hw_nodo_list?id_nodo=${idNodo}`);
    renderDataTable({
      containerSelector: '#tabella-hw-nodo',
      columns: columnsHWAssegnato,
      data: data,
      onRowClick: (item, tr) => {
        // Eventuali azioni al click sulla riga, se necessarie.
      }
    });
    // Dopo aver renderizzato la tabella, sostituiamo il contenuto della colonna "Azioni" con un pulsante "Elimina"
    aggiungiPulsantiElimina(data);
  } catch (error) {
    console.error("Errore caricamento HW assegnato:", error);
  }
}
function aggiungiPulsantiElimina(data) {
  const tbody = document.querySelector('#tabella-hw-nodo');
  if (!tbody) return;
  const rows = tbody.querySelectorAll('tr');
  rows.forEach((row, index) => {
    // Recupera l'oggetto dati corrispondente usando l'indice
    const item = data[index];
    // Sostituisce il contenuto dell'ultima cella (colonna Azioni) con un pulsante "Elimina"
    const cellAzioni = row.lastElementChild;
    cellAzioni.innerHTML = `<button class="btn-delete-hw" data-id="${item.id_nodo_hw}">Elimina</button>`;
  });
  
  // Aggiunge un listener a ciascun pulsante "Elimina"
  tbody.querySelectorAll('.btn-delete-hw').forEach(btn => {
    btn.addEventListener('click', async (evt) => {
      const idNodoHw = evt.target.getAttribute('data-id');
      await eliminaHWAssegnato(idNodoHw);
    });
  });
}



/**
 * Crea un nuovo nodo
 */
async function creaNuovoNodo() {
  // Usa gli ID definiti nel popup
  const nomeNodo = document.getElementById('nomeNodoPopup').value;
  const descrNodo = document.getElementById('descrNodoPopup').value;
  
  if (!nomeNodo) {
    alert("Inserisci un nome nodo");
    return;
  }
  
  try {
    const payload = {
      id_prg: 1,  // Sostituisci con il valore corretto se necessario
      nome_nodo: nomeNodo,
      descrizione: descrNodo
    };
    const data = await apiFetch('/api/crea_nodo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    console.log("Nodo creato:", data);
    // Ricarica la lista dei nodi
    await loadNodi();
    // Svuota i campi del form nel popup
    document.getElementById('nomeNodoPopup').value = '';
    document.getElementById('descrNodoPopup').value = '';
  } catch (error) {
    console.error("Errore nella creazione nodo:", error);
  }
}


/**
 * Assegna l'hardware selezionato al nodo selezionato
 */
async function assegnaHardwareAlNodo() {
  if (!selectedNodo) {
    alert("Seleziona un nodo dall'elenco (o creane uno).");
    return;
  }
  if (!selectedHW) {
    alert("Seleziona un hardware dalla tabella di sinistra.");
    return;
  }
  // Lo slot è gestito dal backend, quindi non lo passiamo
  // se però hai un campo quantita, lo passi
  const quantita = 1; // Se preferisci lasciare sempre 1
  try {
    const payload = {
      id_nodo: selectedNodo,
      id_hw: selectedHW.id_hw,
      // slot: null, // se non vuoi impostarlo
      quantita
    };
    const data = await apiFetch('/api/hw_nodo_add', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    console.log("HW assegnato:", data);
    // Ricarica la tabella
    await loadHWAssegnato(selectedNodo);
  } catch (error) {
    console.error("Errore assegnazione HW:", error);
  }
}

/**
 * Elimina un HW assegnato
 */
async function eliminaHWAssegnato(idNodoHw) {
  if (!confirm("Sei sicuro di voler eliminare questo HW assegnato?")) return;
  try {
    const data = await apiFetch(`/api/hw_nodo_list/${idNodoHw}`, {
      method: 'DELETE'
    });
    console.log("HW eliminato:", data);
    // Ricarica la tabella dopo la cancellazione
    await loadHWAssegnato(selectedNodo);
  } catch (error) {
    console.error("Errore eliminazione HW:", error);
  }
}



async function creaPlcAutomatico() {
  try {
    // La rotta non richiede parametri in input, l'id_prg verrà preso dalla sessione lato server
    const response = await apiFetch('/api/crea_plc_automatico', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    
    if (response.message) {
      alert(response.message);
      // Facoltativo: aggiorna il select dei nodi per visualizzare il nuovo nodo PLC
      loadNodi();
    } else if(response.error) {
      alert("Errore: " + response.error);
    }
  } catch (err) {
    console.error("Errore nella creazione automatica PLC:", err);
    alert("Si è verificato un errore nella creazione automatica del PLC.");
  }
}
