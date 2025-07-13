// static/js/utenze/selezioni.js
import { apiFetch } from './api.js';
import { state } from './state.js';

/**
 * Seleziona una categoria e aggiorna la lista delle sottocategorie.
 * @param {HTMLElement} riga - L'elemento <li> cliccato.
 */
export async function selezionaCategoriaById(idCategoria) {
    document.querySelectorAll('#lista-categorie li').forEach(li => li.classList.remove('selected'));
    const liCat = document.querySelector(`#lista-categorie li[data-id="${idCategoria}"]`);
    if (!liCat) {
        console.warn("Categoria non trovata per id:", idCategoria);
        return;
    }
    liCat.classList.add('selected');
    state.ultimaCategoria = idCategoria;
    console.log(`Categoria selezionata ID: ${idCategoria}`);

    // Carica le sottocategorie per questa categoria
    await aggiornaSottocategorie(idCategoria);
}

/**
 * Carica e aggiorna la lista delle sottocategorie.
 * @param {string} idCategoria - L'ID della categoria.
 * @param {Function} [callback=null] - Callback opzionale da eseguire dopo l'aggiornamento.
 */
export async function selezionaSottocategoriaById(idSottocategoria) {
    document.querySelectorAll('#lista-sottocategorie li').forEach(li => li.classList.remove('selected'));
    const liSotto = document.querySelector(`#lista-sottocategorie li[data-id="${idSottocategoria}"]`);
    if (!liSotto) {
        console.warn("Sottocategoria non trovata per id:", idSottocategoria);
        return;
    }
    liSotto.classList.add('selected');
    state.ultimaSottocategoria = idSottocategoria;
    console.log(`Sottocategoria selezionata ID: ${idSottocategoria}`);
    await apiFetch('/api/reset_opzione', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
    // Carica le opzioni per questa sottocategoria
    await aggiornaOpzioni(idSottocategoria);
}

/**
 * Aggiorna la lista delle opzioni in base all'ID della sottocategoria.
 * @param {string} idSottocategoria - L'ID della sottocategoria.
 * @param {Function} [callback=null] - Callback opzionale da eseguire dopo l'aggiornamento.
 */
export async function aggiornaSottocategorie(idCategoria) {
    try {
        const response = await fetch(`/api/sottocategorie?id_categoria=${idCategoria}`);
        const sottocategorie = await response.json();
        const lista = document.getElementById('lista-sottocategorie');
        lista.innerHTML = '';
        sottocategorie.forEach(sottocategoria => {
            const li = document.createElement('li');
            li.textContent = sottocategoria.sottocategoria;
            li.setAttribute('data-id', sottocategoria.id_sottocategoria);
            li.onclick = () => selezionaSottocategoriaById(sottocategoria.id_sottocategoria);
            lista.appendChild(li);
        });
        await apiFetch('/api/reset_opzione', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
          });
    } catch (error) {
        console.error('Errore durante il caricamento delle sottocategorie:', error);
    }
}

export async function aggiornaOpzioni(idSottocategoria) {
    try {
        const response = await fetch(`/api/opzioni?id_sottocategoria=${idSottocategoria}`);
        const opzioni = await response.json();
        const lista = document.getElementById('lista-opzioni');
        lista.innerHTML = '';
        if (opzioni.length === 0) {
            lista.innerHTML = '<li>Nessuna opzione disponibile</li>';
            return;
        }
        opzioni.forEach(opzione => {
            const li = document.createElement('li');
            li.textContent = opzione.opzione;
            li.setAttribute('data-id', opzione.id_opzione);
            // Quando si clicca, recupera l'utenza selezionata e chiama la funzione async
            li.onclick = () => {
                const trUtenza = document.querySelector('#tabella-utenze tr.selected');
                if (!trUtenza) {
                    console.error("Nessuna utenza selezionata.");
                    return;
                }
                const idUtenza = trUtenza.getAttribute('data-id');
                selezionaOpzioneById(opzione.id_opzione, idUtenza);
            };
            lista.appendChild(li);
        });
    } catch (error) {
        console.error('Errore durante il caricamento delle opzioni:', error);
    }
}

// static/js/utenze/selezioni.js
import { aggiornaDettagli } from './dettagli.js';


/**
 * Seleziona un'opzione, aggiorna lo state e manda la richiesta a Flask per aggiornare i dettagli.
 * @param {HTMLElement} riga - L'elemento <li> cliccato.
 */
export async function selezionaOpzioneById(idOpzione, idUtenza) {
    document.querySelectorAll('#lista-opzioni li').forEach(li => li.classList.remove('selected'));
    const liOpzione = document.querySelector(`#lista-opzioni li[data-id="${idOpzione}"]`);
    if (!liOpzione) {
        console.warn("Opzione non trovata per id:", idOpzione);
        return;
    }
    liOpzione.classList.add('selected');
    state.ultimaOpzione = idOpzione;
    console.log(`Opzione selezionata ID: ${idOpzione}`);

    // Recupera gli altri parametri dal DOM
    const catElement = document.querySelector('#lista-categorie li.selected');
    const sottoElement = document.querySelector('#lista-sottocategorie li.selected');
    if (!catElement || !sottoElement) {
        console.error("Categoria o sottocategoria non selezionate.");
        return;
    }
    const idCategoria = catElement.getAttribute('data-id');
    const idSottocategoria = sottoElement.getAttribute('data-id');
    const idPrg = document.getElementById('id_prg').value;

    // Aggiorna i dettagli
    await aggiornaDettagli(idUtenza, idCategoria, idSottocategoria, idOpzione, idPrg);
}

