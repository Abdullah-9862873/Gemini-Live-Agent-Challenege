// =============================================================================
// AI Multimodal Tutor - Response Display Component
// =============================================================================
// Phase: 5 - Frontend Development
// Purpose: Display AI responses with code highlighting
// Version: 5.0.0
// =============================================================================

import React, { useEffect, useRef } from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import styles from '../styles/ResponseDisplay.module.css';

interface CodeBlock {
  language: string;
  code: string;
}

interface ResponseDisplayProps {
  question: string;
  answer: string;
  sources: string[];
  hasCode: boolean;
  codeBlocks: CodeBlock[];
  voiceAudio?: string | null;
  isLoading: boolean;
}

/**
 * ResponseDisplay Component
 * 
 * Displays the AI's response including:
 * - The original question
 * - Formatted answer text
 * - Syntax-highlighted code blocks
 * - Source references
 * - Voice playback (if available)
 */
const ResponseDisplay: React.FC<ResponseDisplayProps> = ({
  question,
  answer,
  sources,
  hasCode,
  codeBlocks,
  voiceAudio,
  isLoading,
}) => {
  const audioRef = useRef<HTMLAudioElement>(null);

  // Play voice audio when available
  useEffect(() => {
    if (voiceAudio && audioRef.current) {
      const audioUrl = `data:audio/mp3;base64,${voiceAudio}`;
      audioRef.current.src = audioUrl;
    }
  }, [voiceAudio]);

  const playVoice = () => {
    if (audioRef.current) {
      audioRef.current.play();
    }
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <span>Thinking...</span>
        </div>
      </div>
    );
  }

  if (!question && !answer) {
    return (
      <div className={styles.container}>
        <div className={styles.empty}>
          <h2>AI Multimodal Tutor</h2>
          <p>Ask a question to get started!</p>
          <p className={styles.hint}>
            Make sure to ingest course content first using the ingest button.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      {/* Question */}
      <div className={styles.questionSection}>
        <div className={styles.label}>Question</div>
        <div className={styles.question}>{question}</div>
      </div>

      {/* Answer */}
      <div className={styles.answerSection}>
        <div className={styles.label}>Answer</div>
        
        {/* Voice Playback */}
        {voiceAudio && (
          <button className={styles.voiceButton} onClick={playVoice}>
            <span className={styles.voiceIcon}>🔊</span>
            Play Voice
          </button>
        )}
        
        {/* Hidden audio element for playback */}
        <audio ref={audioRef} className={styles.hiddenAudio} controls />
        
        {/* Answer Text */}
        <div className={styles.answer}>
          {answer.split('```').map((part, index) => {
            // Even indices are regular text, odd indices are code
            if (index % 2 === 0) {
              return (
                <p key={index} className={styles.answerText}>
                  {part}
                </p>
              );
            }
            return null; // Code blocks handled separately below
          })}
        </div>

        {/* Code Blocks */}
        {hasCode && codeBlocks.length > 0 && (
          <div className={styles.codeSection}>
            <div className={styles.label}>Code Examples</div>
            {codeBlocks.map((block, index) => (
              <div key={index} className={styles.codeBlock}>
                <SyntaxHighlighter
                  language={block.language || 'text'}
                  style={atomDark}
                  showLineNumbers
                >
                  {block.code}
                </SyntaxHighlighter>
              </div>
            ))}
          </div>
        )}

        {/* Sources */}
        {sources.length > 0 && (
          <div className={styles.sourcesSection}>
            <div className={styles.label}>Sources</div>
            <div className={styles.sources}>
              {sources.map((source, index) => (
                <span key={index} className={styles.source}>
                  {source}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResponseDisplay;
