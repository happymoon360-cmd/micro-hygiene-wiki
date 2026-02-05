import { useState, useEffect } from 'react';
import type { Category } from '../api/client';

interface AffiliateProduct {
  id: number;
  name: string;
  affiliate_url: string;
  network: string;
  keywords: string[];
  is_active: boolean;
}

/**
 * ProductsPage Component
 * Displays all affiliate products catalog
 */
export default function ProductsPage() {
  const [products, setProducts] = useState<AffiliateProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/categories/`);
      const categoriesData: Category[] = await response.json();
      void categoriesData;

      // Extract all affiliate products from categories
      const allProductsData: AffiliateProduct[] = [];
      void allProductsData;

      // Mock affiliate products for demonstration
      // In production, these would come from the backend
      const mockProducts: AffiliateProduct[] = [
        { id: 1, name: 'Kitchen Cleaner', affiliate_url: 'https://example.com/kitchen-cleaner', network: 'Amazon', keywords: ['kitchen', 'cleaning'], is_active: true },
        { id: 2, name: 'Hand Sanitizer', affiliate_url: 'https://example.com/hand-sanitizer', network: 'Amazon', keywords: ['hand', 'sanit'], is_active: true },
        { id: 3, name: 'Disinfectant Wipes', affiliate_url: 'https://example.com/wipes', network: 'Amazon', keywords: ['disinfect', 'wipes'], is_active: true },
        { id: 4, name: 'Toothbrush Kit', affiliate_url: 'https://example.com/toothbrush', network: 'Amazon', keywords: ['toothbrush', 'dental'], is_active: true },
        { id: 5, name: 'Shampoo', affiliate_url: 'https://example.com/shampoo', network: 'Amazon', keywords: ['hair', 'shampoo'], is_active: true },
      ];

      setProducts(mockProducts);
    } catch (err) {
      setLoading(false);
      setError('Failed to load products. Please try again.');
      console.error(err);
    }
  };

  if (loading) {
    return <div className="products-page-loading">Loading products...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="products-page">
      <header>
        <h1>Affiliate Products</h1>
        <p>Recommended products for maintaining hygiene at home.</p>
      </header>

      <div className="products-list">
        {products.length === 0 ? (
          <div className="no-products">
            <p>No products available at this time.</p>
          </div>
        ) : (
          products.map((product) => (
            <div key={product.id} className="product-card">
              <h3>{product.name}</h3>
              <div className="product-meta">
                <span className="network">{product.network}</span>
                {product.is_active && <span className="active-badge">Active</span>}
              </div>
              <p className="product-keywords">
                Keywords: {product.keywords.join(', ')}
              </p>
              <a
                href={product.affiliate_url}
                target="_blank"
                rel="noopener noreferrer"
                className="affiliate-link"
              >
                View Product →
              </a>
            </div>
          ))
        )}
      </div>

      <style>{`
        .products-page {
          max-width: 900px;
          margin: 2rem auto;
          padding: 2rem;
        }

        .products-page-loading {
          text-align: center;
          padding: 2rem;
          font-size: 1.5rem;
        }

        .products-list {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
          gap: 1.5rem;
          margin-top: 2rem;
        }

        .product-card {
          border: 1px solid #ddd;
          border-radius: 8px;
          padding: 1.5rem;
          background-color: #f9f9f9;
          display: flex;
          flex-direction: column;
        }

        .product-card h3 {
          margin: 0 0 0.5rem 0;
          color: #333;
        }

        .product-meta {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.75rem;
          font-size: 0.875rem;
        }

        .network {
          color: #007bff;
          font-weight: 600;
        }

        .active-badge {
          background-color: #28a745;
          color: white;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          font-size: 0.75rem;
        }

        .product-keywords {
          color: #6c757d;
          margin-bottom: 1rem;
        }

        .affiliate-link {
          display: inline-block;
          margin-top: 1rem;
          padding: 0.5rem 1rem;
          background-color: #007bff;
          color: white;
          text-decoration: none;
          border-radius: 4px;
          font-weight: 600;
        }

        .affiliate-link:hover {
          background-color: #0056b3;
        }

        .no-products {
          grid-column: 1 / -1;
          text-align: center;
          padding: 2rem;
          color: #6c757d;
        }
      `}</style>
    </div>
  );
}
