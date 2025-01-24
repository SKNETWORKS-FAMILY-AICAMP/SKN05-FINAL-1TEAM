import { create } from 'zustand';

interface UserState {
  accessToken: string | null;
  userId: number | null;
  setAccessToken: (token: string) => void;
  setUserId: (id: number) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  accessToken: null,
  userId: null,
  setAccessToken: (token) => set({ accessToken: token }),
  setUserId: (id) => set({ userId: id }),
  clearUser: () => set({ accessToken: null, userId: null }),
}));
