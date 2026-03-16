// =============================================================================
// AI Multimodal Tutor - Question Input Component
// =============================================================================
// Phase: 5 - Frontend Development
// Purpose: Text input for asking questions
// Version: 5.0.0
// =============================================================================

import React, { useState, KeyboardEvent } from 'react';
import styles from '../styles/QuestionInput.module.css';

interface QuestionInputProps {
  onSubmit: (question: string) => void;
  isLoading: boolean;
  disabled?: boolean;
}

/**
 * QuestionInput Component
 * 
 * Provides a text input field for users to type their questions.
 * Supports submitting via Enter key or clicking the submit button.
 */
const QuestionInput: React.FC<QuestionInputProps> = ({
  onSubmit,
  isLoading,
  disabled = false,
}) => {
  const [question, setQuestion] = useState<string>('');

  const handleSubmit = () => {
    if (question.trim() && !isLoading && !disabled) {
      onSubmit(question.trim());
      setQuestion('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Submit on Enter (without shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.inputWrapper}>
        <textarea
          className={styles.textarea}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your course..."
          disabled={disabled || isLoading}
          rows={3}
        />
        
        <button
          className={styles.submitButton}
          onClick={handleSubmit}
          disabled={!question.trim() || isLoading || disabled}
        >
          {isLoading ? (
            <span className={styles.loadingIcon}>...</span>
          ) : (
            <span>Ask</span>
          )}
        </button>
      </div>
      
      <div className={styles.hint}>
        Press Enter to submit, Shift+Enter for new line
      </div>
    </div>
  );
};

export default QuestionInput;
