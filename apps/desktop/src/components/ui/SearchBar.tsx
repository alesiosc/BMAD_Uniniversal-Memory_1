import React, { useState } from 'react';
import { useConversationStore } from '../../stores/conversationStore';

export const SearchBar: React.FC = () => {
  const [query, setQuery] = useState('');
  const performSearch = useConversationStore((state) => state.performSearch);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (query.trim()) {
      performSearch(query.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-md">
      <div className="flex items-center border-b border-blue-500 py-2">
        <input
          className="appearance-none bg-transparent border-none w-full text-white mr-3 py-1 px-2 leading-tight focus:outline-none"
          type="text"
          placeholder="Search memories..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          className="flex-shrink-0 bg-blue-500 hover:bg-blue-700 border-blue-500 hover:border-blue-700 text-sm border-4 text-white py-1 px-2 rounded"
          type="submit"
        >
          Search
        </button>
      </div>
    </form>
  );
};