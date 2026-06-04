import { create } from 'zustand';

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
  logout: () => void;
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

  logout: () => {
    localStorage.clear();
    set({ user: null, token: null, isAuthenticated: false });
  },
}));
