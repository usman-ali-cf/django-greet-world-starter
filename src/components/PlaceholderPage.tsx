
import React from 'react'
import underConstruction from '../img/under_construction.png'

interface PlaceholderPageProps {
  pageName: string
}

const PlaceholderPage: React.FC<PlaceholderPageProps> = ({ pageName }) => {
  return (
    <div className="text-center py-16">
      <h2 className="text-2xl font-bold text-gray-900 mb-2">🚧 Pagina in fase di sviluppo</h2>
      <p className="text-lg text-gray-600 mb-8">
        Stiamo lavorando per offrirti presto un'interfaccia completa per <strong>{pageName}</strong>.
      </p>
      <div className="max-w-md mx-auto">
        <img 
          src={underConstruction} 
          alt="In costruzione"
          className="opacity-80 rounded-lg"
          style={{ width: '400px', height: '600px' }}
        />
      </div>
    </div>
  )
}

export default PlaceholderPage
