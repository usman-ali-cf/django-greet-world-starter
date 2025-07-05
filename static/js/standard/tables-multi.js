export function renderDataTableMulti(options) {
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
  
      // Se clicco sulla riga, togglo la selezione
      tr.addEventListener('click', () => {
        tr.classList.toggle('selected');
        if (typeof onRowClick === 'function') {
          onRowClick(item, tr, index);
        }
      });
  
      columns.forEach(col => {
        const td = document.createElement('td');
        if (col.type === 'checkbox') {
          // Creiamo il pallino
          const span = document.createElement('span');
          span.classList.add('checkbox-circle');
          // Se clicco sul pallino, togglo la riga (eventualmente potresti fermare la propagazione)
          span.addEventListener('click', (e) => {
            e.stopPropagation();
            tr.classList.toggle('selected');
          });
          td.appendChild(span);
        } else if (col.type === 'elaborato') {
          td.classList.add('elaborato');
          td.textContent = item[col.field] ? '✔️' : '⚪️';
        } else {
          td.textContent = (item[col.field] ?? '');
        }
        tr.appendChild(td);
      });
  
      tbody.appendChild(tr);
    });
    
    if (typeof postRender === 'function') {
      postRender(tbody, data);
    }
  }
  