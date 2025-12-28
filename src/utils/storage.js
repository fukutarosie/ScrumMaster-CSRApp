/**
 * Safe localStorage utilities for Next.js
 * 
 * These functions safely access localStorage only when running in the browser.
 * During SSR/build time, they return null or the default value.
 */

/**
 * Safely get an item from localStorage
 * @param {string} key - The storage key
 * @param {any} defaultValue - Default value if key doesn't exist or window is undefined
 * @returns {string|null} - The stored value or null
 */
export const getStorageItem = (key, defaultValue = null) => {
  if (typeof window === 'undefined') {
    return defaultValue;
  }
  try {
    const item = window.localStorage.getItem(key);
    return item !== null ? item : defaultValue;
  } catch (error) {
    console.error(`Error reading from localStorage key "${key}":`, error);
    return defaultValue;
  }
};

/**
 * Safely set an item in localStorage
 * @param {string} key - The storage key
 * @param {string} value - The value to store
 * @returns {boolean} - True if successful, false otherwise
 */
export const setStorageItem = (key, value) => {
  if (typeof window === 'undefined') {
    return false;
  }
  try {
    window.localStorage.setItem(key, value);
    return true;
  } catch (error) {
    console.error(`Error writing to localStorage key "${key}":`, error);
    return false;
  }
};

/**
 * Safely remove an item from localStorage
 * @param {string} key - The storage key
 * @returns {boolean} - True if successful, false otherwise
 */
export const removeStorageItem = (key) => {
  if (typeof window === 'undefined') {
    return false;
  }
  try {
    window.localStorage.removeItem(key);
    return true;
  } catch (error) {
    console.error(`Error removing localStorage key "${key}":`, error);
    return false;
  }
};

/**
 * Safely get the authentication token
 * @returns {string|null} - The token or null
 */
export const getToken = () => {
  return getStorageItem('token');
};

/**
 * Safely get the user data
 * @returns {object|null} - Parsed user object or null
 */
export const getUser = () => {
  const userData = getStorageItem('user');
  if (!userData) {
    return null;
  }
  try {
    return JSON.parse(userData);
  } catch (error) {
    console.error('Error parsing user data from localStorage:', error);
    return null;
  }
};

/**
 * Safely set the authentication token
 * @param {string} token - The token to store
 */
export const setToken = (token) => {
  setStorageItem('token', token);
};

/**
 * Safely set the user data
 * @param {object} user - The user object to store
 */
export const setUser = (user) => {
  setStorageItem('user', JSON.stringify(user));
};

/**
 * Safely clear authentication data
 */
export const clearAuth = () => {
  removeStorageItem('token');
  removeStorageItem('user');
};

