import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import HomePage from './components/HomePage';
import TipDetailPage from './components/TipDetailPage';

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
              <Link to="/about">About</Link>
            </div>
          </nav>

          <Routes>
            {/* Clean, SEO-friendly URLs */}
            {/* Home page */}
            <Route path="/" element={<HomePage />} />

            {/* Tip detail page with clean URL: /tips/:id-:slug */}
            <Route path="/tips/:slugId" element={<TipDetailPage />} />

            {/* Category page with clean URL: /categories/:slug */}
            <Route path="/categories/:slug" element={<div>Category Page</div>} />

            {/* About page */}
            <Route path="/about" element={<div>About Page</div>} />

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
        </div>
      </Router>
    </HelmetProvider>
  );
}

// Example of how to generate clean links in other components:
// <Link to={createTipUrl(tip.title, tip.id)}>{tip.title}</Link>
// This generates: /tips/123-clean-tip-title

// Example URL patterns:
// - Home: /
// - Tip Detail: /tips/123-how-to-clean-kitchen
// - Category: /categories/kitchen
// - About: /about
