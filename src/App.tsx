import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Routes>
          <Route path="/" element={
            <div className="container mx-auto px-4 py-8">
              <h1 className="text-4xl font-bold text-foreground mb-4">
                Electrical Project Manager
              </h1>
              <p className="text-muted-foreground">
                React frontend is now configured and ready for migration from Flask+Jinja templates.
              </p>
            </div>
          } />
        </Routes>
      </div>
    </Router>
  )
}

export default App