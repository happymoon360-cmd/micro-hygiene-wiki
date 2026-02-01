import { Helmet } from 'react-helmet-async';
import './HomePage.css';

/**
 * HomePage Component
 * Displays to home page with a list of tips
 */
export default function HomePage() {
  return (
    <>
      <Helmet>
        {/* Meta tags for SEO */}
        <title>Micro-Hygiene Wiki - Home</title>
        <meta
          name="description"
          content="Discover effective cleaning tips and hygiene practices for your home. Community-voted advice for maintaining a clean and healthy living environment."
        />
        <meta
          name="keywords"
          content="cleaning tips, hygiene, home cleaning, kitchen cleaning, bathroom cleaning, household tips"
        />
        <meta name="author" content="Micro-Hygiene Wiki" />
        <meta property="og:title" content="Micro-Hygiene Wiki - Home" />
        <meta
          property="og:description"
          content="Discover effective cleaning tips and hygiene practices for your home."
        />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Micro-Hygiene Wiki - Home" />
        <meta
          name="twitter:description"
          content="Discover effective cleaning tips and hygiene practices for your home."
        />
      </Helmet>

      <div className="home-page">
        <header className="hero">
          <h1>Micro-Hygiene Wiki</h1>
          <p className="subtitle">
            Community-voted cleaning tips and hygiene practices for a healthier
            home
          </p>
        </header>

        <section className="featured-tips">
          <h2>Featured Tips</h2>
          <div className="tip-grid">
            {[
              {
                id: 1,
                title: 'Kitchen Deep Cleaning Guide',
                category: 'Kitchen',
                rating: 4.5,
              },
              {
                id: 2,
                title: 'Bathroom Mold Prevention',
                category: 'Bathroom',
                rating: 4.2,
              },
              {
                id: 3,
                title: 'Living Room Organization',
                category: 'Living Room',
                rating: 4.7,
              },
            ].map((tip) => (
              <div key={tip.id} className="tip-card">
                <span className="category-badge">{tip.category}</span>
                <h3>{tip.title}</h3>
                <div className="rating">★ {tip.rating.toFixed(1)}</div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </>
  );
}
