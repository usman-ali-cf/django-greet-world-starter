
interface Column {
  header: string
  field: string
  type?: string
}

interface DataTableOptions {
  containerSelector: string
  columns: Column[]
  data: any[]
  onRowClick?: (item: any, tr: HTMLElement, index?: number) => void
  postRender?: (tbody: HTMLElement, data: any[]) => void
}

export function renderDataTable(options: DataTableOptions) {
  const { containerSelector, columns, data, onRowClick, postRender } = options
  const container = document.querySelector(containerSelector) as HTMLElement
  
  if (!container) {
    console.error(`Container ${containerSelector} not found`)
    return
  }

  // Clear existing content
  container.innerHTML = ''

  data.forEach((item, index) => {
    const row = document.createElement('tr')
    row.className = 'hover:bg-gray-50 cursor-pointer'
    
    if (item.id || item.id_prg || item.id_nodo || item.id_hw) {
      row.setAttribute('data-id', item.id || item.id_prg || item.id_nodo || item.id_hw)
    }

    columns.forEach(column => {
      const cell = document.createElement('td')
      cell.className = 'px-4 py-2 text-sm'
      
      if (column.type === 'elaborato') {
        cell.textContent = item[column.field] ? '✔️' : '⚪️'
      } else {
        cell.textContent = item[column.field] || ''
      }
      
      row.appendChild(cell)
    })

    if (onRowClick) {
      row.addEventListener('click', () => {
        // Remove selection from other rows
        container.querySelectorAll('tr').forEach(r => r.classList.remove('selected', 'bg-blue-100'))
        // Add selection to clicked row
        row.classList.add('selected', 'bg-blue-100')
        onRowClick(item, row, index)
      })
    }

    container.appendChild(row)
  })

  if (postRender) {
    postRender(container, data)
  }
}

interface MultiSelectDataTableOptions extends DataTableOptions {
  // Multi-select specific options
}

export function renderDataTableMulti(options: MultiSelectDataTableOptions) {
  const { containerSelector, columns, data, postRender } = options
  const container = document.querySelector(containerSelector) as HTMLElement
  
  if (!container) {
    console.error(`Container ${containerSelector} not found`)
    return
  }

  // Clear existing content
  container.innerHTML = ''

  data.forEach((item, index) => {
    const row = document.createElement('tr')
    row.className = 'hover:bg-gray-50 cursor-pointer'
    
    if (item.id_io || item.id) {
      row.setAttribute('data-id', item.id_io || item.id)
    }

    columns.forEach(column => {
      const cell = document.createElement('td')
      cell.className = 'px-4 py-2 text-sm'
      
      if (column.type === 'checkbox') {
        // Create checkbox cell for multi-select
        cell.innerHTML = '<input type="checkbox" class="mr-2">'
      } else {
        cell.textContent = item[column.field] || ''
      }
      
      row.appendChild(cell)
    })

    // Multi-select row click handler
    row.addEventListener('click', (e) => {
      e.preventDefault()
      const checkbox = row.querySelector('input[type="checkbox"]') as HTMLInputElement
      if (checkbox) {
        checkbox.checked = !checkbox.checked
      }
      row.classList.toggle('selected', checkbox?.checked)
      row.classList.toggle('bg-blue-100', checkbox?.checked)
    })

    container.appendChild(row)
  })

  if (postRender) {
    postRender(container, data)
  }
}
