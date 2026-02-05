/**
 * Utility functions for generating clean, SEO-friendly URLs
 */

/**
 * Convert a title or string to a clean, lowercase, hyphen-separated slug
 * @param {string} text - The text to convert
 * @returns {string} - Clean, lowercase, hyphen-separated slug
 */
export function createSlug(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '') // Remove special characters
    .replace(/[\s_]+/g, '-') // Replace spaces and underscores with hyphens
    .replace(/-+/g, '-') // Replace multiple hyphens with single hyphen
    .replace(/^-+|-+$/g, ''); // Remove leading/trailing hyphens
}

/**
 * Generate a clean URL path for a tip
 * @param {string} title - The tip title
 * @param {number} id - The tip ID
 * @returns {string} - Clean URL path (e.g., "/tips/123-clean-tip-title")
 */
export function createTipUrl(title: string, id: number): string {
  const slug = createSlug(title);
  return `/tips/${id}-${slug}`;
}

/**
 * Extract the tip ID from a clean URL
 * @param {string} urlPath - The URL path (e.g., "/tips/123-clean-tip-title")
 * @returns {number | null} - The tip ID or null if invalid
 */
export function extractTipId(urlPath: string): number | null {
  const match = urlPath.match(/\/tips\/(\d+)-/);
  return match ? parseInt(match[1], 10) : null;
}
