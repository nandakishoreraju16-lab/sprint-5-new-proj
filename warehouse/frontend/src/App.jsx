import { useEffect, useState } from 'react'
import { Routes, Route } from 'react-router'

const API_URL = 'http://localhost:8000'

function HomePage() {
  const [status, setStatus] = useState('Checking backend...')

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((res) => res.json())
      .then((data) => setStatus(`Backend: ${data.status}, Database: ${data.database}`))
      .catch(() => setStatus('Backend not reachable. Is uvicorn running on port 8000?'))
  }, [])

  return (
    <div>
      <h1>Warehouse Dispatch Management</h1>
      <p>{status}</p>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="*" element={<h1>404 Not Found</h1>} />
    </Routes>
  )
}

export default App
