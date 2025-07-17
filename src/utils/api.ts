
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
    const headers: Record<string, string> = {
      ...(options.headers as Record<string, string> || {}),
    }
    
    // Only set Content-Type if not FormData and not already set
    if (!(options.body instanceof FormData) && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json'
    }
    
    // Add authorization header if token exists
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
    
    // Make the request to FastAPI backend (port 8000)
    const response = await fetch(`http://localhost:8000${url}`, {
      ...options,
      headers,
    })

    // Handle different response types
    let data
    const contentType = response.headers.get('content-type')
    
    if (contentType && contentType.includes('application/json')) {
      data = await response.json()
    } else if (contentType && contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')) {
      // Handle Excel file download
      const blob = await response.blob()
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = 'Template.xlsx'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
      return { success: true, message: 'File downloaded successfully' }
    } else {
      // Handle text responses
      data = await response.text()
      try {
        data = JSON.parse(data)
      } catch {
        // If not JSON, return as text
        return { success: true, data: data }
      }
    }

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
