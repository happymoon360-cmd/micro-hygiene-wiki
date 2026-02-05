import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getTips, getCategory, type TipList } from '../api/client';

/**
 * CategoryPage Component
 * Displays all tips in a specific category with pagination
 */
export default function CategoryPage() {
  const { slug } = useParams<{ slug: string }>();
  const [tips, setTips] = useState<TipList[]>([]);
  const [category, setCategory] = useState<{ id: number; name: string; slug: string; description: string } | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCategoryAndTips();
  }, [slug]);

  const fetchCategoryAndTips = async () => {
    try {
      setLoading(true);
      setError('');

      if (!slug) {
        throw new Error('Invalid category slug');
      }
      // Fetch category details
      const categoryData = await getCategory(slug);
      setCategory(categoryData);

      // Fetch tips for this category
      const tipsData = await getTips(1);
      setTips(tipsData.results || []);
    } catch (err) {
      setLoading(false);
      setError('Failed to load category. Please try again.');
      console.error(err);
    }
  };

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (loading) {
    return <div className="category-page-loading">Loading...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!category) {
    return <div className="error-message">Category not found</div>;
  }

  return (
    <div className="category-page">
      <header>
        <h1>{category.name}</h1>
        {category.description && <p className="description">{category.description}</p>}
        <p className="tips-count">{tips.length} tips found</p>
      </header>

      <div className="tips-list">
        {tips.map((tip) => (
          <div key={tip.id} className="tip-card">
            <h3>{tip.title}</h3>
            <div className="meta">
              <span className="effectiveness">Effectiveness: {tip.effectiveness_avg.toFixed(1)}/5</span>
              <span className="difficulty">Difficulty: {tip.difficulty_avg.toFixed(1)}/5</span>
              <span className="success-rate">Success Rate: {tip.success_rate.toFixed(0)}%</span>
            </div>
            <p className="tip-description">{tip.slug}</p>
          </div>
        ))}
      </div>

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
          disabled={!category || tips.length < 20}
        >
          Next
        </button>
      </div>

      <style>{`
        .category-page {
          max-width: 800px;
          margin: 2rem auto;
          padding: 2rem;
        }

        .category-page-loading {
          text-align: center;
          padding: 2rem;
          font-size: 1.5rem;
        }

        .tips-list {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
          gap: 1.5rem;
          margin-top: 2rem;
        }

        .tip-card {
          border: 1px solid #ddd;
          border-radius: 8px;
          padding: 1.5rem;
          background-color: #f9f9f9;
        }

        .tip-card h3 {
          margin: 0 0 0.5rem 0;
          color: #333;
        }

        .meta {
          display: flex;
          gap: 0.75rem;
          margin-bottom: 0.75rem;
          font-size: 0.875rem;
        }

        .effectiveness {
          color: #28a745;
          font-weight: 600;
        }

        .difficulty {
          color: #ffc107;
          font-weight: 600;
        }

        .success-rate {
          color: #198754;
          font-weight: 600;
        }

        .pagination {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 1rem;
          margin-top: 2rem;
          padding-top: 1rem;
          border-top: 1px solid #ddd;
        }

        .pagination button {
          padding: 0.5rem 1rem;
          background-color: #007bff;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }

        .pagination button:hover:not(:disabled) {
          background-color: #0056b3;
        }

        .pagination button:disabled {
          background-color: #6c757d;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  );
}
