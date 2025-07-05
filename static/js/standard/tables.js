// static/js/standard/tables.js


 /**
 * Rende una tabella dinamica basata sui dati forniti.
 *
 * @param {Object} options - Opzioni per la tabella.
 * @param {string} options.containerSelector - Il selettore del <tbody> dove inserire le righe.
 * @param {Array} options.columns - Array di oggetti che definiscono le colonne.
 *        Ogni oggetto deve avere:
 *          - header: (string) il testo dell'intestazione.
 *          - field: (string) il nome della proprietà nell'oggetto dati.
 *          - type (opzionale): se "elaborato", il contenuto viene gestito in modo speciale.
 * @param {Array} options.data - Array di oggetti dati.
 * @param {function} [options.onRowClick] - Callback chiamata al clic della riga, riceve (item, tr).
 */
 export function renderDataTable(options) {
  const { containerSelector, columns, data, onRowClick, postRender } = options;
  const tbody = document.querySelector(containerSelector);
  if (!tbody) {
    console.error(`Container non trovato per il selettore: ${containerSelector}`);
    return;
  }
  
  // Svuota il contenitore
  tbody.innerHTML = '';
  
  data.forEach((item, index) => {
    const tr = document.createElement('tr');
    
    if (typeof onRowClick === 'function') {
      tr.addEventListener('click', () => {
        // Toggle per supportare la multiselezione:
        if (tr.classList.contains('selected')) {
          tr.classList.remove('selected');
        } else {
          // Se vuoi supportare la selezione multipla, rimuovi la linea seguente
          // tbody.querySelectorAll('tr').forEach(row => row.classList.remove('selected'));
          tr.classList.add('selected');
        }
        onRowClick(item, tr, index);
      });
    }
    
    columns.forEach(col => {
      const td = document.createElement('td');
      if (col.type === 'elaborato') {
        td.classList.add('elaborato');
        td.textContent = item[col.field] ? '✔️' : '⚪️';
      } else {
        td.textContent = (item[col.field] !== undefined && item[col.field] !== null)
          ? item[col.field] : '';
      }
      tr.appendChild(td);
    });
    
    tbody.appendChild(tr);
  });
  
  // Callback postRender, ad esempio per impostare attributi data-id
  if (typeof postRender === 'function') {
    postRender(tbody, data);
  }
}


