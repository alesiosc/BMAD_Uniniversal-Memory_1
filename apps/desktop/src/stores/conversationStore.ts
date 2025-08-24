import { create } from 'zustand';
import { Conversation, SearchResult } from 'shared-types';
import { conversationService } from '../services/conversationService';
import { get } from 'lodash';

interface ConversationState {
  conversations: Conversation[];
  searchResults: SearchResult[];
  selectedConversation: Conversation | null;
  isLoading: boolean;
  fetchConversations: () => Promise<void>;
  fetchConversationById: (id: string) => Promise<void>;
  performSearch: (query: string) => Promise<void>;
  deleteConversation: (id: string) => Promise<void>;
  addConversation: (conversationData: Omit<Conversation, 'id'>) => Promise<void>;
}

export const useConversationStore = create<ConversationState>((set, get) => ({
  conversations: [],
  searchResults: [],
  selectedConversation: null,
  isLoading: false,

  fetchConversations: async () => {
    set({ isLoading: true });
    try {
      const conversations = await conversationService.getAll();
      set({ conversations, searchResults: [], isLoading: false });
    } catch (error) {
      console.error("Failed to fetch conversations:", error);
      set({ isLoading: false });
    }
  },

  fetchConversationById: async (id: string) => {
    set({ isLoading: true, selectedConversation: null });
    try {
      const conversation = await conversationService.getById(id);
      set({ selectedConversation: conversation, isLoading: false });
    } catch (error) {
      console.error(`Failed to fetch conversation ${id}:`, error);
      set({ isLoading: false });
    }
  },

  performSearch: async (query: string) => {
    set({ isLoading: true });
    try {
      const results = await conversationService.search(query);
      set({ searchResults: results, isLoading: false });
    } catch (error) {
      console.error(`Failed to perform search for "${query}":`, error);
      set({ isLoading: false });
    }
  },

  deleteConversation: async (id: string) => {
    try {
      await conversationService.deleteById(id);
      set((state) => ({
        conversations: state.conversations.filter((c) => c.id !== id),
        searchResults: state.searchResults.filter((c) => c.id !== id),
        selectedConversation: state.selectedConversation?.id === id ? null : state.selectedConversation,
      }));
    } catch (error) {
      console.error(`Failed to delete conversation ${id}:`, error);
      throw error;
    }
  },

  addConversation: async (conversationData) => {
    try {
      await conversationService.add(conversationData);
      await get().fetchConversations();
    } catch (error) {
      console.error("Failed to add conversation:", error);
      throw error;
    }
  },
}));