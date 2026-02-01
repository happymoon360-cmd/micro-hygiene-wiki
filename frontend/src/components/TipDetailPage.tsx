import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import type { TipWithRating } from '../types/tip';
import './TipDetailPage.css';

/**
 * TipDetailPage Component
 * Displays detailed information about a tip with Schema.org Article markup
 */
export default function TipDetailPage() {
  useParams<{ slugId: string }>();

  // In a real app, you would fetch the tip data based on the slugId
  // For now, we'll use mock data
  const mockTip: TipWithRating = {
    id: 123,
    title: 'How to Effectively Clean Your Kitchen',
    description: 'Learn the best practices for keeping your kitchen spotless and hygienic. This comprehensive guide covers daily maintenance, weekly deep cleaning, and tips for organizing your kitchen efficiently.',
    category: {
      id: 1,
      name: 'Kitchen',
      slug: 'kitchen',
    },
    effectiveness_avg: 4.5,
    difficulty_avg: 3.2,
    success_rate: 85,
    created_at: '2024-01-15T10:30:00Z',
    vote_count: 42,
    author: 'Micro-Hygiene Team',
    aggregateRating: {
      ratingValue: 4.5,
      reviewCount: 42,
      bestRating: 5,
      worstRating: 1,
    },
    interactionStatistic: {
      interactionType: 'https://schema.org/InteractAction',
      userInteractionCount: 42,
    },
  };

  // Generate Schema.org Article markup
  const schemaArticle = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: mockTip.title,
    description: mockTip.description,
    author: {
      '@type': 'Person',
      name: mockTip.author,
    },
    datePublished: mockTip.created_at,
    dateModified: mockTip.created_at,
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': window.location.href,
    },
    interactionStatistic: [
      {
        '@type': 'InteractionCounter',
        interactionType: {
          '@type': 'Action',
          name: 'Vote',
        },
        userInteractionCount: mockTip.interactionStatistic.userInteractionCount,
      },
    ],
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: mockTip.aggregateRating.ratingValue,
      reviewCount: mockTip.aggregateRating.reviewCount,
      bestRating: mockTip.aggregateRating.bestRating,
      worstRating: mockTip.aggregateRating.worstRating,
    },
  };

  // Update document title
  useEffect(() => {
    document.title = `${mockTip.title} - Micro-Hygiene Wiki`;
  }, [mockTip.title]);

  return (
    <>
      <Helmet>
        {/* Meta tags for SEO */}
        <title>{mockTip.title} - Micro-Hygiene Wiki</title>
        <meta name="description" content={mockTip.description} />
        <meta
          name="keywords"
          content={`${mockTip.category.name}, ${mockTip.title}, cleaning tips, hygiene, home cleaning`}
        />
        <meta name="author" content={mockTip.author} />
        <meta property="og:title" content={mockTip.title} />
        <meta property="og:description" content={mockTip.description} />
        <meta property="og:type" content="article" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={mockTip.title} />
        <meta name="twitter:description" content={mockTip.description} />

        {/* Schema.org Article markup */}
        <script type="application/ld+json">
          {JSON.stringify(schemaArticle)}
        </script>
      </Helmet>

      <div className="tip-detail-page">
        <header>
          <span className="category-badge">{mockTip.category.name}</span>
          <h1>{mockTip.title}</h1>
          <div className="meta-info">
            <span className="author">By {mockTip.author}</span>
            <span className="date">{new Date(mockTip.created_at).toLocaleDateString()}</span>
          </div>
        </header>

        <section className="content">
          <p className="description">{mockTip.description}</p>

          <div className="stats-grid">
            <div className="stat-card">
              <h3>Effectiveness</h3>
              <div className="stat-value">{mockTip.effectiveness_avg.toFixed(1)}/5</div>
            </div>
            <div className="stat-card">
              <h3>Difficulty</h3>
              <div className="stat-value">{mockTip.difficulty_avg.toFixed(1)}/5</div>
            </div>
            <div className="stat-card">
              <h3>Success Rate</h3>
              <div className="stat-value">{mockTip.success_rate.toFixed(0)}%</div>
            </div>
            <div className="stat-card">
              <h3>Votes</h3>
              <div className="stat-value">{mockTip.vote_count || 0}</div>
            </div>
          </div>

          <div className="rating-summary">
            <h3>User Rating</h3>
            <div className="rating-stars">
              {'★'.repeat(Math.round(mockTip.aggregateRating.ratingValue))}
              {'☆'.repeat(5 - Math.round(mockTip.aggregateRating.ratingValue))}
            </div>
            <p className="rating-text">
              {mockTip.aggregateRating.ratingValue} out of 5 stars (
              {mockTip.aggregateRating.reviewCount} reviews)
            </p>
          </div>
        </section>
      </div>
    </>
  );
}
