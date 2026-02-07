/**
 * API Client for Micro-Hygiene Wiki
 * Provides typed functions for backend API communication
 */

// API base URL - use environment variable or fallback to localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * API Response Types matching Django serializers
 */
export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  tips_count: number;
}

export interface TipList {
  id: number;
  title: string;
  slug: string;
  category_name: string;
  effectiveness_avg: number;
  difficulty_avg: number;
  success_rate: number;
  created_at: string;
}

export interface TipDetail {
  id: number;
  title: string;
  slug: string;
  description: string;
  category: Category;
  votes: Vote[];
  vote_count: number;
  vote_score: number;
  effectiveness_avg: number;
  difficulty_avg: number;
  success_rate: number;
  created_at: string;
}

export interface Vote {
  id: number;
  effectiveness: number;
  difficulty: number;
  ip_hash: string;
  created_at: string;
}

export interface AffiliateProduct {
  id: number;
  name: string;
  affiliate_url: string;
  network: string;
  keywords: string[];
  is_active: boolean;
}

export interface TipListResponse {
  count: number;
  total_pages: number;
  current_page: number;
  next: number | null;
  previous: number | null;
  results: TipList[];
}

export interface CategoryDetail {
  id: number;
  name: string;
  slug: string;
  description: string;
  tips: TipList[];
}

export interface CreateTipRequest {
  title: string;
  description: string;
  category_id: number;
  turnstile_token: string;
}

export interface VoteRequest {
  effectiveness: number;
  difficulty: number;
}

export interface ApiErrorData {
  error: string;
  detail?: string;
}

export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public response?: Response
  ) {
    super(message);
    this.name = 'ApiError';
    this.statusCode = statusCode;
    this.response = response;
  }
}

/**
 * Generic HTTP request wrapper with error handling
 */
async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      let errorData: ApiErrorData;
      try {
        errorData = await response.json();
      } catch {
        errorData = { error: response.statusText || 'Request failed' };
      }
      throw new ApiError(errorData.error || 'Request failed', response.status, response);
    }

    return await response.json() as T;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError('Network error or request failed', undefined, undefined);
  }
}

/**
 * GET request wrapper
 */
export async function get<T>(endpoint: string): Promise<T> {
  return request<T>(endpoint, {
    method: 'GET',
  });
}

/**
 * POST request wrapper
 */
export async function post<T>(endpoint: string, data: unknown): Promise<T> {
  return request<T>(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * GET all categories
 */
export async function getCategories(): Promise<Category[]> {
  const response = await get<Category[]>('/categories/');
  return response;
}

export async function getAffiliateProducts(): Promise<AffiliateProduct[]> {
  const response = await get<AffiliateProduct[]>('/products/');
  return response;
}

/**
 * GET all tips with optional pagination
 */
export async function getTips(page: number = 1): Promise<TipListResponse> {
  const response = await get<TipListResponse>(`/tips/?page=${page}`);
  return response;
}

/**
 * GET tip detail by ID
 */
export async function getTip(id: number): Promise<TipDetail> {
  const response = await get<TipDetail>(`/tips/${id}/`);
  return response;
}

/**
 * Get category detail with tips by slug
 */
export async function getCategory(slug: string): Promise<CategoryDetail> {
  const response = await get<CategoryDetail>(`/categories/${slug}/`);
  return response;
}

/**
 * POST create new tip
 */
export async function createTip(data: CreateTipRequest): Promise<{ tip_id: number; title: string }> {
  const response = await post<{ tip_id: number; title: string }>('/tips/create/', data);
  return response;
}

/**
 * POST vote on a tip
 */
export async function voteTip(id: number, data: VoteRequest): Promise<{ success: boolean; effectiveness_avg: number; difficulty_avg: number; success_rate: number }> {
  const response = await post<{ success: boolean; effectiveness_avg: number; difficulty_avg: number; success_rate: number }>(`/tips/${id}/vote/`, data);
  return response;
}

/**
 * Search tips by query
 */
export async function searchTips(query: string): Promise<TipList[]> {
  const response = await get<TipList[]>(`/tips/search/?q=${encodeURIComponent(query)}`);
  return response;
}
