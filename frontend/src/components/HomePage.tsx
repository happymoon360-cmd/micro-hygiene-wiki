import { useState, useEffect, FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { getTips, voteTip } from '../api/client';
import MedicalDisclaimer from './MedicalDisclaimer';

/**
 * HomePage Component
 * Displays all tips with search and pagination
 */
export default function HomePage() {
  const [tips, setTips] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    fetchTips();
  }, [currentPage]);

  const fetchTips = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await getTips(currentPage);
      setTips(data.results || []);
    } catch (err) {
      setLoading(false);
      setError('Failed to load tips. Please try again.');
      console.error(err);
    }
  };

  const handleSearch = (e: FormEvent) => {
    e.preventDefault();
    const query = new FormData(e.currentTarget as HTMLFormElement).get('search');
    if (query && typeof query === 'string') {
      setSearchQuery(query);
      setCurrentPage(1);
    }
  };

  const handleVote = async (tipId: number, effectiveness: number, difficulty: number) => {
    try {
      await voteTip(tipId, { effectiveness, difficulty });
      // Refresh tips to show updated vote counts
      const data = await getTips(currentPage);
      setTips(data.results || []);
    } catch (err) {
      console.error('Failed to vote:', err);
      alert('Failed to record vote. Please try again.');
    }
  };

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <>
      <Helmet>
        <title>Micro-Hygiene Wiki - Home</title>
        <meta
          name="description"
          content="Discover effective cleaning tips and hygiene practices for your home. Community-voted advice for maintaining a clean and healthy living environment."
        />
        <meta
          name="keywords"
          content="cleaning tips, hygiene, home cleaning, kitchen hygiene, bathroom hygiene, household tips"
        />
      </Helmet>

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

        <main>
          <header className="hero">
            <h1>Micro-Hygiene Wiki</h1>
            <p className="subtitle">
              Community-voted cleaning tips and hygiene practices for a healthier home
            </p>
          </header>

          <section className="search-section">
            <form onSubmit={handleSearch}>
              <input
                type="search"
                placeholder="Search tips..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <button type="submit">Search</button>
            </form>
          </section>

          <section className="featured-tips">
            <h2>Featured Tips</h2>
            <div className="tip-grid">
              {loading ? (
                <div className="loading">Loading tips...</div>
              ) : error ? (
                <div className="error-message">{error}</div>
              ) : tips.length === 0 ? (
                <div className="no-tips">No tips found</div>
              ) : (
                tips.map((tip: any) => (
                  <div key={tip.id} className="tip-card">
                    <span className="category-badge">{tip.category_name}</span>
                    <h3>{tip.title}</h3>
                    <div className="rating">★ {tip.effectiveness_avg.toFixed(1)}</div>
                    <Link to={`/tips/${tip.id}-${tip.slug}`}>
                      <button onClick={() => handleVote(tip.id, tip.effectiveness_avg, tip.difficulty_avg)}>
                        ▲
                      </button>
                      <button onClick={() => handleVote(tip.id, tip.effectiveness_avg, tip.difficulty_avg)}>
                        ▼
                      </button>
                    </Link>
                  </div>
                ))
              )}
            </div>
          </section>

          {tips.length > 0 && (
            <div className="pagination">
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 1}
              >
                Previous
              </button>
              <span>Page {currentPage}</span>
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={tips.length < 20}
              >
                Next
              </button>
            </div>
          )}
        </main>

        <footer className="footer">
          <p>&copy; 2024 Micro-Hygiene Wiki. All rights reserved.</p>
        </footer>

        <MedicalDisclaimer />
      </div>
    </>
  );
}
