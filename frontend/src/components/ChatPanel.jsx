import React, { useState, useRef, useEffect } from 'react';
import { Send, Trash2, Loader2 } from 'lucide-react';
import { MessageBubble } from './MessageBubble';

export function ChatPanel({ messages, isLoading, onSend, onClear }) {
  const [input, setInput] = useState('');
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      
      {/* Header bar */}
      <div style={{ padding: '1rem 1.5rem', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ fontSize: '1rem', fontWeight: 600 }}>Research Chat</h2>
        <button 
          onClick={onClear}
          title="Clear Chat"
          style={{ background: 'transparent', color: 'var(--text-muted)', padding: '0.5rem', borderRadius: '8px' }}
          onMouseEnter={(e) => { e.currentTarget.style.color = '#ef4444'; e.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.1)'; }}
          onMouseLeave={(e) => { e.currentTarget.style.color = 'var(--text-muted)'; e.currentTarget.style.backgroundColor = 'transparent'; }}
        >
          <Trash2 size={18} />
        </button>
      </div>

      {/* Messages area */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }} className="custom-scrollbar">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} role={msg.role} content={msg.content} sources={msg.sources} />
        ))}
        {isLoading && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', color: 'var(--text-muted)', alignSelf: 'flex-start', padding: '1rem' }}>
            <Loader2 className="spinner" size={20} />
            <span style={{ fontSize: '0.875rem' }}>Thinking...</span>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div style={{ padding: '1.5rem', borderTop: '1px solid var(--border-color)', background: 'rgba(0,0,0,0.2)' }}>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '1rem' }}>
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question, or type 'summarize'..."
            disabled={isLoading}
            style={{
              flex: 1, padding: '1rem 1.5rem', borderRadius: '12px',
              background: 'rgba(255,255,255,0.05)', color: 'white', border: '1px solid var(--border-color)',
              fontSize: '1rem', outline: 'none', transition: 'border-color 0.2s'
            }}
            onFocus={(e) => e.target.style.borderColor = 'var(--primary)'}
            onBlur={(e) => e.target.style.borderColor = 'var(--border-color)'}
          />
          <button 
            type="submit"
            disabled={isLoading || !input.trim()}
            style={{
              background: input.trim() && !isLoading ? 'var(--accent-gradient)' : 'rgba(255,255,255,0.1)',
              color: input.trim() && !isLoading ? 'white' : 'var(--text-muted)',
              padding: '0 1.5rem', borderRadius: '12px',
              display: 'flex', alignItems: 'center', justifyContent: 'center'
            }}
          >
            <Send size={20} />
          </button>
        </form>
      </div>

    </div>
  );
}
