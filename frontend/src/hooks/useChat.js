import { useState } from 'react';
import { api } from '../api';

export function useChat() {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'ai',
      content: 'Hello! I am your AI Research Assistant. Upload some PDF documents, and ask me questions or ask for a summary!',
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const addMessage = (role, content, sources = null) => {
    const newMsg = { id: Date.now().toString(), role, content, sources };
    setMessages((prev) => [...prev, newMsg]);
  };

  const handleError = (err) => {
    console.error(err);
    setError(err.message);
    addMessage('error', err.message);
    setIsLoading(false);
  };

  const sendQuery = async (question) => {
    if (!question.trim()) return;
    
    addMessage('user', question);
    setIsLoading(true);
    setError(null);

    // Simple heuristic for routing to summary (only check first 20 chars to avoid false positives in large copy-pastes)
    const lowerQ = question.toLowerCase().trim();
    const isSummaryReq = ['summarize', 'summary', 'tldr', 'give me an overview'].some(kw => lowerQ.substring(0, 30).includes(kw));

    try {
      if (isSummaryReq) {
        const data = await api.summarizeDocuments();
        addMessage('ai', data.summary, data.sources);
      } else {
        const data = await api.queryDocuments(question);
        addMessage('ai', data.answer, data.sources);
      }
    } catch (err) {
      handleError(err);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        id: 'welcome',
        role: 'ai',
        content: 'Chat cleared. How can I help you?',
      }
    ]);
    setError(null);
  };

  return {
    messages,
    isLoading,
    error,
    sendQuery,
    clearChat
  };
}
