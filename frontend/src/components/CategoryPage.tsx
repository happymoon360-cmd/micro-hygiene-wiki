import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getCategory, type CategoryDetail, type TipList } from '../api/client';

const PAGE_SIZE = 20;

/**
 * CategoryPage Component
 * Displays all tips in a specific category with pagination
 */
export default function CategoryPage() {
  const { slug } = useParams<{ slug: string }>();
  const [tips, setTips] = useState<TipList[]>([]);
  const [category, setCategory] = useState<CategoryDetail | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const totalPages = Math.max(1, Math.ceil(tips.length / PAGE_SIZE));
  const paginatedTips = tips.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE);

  useEffect(() => {
    if (currentPage > totalPages) {
      setCurrentPage(totalPages);
    }
  }, [currentPage, totalPages]);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [slug, currentPage]);

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

      // Use tips from category response
      setTips(categoryData.tips || []);
      setCurrentPage(1);
      setLoading(false);
    } catch (err) {
      setLoading(false);
      setError('Failed to load category. Please try again.');
      console.error(err);
    }
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
        {paginatedTips.map((tip) => (
          <div key={tip.id} className="tip-card">
            <h3>{tip.title}</h3>
            <div className="meta">
              <span className="effectiveness">Effectiveness: {tip.effectiveness_avg.toFixed(1)}/5</span>
              <span className="difficulty">Difficulty: {tip.difficulty_avg.toFixed(1)}/5</span>
              <span className="success-rate">Success Rate: {tip.success_rate.toFixed(0)}%</span>
            </div>
          </div>
        ))}
      </div>

      {tips.length > PAGE_SIZE && (
        <div className="pagination">
          <button onClick={() => setCurrentPage((prev) => prev - 1)} disabled={currentPage <= 1}>
            Previous
          </button>
          <span>
            Page {currentPage} / {totalPages}
          </span>
          <button onClick={() => setCurrentPage((prev) => prev + 1)} disabled={currentPage >= totalPages}>
            Next
          </button>
        </div>
      )}

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
          align-items: center;
          justify-content: center;
          gap: 0.8rem;
          margin-top: 1.5rem;
        }

        .pagination button {
          padding: 0.45rem 0.8rem;
          border-radius: 6px;
          border: 1px solid #d1d5db;
          background-color: #fff;
          cursor: pointer;
        }

        .pagination button:disabled {
          cursor: not-allowed;
          opacity: 0.5;
        }

      `}</style>
    </div>
  );
}
