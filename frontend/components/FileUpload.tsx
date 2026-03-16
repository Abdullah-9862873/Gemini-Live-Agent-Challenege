// =============================================================================
// AI Multimodal Tutor - File Upload Component
// =============================================================================
// Phase: 5 - Frontend Development
// Purpose: Upload code files or screenshots
// Version: 5.0.0
// =============================================================================

import React, { useState, useRef } from 'react';
import styles from '../styles/FileUpload.module.css';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  disabled?: boolean;
  accept?: string;
}

/**
 * FileUpload Component
 * 
 * Provides file upload functionality for:
 * - Code snippets (.py, .js, .ts, .java, etc.)
 * - Screenshots (.png, .jpg, .jpeg)
 */
const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  disabled = false,
  accept = '.py,.js,.ts,.java,.cpp,.c,.go,.rs,.txt,.md,.png,.jpg,.jpeg',
}) => {
  const [preview, setPreview] = useState<string | null>(null);
  const [fileName, setFileName] = useState<string>('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setFileName(file.name);

    // Create preview for images
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    } else {
      // For code files, read as text
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target?.result as string);
      };
      reader.readAsText(file);
    }

    onFileSelect(file);
  };

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleClear = () => {
    setPreview(null);
    setFileName('');
    if (inputRef.current) {
      inputRef.current.value = '';
    }
  };

  return (
    <div className={styles.container}>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={handleFileChange}
        disabled={disabled}
        className={styles.hiddenInput}
      />
      
      <button
        className={styles.uploadButton}
        onClick={handleClick}
        disabled={disabled}
      >
        <span className={styles.uploadIcon}>📎</span>
        Upload
      </button>

      {fileName && (
        <div className={styles.fileInfo}>
          <span className={styles.fileName}>{fileName}</span>
          <button className={styles.clearButton} onClick={handleClear}>
            ✕
          </button>
        </div>
      )}

      {preview && (
        <div className={styles.preview}>
          {fileName.match(/\.(png|jpg|jpeg)$/i) ? (
            <img src={preview} alt="Preview" className={styles.imagePreview} />
          ) : (
            <pre className={styles.codePreview}>{preview}</pre>
          )}
        </div>
      )}
    </div>
  );
};

export default FileUpload;
