
import React from 'react'

interface PlaceholderPageProps {
  pageName: string
}

const PlaceholderPage: React.FC<PlaceholderPageProps> = ({ pageName }) => {
  return (
    <div className="text-center py-16">
      <div className="text-6xl mb-4">🚧</div>
      <h2 className="text-2xl font-bold text-gray-900 mb-2">Pagina in fase di sviluppo</h2>
      <p className="text-lg text-gray-600 mb-8">
        Stiamo lavorando per offrirti presto un'interfaccia completa per <strong>{pageName}</strong>.
      </p>
      <div className="max-w-md mx-auto">
        <img 
          src="/api/placeholder/300/200" 
          alt="In costruzione"
          className="w-full opacity-80 rounded-lg"
        />
      </div>
    </div>
  )
}

export default PlaceholderPage
