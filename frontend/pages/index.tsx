// =============================================================================
// AI Multimodal Tutor - Main Page
// =============================================================================
// Phase: 5 - Frontend Development
// Purpose: Main application page
// Version: 5.0.0
// =============================================================================

import { useState, useEffect } from 'react';
import Head from 'next/head';
import QuestionInput from '../components/QuestionInput';
import ResponseDisplay from '../components/ResponseDisplay';
import VoiceInput from '../components/VoiceInput';
import FileUpload from '../components/FileUpload';
import apiService, { AskResponse, HealthResponse } from '../lib/api';
import styles from '../styles/Home.module.css';

export default function Home() {
  // State
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [response, setResponse] = useState<AskResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [ingestStatus, setIngestStatus] = useState<any>(null);

  // Check API connection on mount
  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      const healthData = await apiService.getHealth();
      setHealth(healthData);
      setIsConnected(true);
      
      // Check ingest status
      try {
        const status = await apiService.getIngestStatus();
        setIngestStatus(status);
      } catch (err) {
        console.log('No content ingested yet');
      }
    } catch (err) {
      setIsConnected(false);
      setError('Cannot connect to backend. Make sure the server is running.');
    }
  };

  const handleAskQuestion = async (question: string) => {
    setIsLoading(true);
    setError('');
    
    try {
      const result = await apiService.askQuestion({
        question,
        top_k: 5,
        threshold: 0.7,
        prompt_type: 'default',
      });
      setResponse(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get answer');
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceInput = (transcript: string) => {
    handleAskQuestion(transcript);
  };

  const handleFileSelect = (file: File) => {
    console.log('File selected:', file.name);
    // For Phase 6 - handle file upload
  };

  const handleIngest = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const result = await apiService.ingestCourse();
      alert(`Ingestion complete: ${result.message}`);
      // Refresh status
      const status = await apiService.getIngestStatus();
      setIngestStatus(status);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to ingest course');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>AI Multimodal Tutor</title>
        <meta name="description" content="Ask questions about your GitHub course" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <h1 className={styles.title}>AI Multimodal Tutor</h1>
          <p className={styles.subtitle}>
            Your personal programming tutor powered by AI
          </p>
        </div>
        
        {/* Status Badge */}
        <div className={styles.status}>
          <span className={`${styles.statusDot} ${isConnected ? styles.connected : styles.disconnected}`} />
          {isConnected ? 'Connected' : 'Disconnected'}
        </div>
      </header>

      {/* Main Content */}
      <main className={styles.main}>
        {/* Error Message */}
        {error && (
          <div className={styles.error}>
            {error}
            <button onClick={() => setError('')} className={styles.errorClose}>
              ✕
            </button>
          </div>
        )}

        {/* Info Bar */}
        <div className={styles.infoBar}>
          <div className={styles.infoItem}>
            <span className={styles.infoLabel}>Vectors:</span>
            <span className={styles.infoValue}>
              {ingestStatus?.total_vectors || 0}
            </span>
          </div>
          <div className={styles.infoItem}>
            <span className={styles.infoLabel}>Phase:</span>
            <span className={styles.infoValue}>
              {health?.phase || 'Loading...'}
            </span>
          </div>
          <button 
            className={styles.ingestButton}
            onClick={handleIngest}
            disabled={isLoading || !isConnected}
          >
            📥 Ingest Course
          </button>
        </div>

        {/* Response Display */}
        <ResponseDisplay
          question={response?.question || ''}
          answer={response?.answer || ''}
          sources={response?.sources || []}
          hasCode={response?.has_code || false}
          codeBlocks={response?.code_blocks || []}
          voiceAudio={response?.voice_audio}
          isLoading={isLoading}
        />

        {/* Input Section */}
        <div className={styles.inputSection}>
          <QuestionInput
            onSubmit={handleAskQuestion}
            isLoading={isLoading}
            disabled={!isConnected}
          />
          
          <div className={styles.inputTools}>
            <VoiceInput
              onVoiceInput={handleVoiceInput}
              disabled={!isConnected}
            />
            <FileUpload
              onFileSelect={handleFileSelect}
              disabled={!isConnected}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className={styles.footer}>
        <p>
          Powered by Gemini LLM + Pinecone Vector DB
        </p>
      </footer>
    </div>
  );
}
