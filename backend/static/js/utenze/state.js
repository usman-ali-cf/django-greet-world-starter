// static/js/utenze/state.js

/**
 * Stato globale per la sezione "utenze".
 */
export const state = {
    ultimaCategoria: null,
    ultimaSottocategoria: null,
    ultimaOpzione: null,
    // Assicurarsi che l'elemento con id "id_prg" esista nel DOM
    idPrg: document.getElementById('id_prg') ? document.getElementById('id_prg').value : null,
};
