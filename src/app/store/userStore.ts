import { create } from 'zustand';

interface UserStore {
  accessToken: string | null;
  userId: string | null;
  username: string | null;
  email: string | null;
  setAccessToken: (token: string) => void;
  setUser: (userId: string, username: string, email: string) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  accessToken: null,
  userId: null,
  username: null,
  email: null,
  setAccessToken: (token) => set({ accessToken: token }),
  setUser: (userId, username, email) => set({ userId, username, email }),
  clearUser: () => set({ accessToken: null, userId: null, username: null, email: null }),
}));
