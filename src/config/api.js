/**
 * Centralized API Configuration
 * 
 * For Vercel deployment with serverless functions:
 * - Both frontend and backend are on the same domain
 * - API requests use relative paths (no CORS needed)
 * - Backend runs as serverless functions in /api directory
 * 
 * Environment Variables:
 * - Development: Uses localhost:5000 by default
 * - Production (Vercel): Leave NEXT_PUBLIC_API_URL empty or unset for relative paths
 */

// Get the API base URL from environment variable
// In production on Vercel, use empty string for relative paths (same domain)
// In development, use localhost:5000
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

/**
 * Helper function to construct full API URLs
 * @param {string} path - The API endpoint (e.g., '/api/auth/login')
 * @returns {string} - The full API URL
 */
export const apiUrl = (path) => {
  // If API_BASE_URL is empty (production Vercel), return path as-is (relative)
  if (!API_BASE_URL || API_BASE_URL === '') {
    return path;
  }
  
  // Otherwise, construct full URL with base (development)
  return `${API_BASE_URL}${path}`;
};
