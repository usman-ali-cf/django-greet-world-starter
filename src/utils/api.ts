/**
 * Effettua una chiamata fetch e restituisce i dati in formato JSON.
 * Se la risposta non è ok, solleva un errore con il messaggio restituito.
 *
 * @param {string} url - L'URL della richiesta.
 * @param {RequestInit} [options={}] - Le opzioni per la chiamata fetch (metodo, headers, body, ecc.).
 * @returns {Promise<any>} - I dati della risposta in formato JSON.
 * @throws {Error} - Se la risposta non è ok o si verifica un errore.
 */
export async function apiFetch(url: string, options: RequestInit = {}): Promise<any> {
  try {
    const response = await fetch(url, options)
    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.error || 'Errore sconosciuto')
    }

    return data
  } catch (error) {
    console.error("Errore in apiFetch:", error)
    throw error
  }
}