// static/js/utenze/dettagli.js

import { apiFetch } from './api.js';
import { state } from './state.js';

/**
 * Renderizza i dettagli nel container dedicato.
 * @param {Array} dettagli - Array dei dettagli.
 */
function renderDettagli(dettagli) {
    const container = document.getElementById('dettagli-container');
    container.innerHTML = '';
    console.log("Pulisco il container dei dettagli.");
    
    dettagli.forEach(dettaglio => {
        const div = document.createElement('div');
        div.classList.add('dettaglio');
        
        // Costruisce il markup per il tipo e la descrizione
        let html = `<strong>${dettaglio.tipo}:</strong> ${dettaglio.descrizione}<br>`;
        
        // Se esistono simboli, crea anche le anteprime delle immagini
        if (dettaglio.simboli && Array.isArray(dettaglio.simboli) && dettaglio.simboli.length > 0) {
            html += `<strong></strong> `;  /* Simboli: inserire tra i 2 strong */
            dettaglio.simboli.forEach(simbolo => {
                // Costruisce il percorso dell'immagine in base al nome del simbolo
                html += `<img src="/static/img/${simbolo}.png" alt="${simbolo}" style="width:75px; height:75px; margin-right:5px;border: 2px solid #000; box-shadow: 0px 0px 5px rgba(0,0,0,0.5); filter: invert(0) brightness(1) contrast(1);"> `;


            });
        } else {
            html += `<strong>Simboli:</strong> Nessun simbolo`;
        }
        
        div.innerHTML = html;
        container.appendChild(div);
    });
    
    console.log("Nuovi dettagli renderizzati:", container.innerHTML);
}

/**
 * Aggiorna i dettagli richiamando l'API e usando renderDettagli per visualizzarli.
 * @param {string} id_utenza - ID dell'utenza selezionata.
 * @param {string} id_categoria - ID della categoria selezionata.
 * @param {string} id_sottocategoria - ID della sottocategoria selezionata.
 * @param {string} id_opzione - ID dell'opzione selezionata.
 * @param {string} id_prg - ID del progetto.
 */
export async function aggiornaDettagli(id_utenza, id_categoria, id_sottocategoria, id_opzione, id_prg) {
    try {
        const url = `/api/dettagli?id_utenza=${id_utenza}&id_categoria=${id_categoria}&id_sottocategoria=${id_sottocategoria}&id_opzione=${id_opzione}&id_prg=${id_prg}&t=${Date.now()}`;
        const response = await fetch(url);
        const data = await response.json();
        console.log("Risposta da /api/dettagli:", data);
    
        if (!data || !Array.isArray(data.dettagli)) {
            throw new Error("La chiave 'dettagli' non contiene un array o manca.");
        }
    
        renderDettagli(data.dettagli);
    } catch (error) {
        console.error("Errore durante il caricamento dei dettagli:", error);
        document.getElementById('dettagli-container').innerHTML = "<p>Errore durante il caricamento dei dettagli.</p>";
    }
}

/**
 * Gestisce la conferma dell'operazione.
 */
export async function conferma() {
    try {
        const response = await apiFetch('/api/conferma', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        console.log("Conferma riuscita:", response);
        // Dopo la conferma si possono aggiungere ulteriori aggiornamenti, ad esempio aggiornare la tabella
    } catch (error) {
        console.error("Errore durante la conferma:", error);
        alert(`Errore: ${error.message}`);
    }
}
