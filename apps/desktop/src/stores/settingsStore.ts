import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface SettingsState {
  dataDirectory: string | null;
  hasCompletedOnboarding: boolean;
  setDataDirectory: (path: string) => void;
  setHasCompletedOnboarding: (status: boolean) => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      dataDirectory: null,
      hasCompletedOnboarding: false,
      setDataDirectory: (path) => set({ dataDirectory: path }),
      setHasCompletedOnboarding: (status) => set({ hasCompletedOnboarding: status }),
    }),
    {
      name: 'universal-memory-settings-storage',
    }
  )
);