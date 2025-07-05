// static/js/utenze/api.js

/**
 * Wrapper per le chiamate API.
 * @param {string} url - L'URL della richiesta.
 * @param {object} [options={}] - Opzioni per fetch.
 * @returns {Promise<any>} - I dati parsati dalla risposta JSON.
 * @throws {Error} - Se la risposta non è OK o si verifica un errore.
 */
export async function apiFetch(url, options = {}) {
    try {
        const response = await fetch(url, options);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Errore sconosciuto');
        }
        return data;
    } catch (error) {
        console.error("Errore in apiFetch:", error);
        throw error;
    }
}
