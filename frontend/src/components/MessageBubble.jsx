import React from 'react';
import { Bot, User, AlertCircle } from 'lucide-react';
import { SourceCard } from './SourceCard';

export function MessageBubble({ role, content, sources }) {
  const isAI = role === 'ai';
  const isError = role === 'error';

  // Simple markdown-ish bold parser
  const renderText = (text) => {
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} style={{ color: 'white' }}>{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  return (
    <div style={{
      display: 'flex', gap: '1rem',
      alignSelf: isAI || isError ? 'flex-start' : 'flex-end',
      maxWidth: '85%'
    }}>
      
      {/* Avatar (only for AI) */}
      {(isAI || isError) && (
        <div style={{
          width: '32px', height: '32px', borderRadius: '50%',
          background: isError ? 'rgba(239, 68, 68, 0.2)' : 'var(--accent-gradient)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0, marginTop: '0.25rem'
        }}>
          {isError ? <AlertCircle size={18} color="#ef4444" /> : <Bot size={18} color="white" />}
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        
        {/* Message Bubble */}
        <div style={{
          background: isError ? 'rgba(239, 68, 68, 0.1)' : (isAI ? 'rgba(255, 255, 255, 0.05)' : 'var(--accent-gradient)'),
          color: isError ? '#ef4444' : 'var(--text-main)',
          padding: '1rem 1.25rem',
          borderRadius: '16px',
          borderBottomLeftRadius: isAI || isError ? '4px' : '16px',
          borderBottomRightRadius: !isAI && !isError ? '4px' : '16px',
          border: isAI ? '1px solid var(--border-color)' : 'none',
          boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
          lineHeight: '1.6',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
          fontSize: '0.95rem'
        }}>
          {renderText(content)}
        </div>

        {/* Source Cards */}
        {sources && sources.length > 0 && (
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '0.25rem' }}>
            {sources.map((src, i) => (
              <SourceCard key={i} index={i+1} source={src} />
            ))}
          </div>
        )}

      </div>

      {/* Avatar (only for User) */}
      {!isAI && !isError && (
        <div style={{
          width: '32px', height: '32px', borderRadius: '50%',
          background: 'rgba(255, 255, 255, 0.1)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0, marginTop: '0.25rem',
          border: '1px solid var(--border-color)'
        }}>
          <User size={18} color="var(--text-muted)" />
        </div>
      )}

    </div>
  );
}
