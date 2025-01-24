import { create } from 'zustand';

interface UserStore {
  accessToken: string | null;
  user: {
    username: string | null;
    email: string | null;
  };
  setAccessToken: (token: string) => void;
  clearAccessToken: () => void;
  setUser: (user: { username: string; email: string }) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  accessToken: null,
  user: {
    username: null,
    email: null,
  },
  setAccessToken: (token) => set({ accessToken: token }),
  clearAccessToken: () => set({ accessToken: null }),
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: { username: null, email: null } }),
}));
