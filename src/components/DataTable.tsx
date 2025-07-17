
import React, { useState, useEffect } from 'react'

interface Column {
  header: string
  field: string
  type?: string
}

interface DataTableProps {
  columns: Column[]
  data: any[]
  onRowClick?: (item: any, tr: HTMLTableRowElement, index: number) => void
  postRender?: (tbody: HTMLTableElement, data: any[]) => void
  containerSelector?: string
}

const DataTable: React.FC<DataTableProps> = ({
  columns,
  data,
  onRowClick,
  postRender,
  containerSelector
}) => {
  const [selectedIndex, setSelectedIndex] = useState<number>(-1)

  const handleRowClick = (item: any, index: number, event: React.MouseEvent<HTMLTableRowElement>) => {
    const tr = event.currentTarget
    
    // Remove selection from all rows
    const tbody = tr.parentNode as HTMLTableElement
    tbody.querySelectorAll('tr').forEach(r => r.classList.remove('selected'))
    
    // Add selection to clicked row
    tr.classList.add('selected')
    setSelectedIndex(index)
    
    if (onRowClick) {
      onRowClick(item, tr, index)
    }
  }

  const renderCell = (item: any, column: Column) => {
    const value = item[column.field]
    
    switch (column.type) {
      case 'elaborato':
        return (
          <div className="elaborato">
            {value ? <span className="spunta">✓</span> : <span className="vuoto">○</span>}
          </div>
        )
      case 'checkbox':
        return (
          <div className="checkbox-circle"></div>
        )
      default:
        return value || ''
    }
  }

  useEffect(() => {
    if (postRender) {
      const container = document.querySelector(containerSelector || '') as HTMLTableElement
      if (container) {
        postRender(container, data)
      }
    }
  }, [data, postRender, containerSelector])

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            {columns.map((column, index) => (
              <th key={index}>{column.header}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr
              key={index}
              onClick={(e) => handleRowClick(item, index, e)}
              className={selectedIndex === index ? 'selected' : ''}
              data-id={item.id || item.id_prg || item.id_hw || item.id_nodo || item.id_io}
            >
              {columns.map((column, colIndex) => (
                <td key={colIndex}>
                  {renderCell(item, column)}
                </td>
              ))}
            </tr>
          ))}
          {/* Add extra space at the bottom */}
          <tr>
            <td colSpan={columns.length} style={{ height: '32px', backgroundColor: 'transparent' }}></td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}

export default DataTable
