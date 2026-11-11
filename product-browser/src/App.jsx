import { Routes, Route, Link } from 'react-router'
import ProductDetailPage from './pages/ProductDetailPage.jsx'
import ProductsPage from './pages/ProductsPage.jsx'
import BrowsePage from './pages/BrowserPage.jsx'

function App() {


  return (
    <>
      <nav>
        <Link to="/">All Products</Link> | <Link to="/browse">Browse Products</Link>
      </nav>
      <Routes>
        <Route path="/" element={<ProductsPage />} />
        <Route path="/browse" element={<BrowsePage />} />
        <Route path="/products/:id" element={<ProductDetailPage />} />
        <Route path="*" element={<h1>404 Not Found</h1>} />
      </Routes>


    </>
  )
}

export default App