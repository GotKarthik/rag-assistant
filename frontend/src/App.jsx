import React, { useState, useEffect } from 'react';
import { UploadPanel } from './components/UploadPanel';
import { ChatPanel } from './components/ChatPanel';
import { api } from './api';
import { useChat } from './hooks/useChat';
import { Database, FileText, Cpu } from 'lucide-react';

function App() {
  const [documents, setDocuments] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const { messages, isLoading, sendQuery, clearChat } = useChat();

  const fetchDocuments = async () => {
    try {
      const data = await api.getDocuments();
      setDocuments(data.documents);
    } catch (err) {
      console.error("Could not fetch documents", err);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUpload = async (file) => {
    setIsUploading(true);
    try {
      await api.uploadPDF(file);
      await fetchDocuments();
    } catch (err) {
      alert(`Upload failed: ${err.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', padding: '1.5rem', gap: '1.5rem' }}>
      
      {/* Header */}
      <header className="glass-panel" style={{ padding: '1rem 2rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{ background: 'var(--accent-gradient)', padding: '0.5rem', borderRadius: '12px' }}>
          <Cpu color="white" />
        </div>
        <h1 style={{ fontSize: '1.25rem', fontWeight: 600, letterSpacing: '-0.025em' }}>Antigravity Research AI</h1>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: '1rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <FileText size={16} /> {documents.length} Docs
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Database size={16} /> {documents.reduce((acc, doc) => acc + doc.num_chunks, 0)} Chunks
          </span>
        </div>
      </header>

      {/* Main split view */}
      <main style={{ display: 'flex', gap: '1.5rem', flex: 1, minHeight: 0 }}>
        
        {/* Left Sidebar - Uploads */}
        <aside style={{ width: '300px', display: 'flex', flexDirection: 'column' }}>
          <UploadPanel 
            onUpload={handleUpload} 
            isUploading={isUploading} 
            documents={documents} 
          />
        </aside>

        {/* Right Area - Chat */}
        <section style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
          <ChatPanel 
            messages={messages}
            isLoading={isLoading}
            onSend={sendQuery}
            onClear={clearChat}
          />
        </section>

      </main>
    </div>
  );
}

export default App;
