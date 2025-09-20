import { create } from 'zustand';
import axios from 'axios';

// Base URL for backend
const API_BASE = 'http://localhost:8000'; // Change to production URL

const useStore = create((set, get) => ({
  user: null,
  products: [],
  favorites: [],
  isLoading: false,
  error: null,

  // Authenticate user
  authenticateUser: async (initData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post(`${API_BASE}/users/auth`, { init_data: initData });
      set({ user: response.data });
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ isLoading: false });
    }
  },

  // Get user
  getUser: async (telegramId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE}/users/me?telegram_id=${telegramId}`);
      set({ user: response.data });
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ isLoading: false });
    }
  },

  // Get products
  fetchProducts: async (params = {}) => {
    set({ isLoading: true, error: null });
    try {
      const query = new URLSearchParams(params).toString();
      const response = await axios.get(`${API_BASE}/products?${query}`);
      set({ products: response.data });
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ isLoading: false });
    }
  },

  // Get favorites
  fetchFavorites: async (telegramId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE}/favorites?telegram_id=${telegramId}`);
      set({ favorites: response.data });
    } catch (error) {
      set({ error: error.message });
    } finally {
      set({ isLoading: false });
    }
  },

  // Add to favorites
  addToFavorites: async (productId, telegramId) => {
    try {
      await axios.post(`${API_BASE}/favorites/${productId}?telegram_id=${telegramId}`);
      // Refresh favorites
      get().fetchFavorites(telegramId);
    } catch (error) {
      set({ error: error.message });
    }
  },

  // Remove from favorites
  removeFromFavorites: async (productId, telegramId) => {
    try {
      await axios.delete(`${API_BASE}/favorites/${productId}?telegram_id=${telegramId}`);
      // Refresh favorites
      get().fetchFavorites(telegramId);
    } catch (error) {
      set({ error: error.message });
    }
  },
}));

export default useStore;