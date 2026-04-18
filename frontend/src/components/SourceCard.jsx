import React, { useState } from 'react';
import { ChevronDown, ChevronUp, ExternalLink } from 'lucide-react';

export function SourceCard({ index, source }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div style={{
      background: 'rgba(0,0,0,0.2)',
      border: '1px solid var(--border-color)',
      borderRadius: '8px',
      overflow: 'hidden',
      maxWidth: '300px',
      flex: '1 1 200px'
    }}>
      
      {/* Header / Toggle */}
      <div 
        onClick={() => setExpanded(!expanded)}
        style={{
          padding: '0.5rem 0.75rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          cursor: 'pointer',
          background: 'rgba(255,255,255,0.03)',
          transition: 'background 0.2s',
          fontSize: '0.8rem'
        }}
        onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.06)'}
        onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.03)'}
      >
        <span style={{ 
          background: 'var(--primary)', color: '#000', fontWeight: 'bold', 
          width: '20px', height: '20px', display: 'flex', alignItems: 'center', 
          justifyContent: 'center', borderRadius: '4px', fontSize: '0.7rem' 
        }}>
          {index}
        </span>
        <span style={{ flex: 1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', color: 'var(--text-muted)' }}>
          {source.source} <span style={{opacity: 0.6}}>(Pg {source.page})</span>
        </span>
        {expanded ? <ChevronUp size={14} color="var(--text-muted)" /> : <ChevronDown size={14} color="var(--text-muted)" />}
      </div>

      {/* Expanded Content */}
      {expanded && (
        <div style={{
          padding: '0.75rem',
          borderTop: '1px solid var(--border-color)',
          fontSize: '0.8rem',
          color: 'var(--text-muted)',
          lineHeight: '1.5',
          fontStyle: 'italic',
          background: 'rgba(0,0,0,0.3)',
          maxHeight: '150px',
          overflowY: 'auto'
        }} className="custom-scrollbar">
          "{source.text}"
        </div>
      )}
    </div>
  );
}
