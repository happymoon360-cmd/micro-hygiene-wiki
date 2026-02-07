import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import { Helmet } from 'react-helmet-async';
import { getTip, voteTip, type TipDetail } from '../api/client';

/**
 * TipDetailPage Component
 * Displays detailed information about a tip with voting
 */
export default function TipDetailPage() {
  const { slugId } = useParams<{ slugId: string }>();
  const [tip, setTip] = useState<TipDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [voting, setVoting] = useState<{ id: number } | null>(null);
  const [effectivenessRating, setEffectivenessRating] = useState<number>(3);
  const [difficulty, setDifficulty] = useState<number>(3);

  const tipIdInitializedRef = useRef<number | null>(null);

  const clampRating = (value: number) => Math.min(5, Math.max(1, Math.round(value)));

  useEffect(() => {
    fetchTip();
  }, [slugId]);

  useEffect(() => {
    if (!tip) return;
    if (tipIdInitializedRef.current === tip.id) return;
    tipIdInitializedRef.current = tip.id;

    setEffectivenessRating(clampRating(tip.effectiveness_avg));
    setDifficulty(clampRating(tip.difficulty_avg));
  }, [tip]);

  const fetchTip = async () => {
    try {
      setLoading(true);
      setError('');

      // Parse slugId to extract numeric ID (format: {id}-{slug})
      if (!slugId) {
        throw new Error('Invalid tip ID');
      }
      const tipId = slugId.split('-')[0];

      if (!tipId || isNaN(parseInt(tipId))) {
        throw new Error('Invalid tip ID');
      }

      const data = await getTip(parseInt(tipId));
      setTip(data);
      setLoading(false);
    } catch (err) {
      setLoading(false);
      setError('Failed to load tip. Please try again.');
      console.error(err);
    }
  };

  const handleVote = async (effectiveness: number, difficulty: number) => {
    if (!tip) return;

    setVoting({ id: tip.id });

    try {
      await voteTip(tip.id, {
        effectiveness: clampRating(effectiveness),
        difficulty: clampRating(difficulty),
      });
      // Refresh tip data to show updated vote counts
      const tipId = slugId?.split('-')[0];
      if (!tipId) {
        throw new Error('Invalid tip ID');
      }
      const data = await getTip(parseInt(tipId));
      setTip(data);
      setVoting(null);
    } catch (err) {
      setVoting(null);
      alert('Failed to record vote. Please try again.');
    }
  };

  if (loading) {
    return <div className="tip-detail-page-loading">Loading tip...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!tip) {
    return <div className="error-message">Tip not found</div>;
  }

  return (
    <>
      <Helmet>
        <title>{tip.title} - Micro-Hygiene Wiki</title>
        <meta
          name="description"
          content={tip.description}
        />
        <meta
          name="keywords"
          content={`${tip.category.name}, ${tip.title}, cleaning tips, hygiene`}
        />
      </Helmet>

      <div className="tip-detail-page">
        <header>
          <span className="category-badge">{tip.category.name}</span>
          <h1>{tip.title}</h1>
          <div className="meta-info">
            <span>By Community</span>
            <span>•</span>
            <span>{new Date(tip.created_at).toLocaleDateString()}</span>
          </div>
        </header>

        <section className="content">
          <p className="tip-description">{tip.description}</p>

          <div className="stats-grid">
            <div className="stat-card">
              <h3>Effectiveness</h3>
              <div className="stat-value">{tip.effectiveness_avg.toFixed(1)}/5</div>
            </div>
            <div className="stat-card">
              <h3>Difficulty</h3>
              <div className="stat-value">{tip.difficulty_avg.toFixed(1)}/5</div>
            </div>
            <div className="stat-card">
              <h3>Success Rate</h3>
              <div className="stat-value">{tip.success_rate.toFixed(0)}%</div>
            </div>
            <div className="stat-card">
              <h3>Votes</h3>
              <div className="stat-value">{tip.vote_count}</div>
            </div>
          </div>

          <div className="voting-section">
            <h3>Rate this Tip</h3>
            <p className="voting-subtitle">How effective was this tip? (1-5) How difficult? (1-5)</p>

            <div className="difficulty-rating">
              <p>How difficult was this?</p>
              <button
                onClick={() => {
                  setDifficulty(1);
                  handleVote(effectivenessRating, 1);
                }}
                disabled={voting?.id === tip.id}
              >
                Very Easy (1)
              </button>
              <button
                onClick={() => {
                  setDifficulty(2);
                  handleVote(effectivenessRating, 2);
                }}
                disabled={voting?.id === tip.id}
              >
                Easy (2)
              </button>
              <button
                onClick={() => {
                  setDifficulty(3);
                  handleVote(effectivenessRating, 3);
                }}
                disabled={voting?.id === tip.id}
              >
                Average (3)
              </button>
              <button
                onClick={() => {
                  setDifficulty(4);
                  handleVote(effectivenessRating, 4);
                }}
                disabled={voting?.id === tip.id}
              >
                Hard (4)
              </button>
              <button
                onClick={() => {
                  setDifficulty(5);
                  handleVote(effectivenessRating, 5);
                }}
                disabled={voting?.id === tip.id}
              >
                Very Hard (5)
              </button>
            </div>

            <div className="vote-buttons">
              <button
                onClick={() => {
                  setEffectivenessRating(5);
                  handleVote(5, difficulty);
                }}
                disabled={voting?.id === tip.id}
              >
                ▲ Very Effective (5)
              </button>
              <button
                onClick={() => {
                  setEffectivenessRating(4);
                  handleVote(4, difficulty);
                }}
                disabled={voting?.id === tip.id}
              >
                ▲ Effective (4)
              </button>
              <button
                onClick={() => {
                  setEffectivenessRating(3);
                  handleVote(3, difficulty);
                }}
                disabled={voting?.id === tip.id}
              >
                ▲ Average (3)
              </button>
              <button
                onClick={() => {
                  setEffectivenessRating(2);
                  handleVote(2, difficulty);
                }}
                disabled={voting?.id === tip.id}
              >
                ▲ Less Effective (2)
              </button>
              <button
                onClick={() => {
                  setEffectivenessRating(1);
                  handleVote(1, difficulty);
                }}
                disabled={voting?.id === tip.id}
              >
                ▲ Not Effective (1)
              </button>
            </div>
          </div>
        </section>

        {/* Schema.org Article markup */}
        <script type="application/ld+json">
          {JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Article',
            headline: tip.title,
            description: tip.description,
            author: {
              '@type': 'Person',
              name: 'Community',
            },
            datePublished: tip.created_at,
            dateModified: tip.created_at,
            mainEntityOfPage: {
              '@type': 'WebPage',
              '@id': window.location.href,
            },
            aggregateRating: {
              '@type': 'AggregateRating',
              ratingValue: tip.effectiveness_avg,
              reviewCount: tip.vote_count,
              bestRating: 5,
              worstRating: 1,
            },
          })}
        </script>
      </div>
    </>
  );
}
