import React, { useCallback, useRef } from 'react';
import { UploadCloud, File, Loader2 } from 'lucide-react';

export function UploadPanel({ onUpload, isUploading, documents }) {
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf') {
        onUpload(file);
      } else {
        alert("Please upload a PDF file.");
      }
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <div style={{ padding: '1.5rem', borderBottom: '1px solid var(--border-color)' }}>
        <h2 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '1rem' }}>Knowledge Base</h2>
        
        <div 
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          style={{
            border: '2px dashed var(--border-color)',
            borderRadius: '12px',
            padding: '2rem 1rem',
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            backgroundColor: 'rgba(255,255,255,0.02)',
            position: 'relative'
          }}
          onMouseEnter={(e) => e.currentTarget.style.borderColor = 'var(--primary)'}
          onMouseLeave={(e) => e.currentTarget.style.borderColor = 'var(--border-color)'}
        >
          <input 
            type="file" 
            accept=".pdf" 
            ref={fileInputRef} 
            onChange={handleFileSelect} 
            style={{ display: 'none' }} 
          />
          
          {isUploading ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.75rem', color: 'var(--primary)' }}>
              <Loader2 className="spinner" size={28} />
              <span style={{ fontSize: '0.875rem', fontWeight: 500 }}>Processing PDF...</span>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.75rem', color: 'var(--text-muted)' }}>
              <UploadCloud size={28} />
              <span style={{ fontSize: '0.875rem' }}>Drag & drop or click to upload PDF</span>
            </div>
          )}
        </div>
        
        <style>{`
          @keyframes spin { 100% { transform: rotate(360deg); } }
          .spinner { animation: spin 1s linear infinite; }
        `}</style>
      </div>

      <div style={{ flex: 1, overflowY: 'auto', padding: '1rem' }} className="custom-scrollbar">
        {documents.length === 0 ? (
          <div style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.875rem', marginTop: '2rem' }}>
            No documents uploaded yet.
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {documents.map((doc, idx) => (
              <div key={idx} style={{ 
                display: 'flex', alignItems: 'center', gap: '0.75rem', 
                padding: '0.75rem', background: 'rgba(255,255,255,0.03)', 
                borderRadius: '8px', border: '1px solid rgba(255,255,255,0.05)'
              }}>
                <div style={{ color: 'var(--primary)' }}>
                  <File size={20} />
                </div>
                <div style={{ overflow: 'hidden' }}>
                  <div style={{ fontSize: '0.875rem', whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden' }}>
                    {doc.filename}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    {doc.num_chunks} chunks
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
