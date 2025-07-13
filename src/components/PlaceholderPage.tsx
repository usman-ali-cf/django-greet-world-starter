import { useParams } from 'react-router-dom'
// Use static path for now - will work with the existing Flask static files

interface PlaceholderPageProps {
  pageName: string
}

export default function PlaceholderPage({ pageName }: PlaceholderPageProps) {
  const { id } = useParams<{ id: string }>()

  return (
    <div className="text-center py-12">
      <img 
        src="/static/img/under_construction.png"
        alt="Under Construction"
        className="mx-auto mb-6 max-w-md"
      />
      <h2 className="text-2xl font-bold mb-4">{pageName}</h2>
      <p className="text-gray-600 mb-4">
        Questa pagina è in fase di migrazione da Flask/Jinja a React.
      </p>
      {id && (
        <p className="text-sm text-gray-500">
          Progetto ID: {id}
        </p>
      )}
    </div>
  )
}