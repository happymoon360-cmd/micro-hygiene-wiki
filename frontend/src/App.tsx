import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import HomePage from './components/HomePage';
import TipDetailPage from './components/TipDetailPage';
import CategoryPage from './components/CategoryPage';
import ProductsPage from './components/ProductsPage';
import SubmitForm from './components/SubmitForm';
import MedicalDisclaimer from './components/MedicalDisclaimer';

/**
 * App Component
 * Main application with React Router configured for clean, SEO-friendly URLs
 */
export default function App() {
  return (
    <HelmetProvider>
      <Router>
        <div className="app">
          <nav className="navbar">
            <Link to="/" className="logo">
              Micro-Hygiene Wiki
            </Link>
            <div className="nav-links">
              <Link to="/">Home</Link>
              <Link to="/categories">Categories</Link>
              <Link to="/products">Products</Link>
              <Link to="/submit">Submit Tip</Link>
            </div>
          </nav>

          <Routes>
            {/* Home page */}
            <Route path="/" element={<HomePage />} />

            {/* Tip detail page with clean URL: /tips/{id}-{slug} */}
            <Route path="/tips/:slugId" element={<TipDetailPage />} />

            {/* Category page with clean URL: /categories/{slug} */}
            <Route path="/categories/:slug" element={<CategoryPage />} />

            {/* Products page */}
            <Route path="/products" element={<ProductsPage />} />

            {/* Submit tip form */}
            <Route path="/submit" element={<SubmitForm />} />

            {/* About page */}
            <Route
              path="/about"
              element={
                <div className="about-page">
                  <h1>About</h1>
                  <p>
                    Micro-Hygiene Wiki is a community-driven platform for sharing effective cleaning tips
                    and hygiene practices. Users can browse tips, vote on their effectiveness,
                    and submit their own tips for the community to review.
                  </p>
                </div>
              }
            />

            {/* 404 Not Found */}
            <Route
              path="*"
              element={
                <div className="not-found">
                  <h1>404 - Page Not Found</h1>
                  <Link to="/">Go Home</Link>
                </div>
              }
            />
          </Routes>

          <footer className="footer">
            <p>&copy; 2024 Micro-Hygiene Wiki. All rights reserved.</p>
          </footer>

          <MedicalDisclaimer />
        </div>
      </Router>
    </HelmetProvider>
  );
}

// Example URL patterns:
// - Home: /
// - Tip Detail: /tips/123-clean-kitchen-counters
// - Category: /categories/kitchen
// - Products: /products
// - Submit: /submit
// - About: /about
