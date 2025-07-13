// static/js/utenze/utenzeTable.js
import { apiFetch } from './api.js';

/**
 * Carica la tabella delle utenze dato l'ID del progetto.
 * @param {string} idPrg - L'ID del progetto.
 */
export async function caricaTabellaUtenze(idPrg) {
    try {
        const data = await apiFetch(`/api/aggiorna_tabella?id_prg=${idPrg}`);
        if (data.utenze) {
            aggiornaTabellaUI(data.utenze);
        }
    } catch (error) {
        console.error("Errore durante il caricamento delle utenze:", error);
        alert("Errore durante il caricamento delle utenze.");
    }
}

/**
 * Aggiorna il DOM della tabella delle utenze.
 * @param {Array} utenze - Array di utenze.
 */
export function aggiornaTabellaUI(utenze) {
    const tabella = document.getElementById('tabella-utenze');
    tabella.innerHTML = ''; // Svuota la tabella esistente

    utenze.forEach(utenza => {
        const { id_utenza, nome_utenza, descrizione, categoria, tipo_comando, tensione, zona, DI, DO, AI, AO, FDI, FDO, elaborata } = utenza;

        const row = document.createElement('tr');
        row.setAttribute('data-id', id_utenza);

        // Colonna "Elaborata"
        const elaborataCell = document.createElement('td');
        elaborataCell.textContent = elaborata ? '✔️' : '⚪️';
        row.appendChild(elaborataCell);

        // Aggiungi le altre colonne
        const colonne = [nome_utenza, descrizione, categoria, tipo_comando, tensione, zona, DI, DO, AI, AO, FDI, FDO];
        colonne.forEach(valore => {
            const cell = document.createElement('td');
            cell.textContent = valore || '';
            row.appendChild(cell);
        });

        tabella.appendChild(row);
    });
}
