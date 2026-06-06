import { create } from 'zustand';
import api from '../services/api';

interface User {
  id: string;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: 'student' | 'teacher' | 'admin';
  is_2fa_enabled: boolean;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  token: string | null;
  setAuth: (user: User, token: string, refreshToken: string) => void;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  isAuthenticated: !!localStorage.getItem('access_token'),
  token: localStorage.getItem('access_token'),

  setAuth: (user, token, refreshToken) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('refresh_token', refreshToken);
    localStorage.setItem('user', JSON.stringify(user));
    set({ user, token, isAuthenticated: true });
  },

  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token');

    try {
      if (refreshToken) {
        await api.post('/auth/logout/', { refresh: refreshToken });
      }
    } catch (error) {
      console.error('No se pudo registrar el cierre de sesión', error);
    } finally {
      localStorage.clear();
      set({ user: null, token: null, isAuthenticated: false });
    }
  },
}));
