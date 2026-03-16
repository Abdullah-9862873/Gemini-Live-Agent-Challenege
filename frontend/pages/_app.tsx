// =============================================================================
// AI Multimodal Tutor - App Component
// =============================================================================
// Phase: 5 - Frontend Development
// Purpose: Main app wrapper
// Version: 5.0.0
// =============================================================================

import type { AppProps } from 'next/app';
import '../styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
