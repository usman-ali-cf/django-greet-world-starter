
import React, { useState, useEffect } from 'react'

interface Column {
  header: string
  field: string
  type?: string
}

interface DataTableMultiProps {
  columns: Column[]
  data: any[]
  onRowClick?: (item: any, tr: HTMLTableRowElement, index: number) => void
  postRender?: (tbody: HTMLTableElement, data: any[]) => void
  containerSelector?: string
}

const DataTableMulti: React.FC<DataTableMultiProps> = ({
  columns,
  data,
  onRowClick,
  postRender,
  containerSelector
}) => {
  const [selectedRows, setSelectedRows] = useState<Set<number>>(new Set())

  const handleRowClick = (item: any, index: number, event: React.MouseEvent<HTMLTableRowElement>) => {
    const tr = event.currentTarget
    
    const newSelectedRows = new Set(selectedRows)
    
    if (selectedRows.has(index)) {
      newSelectedRows.delete(index)
      tr.classList.remove('selected')
    } else {
      newSelectedRows.add(index)
      tr.classList.add('selected')
    }
    
    setSelectedRows(newSelectedRows)
    
    if (onRowClick) {
      onRowClick(item, tr, index)
    }
  }

  const renderCell = (item: any, column: Column) => {
    const value = item[column.field]
    
    switch (column.type) {
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
              className={selectedRows.has(index) ? 'selected' : ''}
              data-id={item.id || item.id_prg || item.id_hw || item.id_nodo || item.id_io}
            >
              {columns.map((column, colIndex) => (
                <td key={colIndex}>
                  {renderCell(item, column)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default DataTableMulti
