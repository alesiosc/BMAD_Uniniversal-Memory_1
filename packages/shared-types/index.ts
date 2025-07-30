export interface ConversationTurn {
  speaker: 'user' | 'ai';
  text: string;
}

export interface Conversation {
  id: string;
  source: string;
  timestamp: number;
  content: ConversationTurn[];
}