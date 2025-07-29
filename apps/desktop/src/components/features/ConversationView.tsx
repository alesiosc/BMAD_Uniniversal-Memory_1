import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useConversationStore } from '../../stores/conversationStore';
import { ConversationTurn } from 'shared-types';

const formatTimestamp = (timestamp: number): string => {
  return new Date(timestamp * 1000).toLocaleString();
};

const Turn: React.FC<{ turn: ConversationTurn }> = ({ turn }) => {
  const isUser = turn.speaker === 'user';
  return (
    <div className={`p-4 rounded-lg mb-4 ${isUser ? 'bg-gray-700 ml-10' : 'bg-gray-800 mr-10'}`}>
      <p className={`text-sm font-semibold mb-2 ${isUser ? 'text-blue-400' : 'text-green-400'}`}>{isUser ? 'User' : 'AI'}</p>
      <p className="text-gray-300 whitespace-pre-wrap">{turn.text}</p>
    </div>
  );
};

export const ConversationView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { selectedConversation, isLoading, fetchConversationById, deleteConversation } = useConversationStore();

  useEffect(() => {
    if (id) {
      fetchConversationById(id);
    }
  }, [id, fetchConversationById]);

  const handleDelete = async () => {
    if (id && window.confirm("Are you sure you want to permanently delete this memory?")) {
      try {
        await deleteConversation(id);
        navigate('/'); // Navigate back to the main feed on success
      } catch (error) {
          alert("Failed to delete memory. Please try again.");
      }
    }
  };

  if (isLoading) {
    return <div className="text-white text-center p-4">Loading conversation...</div>;
  }

  if (!selectedConversation) {
    return <div className="text-white text-center p-4">Conversation not found or has been deleted.</div>;
  }

  return (
    <div className="h-full overflow-y-auto p-4">
      <div className="mb-6 pb-4 border-b border-gray-700 flex justify-between items-center">
        <div>
          <h2 className="text-lg font-bold text-blue-400">{selectedConversation.source}</h2>
          <p className="text-xs text-gray-400">{formatTimestamp(selectedConversation.timestamp)}</p>
        </div>
        <button
          onClick={handleDelete}
          className="bg-red-600 hover:bg-red-800 text-white font-bold py-2 px-4 rounded transition-colors"
        >
          Delete
        </button>
      </div>
      <div>
        {selectedConversation.content.map((turn, index) => (
          <Turn key={index} turn={turn} />
        ))}
      </div>
    </div>
  );
};