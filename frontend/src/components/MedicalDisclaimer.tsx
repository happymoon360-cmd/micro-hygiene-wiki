import { Helmet } from 'react-helmet-async';

/**
 * MedicalDisclaimer Component
 * Displays medical disclaimer across all pages
 */
export default function MedicalDisclaimer() {
  return (
    <>
      <Helmet>
        <meta name="description" content="Medical disclaimer for Micro-Hygiene Wiki" />
      </Helmet>
      <div className="medical-disclaimer">
        <strong>⚕️ Medical Disclaimer:</strong>
        <p>
          The content on this website is for general informational purposes only and does not 
          constitute medical advice, diagnosis, or treatment. Always consult with a qualified 
          healthcare professional before implementing any hygiene practices discussed here.
        </p>
        <p>
          These tips are based on community experience and general best practices. 
          Individual results may vary based on personal health conditions, allergies, and 
          specific circumstances.
        </p>
        <p>
          If you have a medical condition, skin sensitivity, or allergies to any cleaning 
          products or materials, please consult your doctor before use.
        </p>
      </div>
      <style>{`
        .medical-disclaimer {
          background-color: #fff3cd;
          border: 2px solid #ffa726;
          border-left: 4px solid #ffc107;
          padding: 1rem 1.5rem;
          margin: 2rem 0;
          border-radius: 4px;
        }

        .medical-disclaimer strong {
          color: #dc3545;
          display: block;
          margin-bottom: 0.75rem;
        }

        .medical-disclaimer p {
          margin-bottom: 0.75rem;
          line-height: 1.5;
          color: #333;
        }

        .medical-disclaimer p:last-child {
          margin-bottom: 0;
        }
      `}</style>
    </>
  );
}
