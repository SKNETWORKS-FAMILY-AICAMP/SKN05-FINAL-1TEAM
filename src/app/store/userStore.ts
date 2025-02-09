import { create } from 'zustand';

interface UserState {
  userId: number | null;
  username: string | null;
  email: string | null;
  accessToken: string | null;
  setUser: (userId: number, username: string, email: string, accessToken: string) => void;
  clearUser: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  userId: null,
  username: null,
  email: null,
  accessToken: null,
  setUser: (userId, username, email, accessToken) => 
    set({ userId, username, email, accessToken }),
  clearUser: () => 
    set({ userId: null, username: null, email: null, accessToken: null }),
}));
