// static/js/utenze/main.js
import { caricaTabellaUtenze } from './utenzeTable.js';
import { state } from './state.js';
import { selezionaCategoriaById, selezionaSottocategoriaById, selezionaOpzioneById } from './selezioni.js';
import { aggiornaDettagli } from './dettagli.js';

import { apiFetch } from './api.js';  // Usato per uniformare le chiamate



// Funzione per gestire la selezione dell'utenza (già definita)
async function selezionaUtenza(riga) {
    // Deseleziona eventuali righe precedenti
    document.querySelectorAll('#tabella-utenze tr').forEach(row => row.classList.remove('selected'));
    riga.classList.add('selected');

    const idUtenza = riga.getAttribute('data-id');
    console.log(`Selezionata utenza con ID: ${idUtenza}`);

    try {
        const response = await fetch(`/api/selezione_utenza?id_utenza=${idUtenza}`);
        const data = await response.json();
        if (!response.ok) {
            console.error("Errore nella selezione dell'utenza:", data.error);
            alert(`Errore: ${data.error}`);
            return;
        }

        // Estrae i parametri della selezione
        let { id_cat, id_sottocat, id_opzione } = data.selezione || {};
        
        // Se manca l'opzione, usa l'ultima selezione memorizzata (se presente)
        if (!id_opzione && state.ultimaOpzione) {
            console.warn("id_opzione non restituito, uso valore memorizzato:", state.ultimaOpzione);
            id_opzione = state.ultimaOpzione;
        }

        // Aggiorna le variabili globali solo se sono presenti valori validi
        if (id_cat) state.ultimaCategoria = id_cat;
        if (id_sottocat) state.ultimaSottocategoria = id_sottocat;
        if (id_opzione) state.ultimaOpzione = id_opzione;

        // Procedi in sequenza solo se sono definiti
        if (id_cat) await selezionaCategoriaById(id_cat);
        if (id_sottocat) await selezionaSottocategoriaById(id_sottocat);
        if (id_opzione) await selezionaOpzioneById(id_opzione, idUtenza);

    } catch (error) {
        console.error("Errore durante la selezione dell'utenza:", error);
        alert("Errore durante la selezione dell'utenza. Riprova più tardi.");
    }
}




/**
 * Funzione di conferma aggiornata.
 * Usa apiFetch per inviare la richiesta e aggiorna la tabella, selezionando la riga successiva.
 */
async function conferma() {
    try {
        const rigaSelezionata = document.querySelector('#tabella-utenze tr.selected');
        if (!rigaSelezionata) {
            alert("Seleziona prima un'utenza.");
            return;
        }
        const idUtenzaSelezionata = rigaSelezionata.getAttribute('data-id');
        console.log("Conferma: utenza selezionata", idUtenzaSelezionata);
        
        // Usa apiFetch per uniformità nella gestione degli errori
        const data = await apiFetch('/api/conferma', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        console.log("Conferma riuscita:", data);

        // Aggiorna la tabella dopo la conferma
        await caricaTabellaUtenze(state.idPrg);

        // Se esiste una riga successiva, la seleziona automaticamente
        const tutteLeRighe = Array.from(document.querySelectorAll('#tabella-utenze tr'));
        const indiceCorrente = tutteLeRighe.findIndex(row => row.getAttribute('data-id') === idUtenzaSelezionata);
        if (indiceCorrente !== -1 && indiceCorrente < tutteLeRighe.length - 1) {
            const rigaSuccessiva = tutteLeRighe[indiceCorrente + 1];
            await selezionaUtenza(rigaSuccessiva);
            rigaSuccessiva.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            console.log("Nessuna riga successiva disponibile.");
        }
    } catch (error) {
        console.error("Errore durante la conferma:", error);
        alert("Errore durante la conferma. Riprova più tardi.");
    }
}

/**
 * Inizializza l'app aggiungendo gli event listener.
 */
document.addEventListener('DOMContentLoaded', () => {
    const idPrg = document.getElementById('id_prg').value;
    caricaTabellaUtenze(idPrg);

    // Listener per la tabella delle utenze (rimane invariato)
    const tabellaUtenze = document.getElementById('tabella-utenze');
    if (tabellaUtenze) {
        tabellaUtenze.addEventListener('click', (event) => {
            const riga = event.target.closest('tr');
            if (riga && riga.hasAttribute('data-id')) {
                selezionaUtenza(riga);
            }
        });
    }

    // Listener per la lista delle categorie (usa la nuova funzione)
    const listaCategorie = document.getElementById('lista-categorie');
    if (listaCategorie) {
        listaCategorie.addEventListener('click', (event) => {
            const li = event.target.closest('li');
            if (li) {
                const idCategoria = li.getAttribute('data-id');
                selezionaCategoriaById(idCategoria);
            }
        });
    }

    // Listener per il pulsante "Conferma"
    const btnConferma = document.getElementById('btn-conferma');
    if (btnConferma) {
        btnConferma.addEventListener('click', conferma);
    }

    // Listener per il pulsante "Pre-elabora Tutte"
    const btnPreElabora = document.getElementById('btnPreElabora');
    const statusDiv = document.getElementById('elabStatus');
    if (btnPreElabora) {
        btnPreElabora.addEventListener('click', async () => {
            btnPreElabora.disabled = true;
            btnPreElabora.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Elaborazione...';
            statusDiv.style.display = 'block';
            statusDiv.textContent = 'Elaborazione in corso...';

            try {
                const data = await apiFetch('/api/preelabora_utenze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({})
                });

                statusDiv.className = 'alert alert-success mt-2';
                statusDiv.innerHTML = `
                    ${data.message}
                    <button type="button" class="close" onclick="this.parentElement.style.display='none'">&times;</button>
                `;
                setTimeout(() => caricaTabellaUtenze(state.idPrg), 1000);
            } catch (error) {
                statusDiv.className = 'alert alert-danger mt-2';
                statusDiv.textContent = `Errore: ${error.message}`;
            } finally {
                btnPreElabora.disabled = false;
                btnPreElabora.innerHTML = '<i class="fas fa-cogs"></i> Pre-elabora Tutte';
            }
        });
    }
});
