import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

declare const global: typeof globalThis;
import {
  getCategories,
  getTips,
  getTip,
  getCategory,
  createTip,
  voteTip,
  searchTips,
  ApiError,
} from '../api/client';

describe('API Client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('getCategories', () => {
    it('should fetch categories successfully', async () => {
      const mockCategories = [
        { id: 1, name: 'Kitchen', slug: 'kitchen', description: 'Kitchen tips', tips_count: 5 },
        { id: 2, name: 'Bathroom', slug: 'bathroom', description: 'Bathroom tips', tips_count: 3 },
      ];

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockCategories,
      } as Response);

      const result = await getCategories();

      expect(result).toEqual(mockCategories);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/categories/'),
        expect.objectContaining({ method: 'GET' })
      );
    });

    it('should throw ApiError on failed request', async () => {
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
        json: async () => ({ error: 'Server error' }),
      } as Response);

      await expect(getCategories()).rejects.toThrow(ApiError);
    });

    it('should throw ApiError on network error', async () => {
      global.fetch = vi.fn().mockRejectedValueOnce(new Error('Network error'));

      await expect(getCategories()).rejects.toThrow(ApiError);
    });
  });

  describe('getTips', () => {
    it('should fetch tips with default page', async () => {
      const mockResponse = {
        count: 2,
        total_pages: 1,
        current_page: 1,
        next: null,
        previous: null,
        results: [
          { id: 1, title: 'Tip 1', slug: 'tip-1', category_name: 'Kitchen', effectiveness_avg: 4.5, difficulty_avg: 2.0, success_rate: 150, created_at: '2024-01-01' },
        ],
      };

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response);

      const result = await getTips();

      expect(result).toEqual(mockResponse);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tips/?page=1'),
        expect.any(Object)
      );
    });

    it('should fetch tips with specified page', async () => {
      const mockResponse = {
        count: 40,
        total_pages: 2,
        current_page: 2,
        next: null,
        previous: 1,
        results: [],
      };

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response);

      const result = await getTips(2);

      expect(result.current_page).toBe(2);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tips/?page=2'),
        expect.any(Object)
      );
    });
  });

  describe('getTip', () => {
    it('should fetch tip detail by id', async () => {
      const mockTip = {
        id: 1,
        title: 'Test Tip',
        slug: 'test-tip',
        description: 'Test description',
        category: { id: 1, name: 'Kitchen', slug: 'kitchen', description: '', tips_count: 5 },
        votes: [],
        vote_count: 0,
        vote_score: 0,
        effectiveness_avg: 4.5,
        difficulty_avg: 2.0,
        success_rate: 150,
        created_at: '2024-01-01',
      };

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockTip,
      } as Response);

      const result = await getTip(1);

      expect(result).toEqual(mockTip);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tips/1/'),
        expect.any(Object)
      );
    });

    it('should throw error for non-existent tip', async () => {
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
        json: async () => ({ error: 'Tip not found' }),
      } as Response);

      await expect(getTip(999)).rejects.toThrow(ApiError);
    });
  });

  describe('getCategory', () => {
    it('should fetch category detail by slug', async () => {
      const mockCategory = {
        id: 1,
        name: 'Kitchen',
        slug: 'kitchen',
        description: 'Kitchen hygiene tips',
        tips: [
          { id: 1, title: 'Tip 1', slug: 'tip-1', category_name: 'Kitchen', effectiveness_avg: 4.5, difficulty_avg: 2.0, success_rate: 150, created_at: '2024-01-01' },
        ],
      };

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockCategory,
      } as Response);

      const result = await getCategory('kitchen');

      expect(result).toEqual(mockCategory);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/categories/kitchen/'),
        expect.any(Object)
      );
    });
  });

  describe('createTip', () => {
    it('should create a new tip successfully', async () => {
      const mockResponse = { tip_id: 1, title: 'New Tip' };
      const tipData = {
        title: 'New Tip',
        description: 'Description',
        category_id: 1,
        turnstile_token: 'token123',
      };

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response);

      const result = await createTip(tipData);

      expect(result).toEqual(mockResponse);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tips/create/'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(tipData),
        })
      );
    });

    it('should throw error on validation failure', async () => {
      const tipData = {
        title: '',
        description: '',
        category_id: 1,
        turnstile_token: 'token',
      };

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        json: async () => ({ error: 'Missing required fields' }),
      } as Response);

      await expect(createTip(tipData)).rejects.toThrow(ApiError);
    });
  });

  describe('voteTip', () => {
    it('should submit vote successfully', async () => {
      const mockResponse = {
        success: true,
        effectiveness_avg: 4.5,
        difficulty_avg: 2.0,
        success_rate: 150,
      };
      const voteData = { effectiveness: 5, difficulty: 2 };

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      } as Response);

      const result = await voteTip(1, voteData);

      expect(result).toEqual(mockResponse);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tips/1/vote/'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(voteData),
        })
      );
    });

    it('should throw error on duplicate vote', async () => {
      const voteData = { effectiveness: 5, difficulty: 2 };

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        status: 400,
        statusText: 'Bad Request',
        json: async () => ({ error: 'You have already voted on this tip' }),
      } as Response);

      await expect(voteTip(1, voteData)).rejects.toThrow(ApiError);
    });
  });

  describe('searchTips', () => {
    it('should search tips by query', async () => {
      const mockResults = [
        { id: 1, title: 'Kitchen Tip', slug: 'kitchen-tip', category_name: 'Kitchen', effectiveness_avg: 4.5, difficulty_avg: 2.0, success_rate: 150, created_at: '2024-01-01' },
      ];

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResults,
      } as Response);

      const result = await searchTips('kitchen');

      expect(result).toEqual(mockResults);
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/tips/search/?q=kitchen'),
        expect.any(Object)
      );
    });

    it('should encode special characters in query', async () => {
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => [],
      } as Response);

      await searchTips('kitchen & bathroom');

      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining(encodeURIComponent('kitchen & bathroom')),
        expect.any(Object)
      );
    });
  });

  describe('ApiError', () => {
    it('should create ApiError with message', () => {
      const error = new ApiError('Test error');
      expect(error.message).toBe('Test error');
      expect(error.name).toBe('ApiError');
    });

    it('should create ApiError with status code', () => {
      const error = new ApiError('Test error', 404);
      expect(error.statusCode).toBe(404);
    });

    it('should create ApiError with response', () => {
      const mockResponse = { status: 500 } as Response;
      const error = new ApiError('Test error', 500, mockResponse);
      expect(error.response).toBe(mockResponse);
    });
  });
});
