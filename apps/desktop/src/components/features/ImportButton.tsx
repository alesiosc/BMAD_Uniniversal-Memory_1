import React, { useRef } from 'react';
import { useConversationStore } from '../../stores/conversationStore';
import { Conversation } from 'shared-types';
import { open } from '@tauri-apps/api/dialog';

export const ImportButton: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const addConversation = useConversationStore((state) => state.addConversation);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
      const text = e.target?.result as string;
      const turns = text.split('\\n').map(line => ({
        speaker: line.toLowerCase().startsWith('user:') ? 'user' : 'ai',
        text: line.replace(/^(User:|AI:)\s*/i, ''),
      }));

      const newConversation: Omit<Conversation, 'id'> = {
        source: `imported: ${file.name}`,
        timestamp: Math.floor(Date.now() / 1000),
        content: turns,
      };

      try {
        await addConversation(newConversation);
        alert('Import successful!');
      } catch (error) {
        alert('Import failed. Please check the console for details.');
      }
    };
    reader.readAsText(file);
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: 'none' }}
        accept=".txt"
      />
      <button
        onClick={handleClick}
        className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded transition-colors"
      >
        Import
      </button>
    </div>
  );
};