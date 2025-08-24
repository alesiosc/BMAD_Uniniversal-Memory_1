import { Conversation, SearchResult } from 'shared-types';
import { conversationService } from './conversationService';
import { get } from 'lodash';

const apiClient = {
  async get(endpoint: string) {
    const response = await fetch(`http://127.0.0.1:8000${endpoint}`);
    if (!response.ok) throw new Error('Network response was not ok');
    return response.json();
  },
  async post(endpoint: string, body: any) {
    const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error('Network response was not ok');
    return response.json();
  },
  async delete(endpoint: string) {
    const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return;
  }
};

export const conversationService = {
  getAll: async (): Promise<Conversation[]> => {
    return apiClient.get('/conversations');
  },
  getById: async (id: string): Promise<Conversation> => {
    return apiClient.get(`/conversations/${id}`);
  },
  search: async (query: string): Promise<SearchResult[]> => {
    return apiClient.post('/search', { query });
  },
  deleteById: async (id: string): Promise<void> => {
    return apiClient.delete(`/conversations/${id}`);
  },
  add: async (conversationData: Omit<Conversation, 'id'>): Promise<Conversation> => {
    return apiClient.post('/conversations', conversationData);
  },
};