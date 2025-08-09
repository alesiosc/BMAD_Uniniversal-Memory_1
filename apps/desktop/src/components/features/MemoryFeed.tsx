import React, { useEffect } from 'react';
import { useConversationStore } from '../../stores/conversationStore';
import { Conversation } from 'shared-types';
import { Link } from 'react-router-dom';
import { formatTimestamp } from '../../utils/date';

const MemoryItem: React.FC<{ conversation: Conversation }> = ({ conversation }) => {
  const previewText = conversation.content[0]?.text.substring(0, 100) || 'No content';

  return (
    <Link to={`/conversation/${conversation.id}`} className="block">
      <div className="bg-gray-800 p-4 rounded-lg mb-4 border border-gray-700 hover:bg-gray-700 transition-colors">
        <div className="flex justify-between items-center mb-2">
          <p className="text-sm font-semibold text-blue-400">{conversation.source}</p>
          <p className="text-xs text-gray-400">{formatTimestamp(conversation.timestamp)}</p>
        </div>
        <p className="text-gray-300 text-sm">{previewText}...</p>
      </div>
    </Link>
  );
};

export const MemoryFeed: React.FC = () => {
  const { conversations, searchResults, isLoading, fetchConversations } = useConversationStore();
  const hasSearchResults = searchResults.length > 0;
  const itemsToDisplay = hasSearchResults ? searchResults : conversations;

  useEffect(() => {
    fetchConversations();
  }, [fetchConversations]);

  if (isLoading && itemsToDisplay.length === 0) {
    return <div className="text-white text-center p-4">Loading...</div>;
  }
  
  if (itemsToDisplay.length === 0) {
      return <div className="text-white text-center p-4">
          {hasSearchResults ? "No results found." : "No memories captured yet."}
      </div>;
  }


  return (
    <div className="h-full overflow-y-auto p-4">
      {hasSearchResults && <h2 className="text-lg font-semibold mb-4">Search Results</h2>}
      {itemsToDisplay.map((convo) => (
        <MemoryItem key={convo.id} conversation={convo} />
      ))}
    </div>
  );
};