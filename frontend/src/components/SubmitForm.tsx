import { useState, FormEvent, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * SubmitForm Component
 * Form for submitting new tips with Cloudflare Turnstile CAPTCHA
 */
export default function SubmitForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category_id: 0,
  });
  const [turnstileToken, _setTurnstileToken] = useState('');
  const [turnstileError, setTurnstileError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [categories, setCategories] = useState<{ id: number; name: string; slug: string }[]>([]);

  // Load categories on mount
  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/categories/`);
      const data = await response.json();
      setCategories(data);
    } catch (err) {
      console.error('Failed to load categories:', err);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!turnstileToken) {
      setTurnstileError('Please complete the CAPTCHA verification');
      return;
    }

    setIsSubmitting(true);
    setError('');
    setTurnstileError('');

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/tips/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          turnstile_token: turnstileToken,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to create tip');
        if (errorData.error?.includes('turnstile')) {
          setTurnstileError(errorData.error);
        }
      } else {
        // Success - redirect to home
        navigate('/');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
      setTurnstileError('');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="submit-form-container">
      <h1>Submit a New Tip</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            id="title"
            type="text"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            required
            placeholder="e.g., How to clean kitchen counters efficiently"
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description *</label>
          <textarea
            id="description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            required
            rows={6}
            placeholder="Provide detailed instructions..."
          />
        </div>

        <div className="form-group">
          <label htmlFor="category">Category *</label>
          <select
            id="category"
            value={formData.category_id}
            onChange={(e) => setFormData({ ...formData, category_id: parseInt(e.target.value) })}
            required
          >
            <option value="">Select a category</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Cloudflare Turnstile CAPTCHA *</label>
          <div className="turnstile-container" id="turnstile-widget"></div>
          {turnstileError && <div className="error-message">{turnstileError}</div>}
        </div>

        {error && <div className="error-message">{error}</div>}

        <button type="submit" disabled={isSubmitting || !turnstileToken}>
          {isSubmitting ? 'Submitting...' : 'Submit Tip'}
        </button>
      </form>

      <style>{`
        .submit-form-container {
          max-width: 600px;
          margin: 2rem auto;
          padding: 2rem;
        }

        .form-group {
          margin-bottom: 1.5rem;
        }

        label {
          display: block;
          margin-bottom: 0.5rem;
          font-weight: 600;
        }

        input, textarea, select {
          width: 100%;
          padding: 0.75rem;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 1rem;
        }

        textarea {
          min-height: 150px;
          resize: vertical;
        }

        button {
          width: 100%;
          padding: 0.75rem 1.5rem;
          background-color: #007bff;
          color: white;
          border: none;
          border-radius: 4px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
        }

        button:hover:not(:disabled) {
          background-color: #0056b3;
        }

        button:disabled {
          background-color: #6c757d;
          cursor: not-allowed;
        }

        .error-message {
          color: #dc3545;
          background-color: #f8d7da;
          padding: 0.75rem;
          border-radius: 4px;
          margin-top: 1rem;
        }

        .turnstile-container {
          margin-bottom: 1.5rem;
        }
      `}</style>
    </div>
  );
}
