import { useState, useEffect, FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { getTips, searchTips } from '../api/client';

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

  const fetchTips = async () => {
    try {
      setLoading(true);
      setError('');
      let data: any;
      if (searchQuery.trim()) {
        data = await searchTips(searchQuery);
      } else {
        data = await getTips(currentPage);
      }

      if (Array.isArray(data)) {
        data = { results: data };
      }
      setTips(data.results || []);
    } catch (err) {
      setError('Failed to load tips. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTips();
  }, [currentPage, searchQuery]);

  const handleSearch = (e: FormEvent) => {
    e.preventDefault();
    setCurrentPage(1);
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
                  <Link to={`/tips/${tip.id}-${tip.slug}`}>
                    <h3>{tip.title}</h3>
                  </Link>
                  <div className="rating">★ {tip.effectiveness_avg.toFixed(1)}</div>
                </div>
              ))
            )}
          </div>
        </section>

        {tips.length > 0 && (
          <div className="pagination">
            <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
              Previous
            </button>
            <span>Page {currentPage}</span>
            <button onClick={() => handlePageChange(currentPage + 1)} disabled={tips.length < 20}>
              Next
            </button>
          </div>
        )}
      </main>
    </>
  );
}
