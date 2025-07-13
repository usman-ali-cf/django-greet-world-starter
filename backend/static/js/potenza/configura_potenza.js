// Importa i moduli dalla cartella "standard"
import { renderDataTable } from '../standard/tables.js';
import { apiFetch } from '../standard/api.js';

// Definisci le colonne per la tabella delle utenze di potenza
const columnsPotenza = [
  { header: "Elaborato",  field: "elaborato",  type: "elaborato" },
  { header: "Nome",       field: "nome" },
  { header: "Tensione",   field: "tensione" },
  { header: "Descrizione",field: "descrizione" },
  { header: "Potenza",    field: "potenza" }
];
// Variabili globali per tenere traccia dello stato
let currentData = [];
let selectedRowIndex = -1; // Memorizza l'indice della riga attualmente selezionata
/**
 * Carica i dati delle utenze di potenza e renderizza la tabella.
 * L'endpoint /api/potenza deve restituire un oggetto JSON { utenze: [...] }.
 * @param {string} idPrg - ID del progetto.
 */
async function caricaUtenzePotenza(idPrg) {
  try {
    const response = await fetch(`/api/potenza?id_prg=${idPrg}`);
    const data = await response.json();
    if (!response.ok) {
      console.error("Errore nel caricamento delle utenze:", data.error);
      return;
    }
    renderDataTable({
      containerSelector: '#tabella-utenze',
      columns: columnsPotenza,
      data: data.utenze,
      onRowClick: selezionaRigaCallback
    });
  } catch (error) {
    console.error("Errore durante il caricamento delle utenze di potenza:", error);
  }
}

/**
 * Callback eseguita quando una riga viene cliccata.
 * Imposta l'input nascosto e aggiorna le opzioni di avviamento.
 * @param {Object} item - Dati della riga selezionata.
 * @param {HTMLElement} tr - La riga (<tr>) selezionata.
 */
function selezionaRigaCallback(item, tr, index) {
  // Imposta direttamente selectedRowIndex con l'indice passato
  
  
  const inputIdPotenza = document.querySelector('input[name="id_potenza"]');
  selectedRowIndex = index;
  if (inputIdPotenza) {
    inputIdPotenza.value = item.id_potenza;
    
    console.log(`Selezionata utenza con ID: ${item.id_potenza} (indice ${index})`);
  } else {
    console.error("Errore: Input nascosto 'id_potenza' non trovato.");
    return;
  }
  getOpzioneAvviamento(item.id_potenza);
}


/**
 * Recupera l'opzione di avviamento per l'utenza e aggiorna i radio button.
 * @param {string} idPotenza - L'ID della utenza.
 */
async function getOpzioneAvviamento(idPotenza) {
  try {
    const data = await apiFetch(`/configura_potenza/get_opzione?id_potenza=${idPotenza}`);
    const radios = document.querySelectorAll('input[name="opzione_avviamento"]');
    if (data.id_opzione_avviamento) {
      radios.forEach(radio => {
        radio.checked = (radio.value === data.id_opzione_avviamento.toString());
      });
      console.log(`Opzione selezionata automaticamente: ${data.id_opzione_avviamento}`);
    } else {
      radios.forEach(radio => radio.checked = false);
      console.log('Nessuna opzione selezionata per questa utenza.');
    }
  } catch (error) {
    console.error("Errore durante l'aggiornamento delle opzioni:", error);
  }
}

/**
 * Invia i dati per confermare l'avviamento al backend.
 */
// Funzione per confermare l'avviamento
async function confermaAvviamento() {
  const id_prg = document.querySelector('input[name="id_prg"]')?.value;
  const id_potenza = document.querySelector('input[name="id_potenza"]')?.value;
  const opzione_avviamento = document.querySelector('input[name="opzione_avviamento"]:checked')?.value;

  // Verifica che sia stata selezionata un'utenza
  if (!id_potenza) {
      document.getElementById('feedback').innerText = 'Errore: Nessuna utenza selezionata.';
      console.warn('Errore: Nessuna utenza selezionata.');
      return;
  }

  // Verifica che sia stata selezionata un'opzione di avviamento
  if (!opzione_avviamento) {
      document.getElementById('feedback').innerText = 'Errore: Nessuna opzione di avviamento selezionata.';
      console.warn('Errore: Nessuna opzione di avviamento selezionata.');
      return;
  }

  // Recupera la riga attualmente selezionata prima dell'aggiornamento
  const rigaSelezionata = document.querySelector('#tabella-utenze tr.selected');
  const idPotenzaSelezionata = rigaSelezionata ? rigaSelezionata.getAttribute('data-id') : null;

  try {
      const data = await apiFetch('/configura_potenza/assegna_avviamento', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id_prg, id_potenza, opzione_avviamento })
      });

      // Gestione risposta corretta
      document.getElementById('feedback').innerText = data.message || 'Avviamento configurato correttamente!';
      // Salva l'indice attuale prima del refresh
      
      // Ricarica e aggiorna la tabella utenze
      await caricaUtenzePotenza(id_prg);
      
      const currentIndex = selectedRowIndex;
      // Dopo il refresh, se esiste una riga successiva, selezionala
      const tutteLeRighe = Array.from(document.querySelectorAll('#tabella-utenze tr'));
      if (tutteLeRighe.length > currentIndex + 1) {
        // Usa il nuovo set di righe renderizzate
        
        if (tutteLeRighe.length > currentIndex + 1) {
          const rigaSuccessiva = tutteLeRighe[currentIndex + 1];
          rigaSuccessiva.click(); // Simula il click per attivare la callback di selezione
          rigaSuccessiva.scrollIntoView({ behavior: 'smooth', block: 'center' });
          
        } else {
                 console.log("Nessuna riga successiva disponibile.");
        }
      
      
      }
      
      }catch (error) {
      console.error("Errore durante la conferma avviamento:", error);
      document.getElementById('feedback').innerText = "Errore durante la conferma avviamento. Riprova più tardi.";
  }
}

function aggiornaLista() {
  location.reload();
}

document.addEventListener('DOMContentLoaded', () => {
  const idPrg = document.getElementById('id_prg').value;
  caricaUtenzePotenza(idPrg);

  document.getElementById('aggiorna-lista')?.addEventListener('click', aggiornaLista);
  document.getElementById('btn-conferma-avviamento')?.addEventListener('click', confermaAvviamento);
});