import { useEffect, useState } from 'react';
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';
import { getCategories, type Category } from '../api/client';

export default function CategoriesListPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string>('');

  const fetchCategories = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await getCategories();
      setCategories(data);
    } catch (err) {
      setError('Failed to load categories. Please try again.');
      console.error('Failed to load categories:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  return (
    <div className="categories-list-page">
      <Helmet>
        <title>Micro-Hygiene Wiki - Categories</title>
        <meta
          name="description"
          content="Browse all micro-hygiene categories and find community-voted cleaning tips by room, surface, and scenario."
        />
        <meta
          name="keywords"
          content="hygiene categories, cleaning categories, micro-hygiene, home cleaning, household tips"
        />
      </Helmet>

      <header className="categories-header">
        <h1>Categories</h1>
        <p className="subtitle">Explore tips grouped by where you clean and what you maintain.</p>
      </header>

      {loading ? (
        <div className="categories-loading">Loading categories...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : categories.length === 0 ? (
        <div className="categories-empty">No categories found.</div>
      ) : (
        <div className="categories-grid">
          {categories.map((cat) => (
            <Link key={cat.id} to={`/categories/${cat.slug}`} className="category-card">
              <div className="card-top">
                <h2>{cat.name}</h2>
                <span className="tips-count">{(cat.tips_count ?? 0).toLocaleString()} tips</span>
              </div>
              {cat.description ? (
                <p className="description">{cat.description}</p>
              ) : (
                <p className="description description-muted">No description yet.</p>
              )}
              <span className="card-cta">View tips →</span>
            </Link>
          ))}
        </div>
      )}

      <style>{`
        .categories-list-page {
          max-width: 980px;
          margin: 2rem auto;
          padding: 2rem;
        }

        .categories-header {
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
          margin-bottom: 1.5rem;
        }

        .categories-header h1 {
          margin: 0;
          color: #1f2937;
          letter-spacing: -0.02em;
        }

        .subtitle {
          margin: 0;
          color: #6b7280;
          max-width: 70ch;
        }

        .categories-loading,
        .categories-empty {
          text-align: center;
          padding: 2rem;
          color: #4b5563;
          font-size: 1.1rem;
        }

        .categories-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
          gap: 1.2rem;
          margin-top: 1rem;
        }

        .category-card {
          border: 1px solid #e5e7eb;
          border-radius: 12px;
          padding: 1.15rem 1.15rem 1rem;
          background: linear-gradient(180deg, #ffffff 0%, #f9fafb 100%);
          text-decoration: none;
          color: inherit;
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
          min-height: 150px;
          transition: transform 140ms ease, box-shadow 140ms ease, border-color 140ms ease;
        }

        .category-card:hover {
          transform: translateY(-2px);
          border-color: #d1d5db;
          box-shadow: 0 10px 30px rgba(17, 24, 39, 0.08);
        }

        .category-card:focus-visible {
          outline: 3px solid rgba(37, 99, 235, 0.35);
          outline-offset: 2px;
        }

        .card-top {
          display: flex;
          justify-content: space-between;
          gap: 0.75rem;
          align-items: baseline;
        }

        .category-card h2 {
          margin: 0;
          font-size: 1.1rem;
          color: #111827;
        }

        .tips-count {
          font-size: 0.85rem;
          color: #1f2937;
          background: rgba(17, 24, 39, 0.06);
          padding: 0.25rem 0.5rem;
          border-radius: 999px;
          white-space: nowrap;
        }

        .description {
          margin: 0;
          color: #4b5563;
          line-height: 1.45;
          display: -webkit-box;
          -webkit-line-clamp: 3;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }

        .description-muted {
          color: #9ca3af;
        }

        .card-cta {
          margin-top: auto;
          color: #2563eb;
          font-weight: 600;
        }

        @media (max-width: 600px) {
          .categories-list-page {
            padding: 1.25rem;
            margin: 1rem auto;
          }

          .categories-grid {
            gap: 0.9rem;
          }
        }
      `}</style>
    </div>
  );
}
