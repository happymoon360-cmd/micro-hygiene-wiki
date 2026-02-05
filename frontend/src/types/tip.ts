/**
 * Type definitions for Tip data
 */

export interface Tip {
  id: number;
  title: string;
  description: string;
  category: {
    id: number;
    name: string;
    slug: string;
  };
  effectiveness_avg: number;
  difficulty_avg: number;
  success_rate: number;
  created_at: string;
  vote_count?: number;
  author?: string;
}

export interface TipWithRating extends Tip {
  aggregateRating: {
    ratingValue: number;
    reviewCount: number;
    bestRating: number;
    worstRating: number;
  };
  interactionStatistic: {
    interactionType: string;
    userInteractionCount: number;
  };
}
