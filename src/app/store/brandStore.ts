import { create } from 'zustand';

interface BrandState {
  selectedBrand: string | null;
  selectedModel: string | null;
  setSelectedBrand: (brand: string) => void;
  setSelectedModel: (model: string) => void;
  resetSelection: () => void;
}

export const useBrandStore = create<BrandState>((set) => ({
  selectedBrand: null,
  selectedModel: null,
  setSelectedBrand: (brand) => set({ selectedBrand: brand }),
  setSelectedModel: (model) => set({ selectedModel: model }),
  resetSelection: () => set({ selectedBrand: null, selectedModel: null }),
}));