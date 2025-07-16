
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
    // Get token from localStorage
    const token = localStorage.getItem('access_token')
    
    // Prepare headers
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }
    
    // Add authorization header if token exists
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    // Make the request to Flask backend (port 5000)
    const response = await fetch(`http://localhost:5000${url}`, {
      ...options,
      headers,
    })
    
    const data = await response.json()

    if (!response.ok) {
      // If unauthorized, remove token and redirect to login
      if (response.status === 401) {
        localStorage.removeItem('access_token')
        window.location.href = '/login'
      }
      throw new Error(data.detail || data.error || 'Errore sconosciuto')
    }

    return data
  } catch (error) {
    console.error("Errore in apiFetch:", error)
    throw error
  }
}
