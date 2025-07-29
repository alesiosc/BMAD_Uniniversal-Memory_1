import { Conversation } from 'shared-types';

const apiClient = {
  // get and post methods remain the same
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
        // Handle 404 specifically if needed, otherwise just throw
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    // DELETE requests often return 204 No Content, so we don't expect a body
    return;
  }
};

export const conversationService = {
  // getAll, getById, search methods remain the same
  getAll: async (): Promise<Conversation[]> => {
    return apiClient.get('/conversations');
  },
  getById: async (id: string): Promise<Conversation> => {
    return apiClient.get(`/conversations/${id}`);
  },
  search: async (query: string): Promise<Conversation[]> => {
    return apiClient.post('/search', { query });
  },
  deleteById: async (id: string): Promise<void> => {
    return apiClient.delete(`/conversations/${id}`);
  },
};