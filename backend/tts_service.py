# =============================================================================
# AI Multimodal Tutor - Text-to-Speech (TTS) Service
# =============================================================================
# Phase: 4 - LLM Integration (Voice Output)
# Purpose: Convert text responses to audio
# Version: 4.0.0
# =============================================================================

from typing import Optional
import logging
import base64
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TTSService:
    """
    Text-to-Speech Service.
    
    This class handles converting text to speech.
    Uses gTTS (free) as primary, with Google Cloud TTS as option.
    
    Attributes:
        language: Target language code
        speed: Speech speed (0.5 to 2.0)
    """
    
    def __init__(
        self,
        language: str = "en",
        speed: float = 1.0
    ):
        """
        Initialize the TTS service.
        
        Args:
            language: Language code (e.g., "en", "es", "fr")
            speed: Speech speed (0.5 to 2.0)
        """
        self.language = language
        self.speed = speed
        self.gtts_available = False
        
        # Try to import gTTS
        try:
            from gtts import gTTS
            self.gtts = gTTS
            self.gtts_available = True
            logger.info("gTTS available for TTS")
        except ImportError:
            logger.warning("gTTS not available. Run: pip install gtts")
            self.gtts = None
    
    def text_to_speech(
        self,
        text: str,
        lang: Optional[str] = None
    ) -> dict:
        """
        Convert text to speech.
        
        Args:
            text: Text to convert to speech
            lang: Language code (uses default if None)
        
        Returns:
            Dictionary with audio data and metadata
        
        Example:
            >>> tts = TTSService()
            >>> result = tts.text_to_speech("Hello, world!")
            >>> audio_base64 = result["audio_base64"]
        """
        lang = lang or self.language
        
        # Check if gTTS is available
        if not self.gtts_available:
            return {
                "status": "error",
                "message": "gTTS not installed. Run: pip install gtts",
                "audio_base64": None
            }
        
        try:
            # Generate speech
            tts = self.gtts(text=text, lang=lang, slow=(self.speed < 1.0))
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            # Convert to base64
            audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
            
            logger.info(f"Generated TTS audio ({len(audio_base64)} bytes)")
            
            return {
                "status": "success",
                "audio_base64": audio_base64,
                "language": lang,
                "text_length": len(text),
                "message": "Audio generated successfully"
            }
        
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            return {
                "status": "error",
                "message": str(e),
                "audio_base64": None
            }
    
    def text_to_speech_file(
        self,
        text: str,
        output_path: str,
        lang: Optional[str] = None
    ) -> dict:
        """
        Convert text to speech and save to file.
        
        Args:
            text: Text to convert
            output_path: Path to save audio file
            lang: Language code
        
        Returns:
            Dictionary with status
        """
        lang = lang or self.language
        
        if not self.gtts_available:
            return {
                "status": "error",
                "message": "gTTS not installed"
            }
        
        try:
            tts = self.gtts(text=text, lang=lang, slow=(self.speed < 1.0))
            tts.save(output_path)
            
            logger.info(f"Saved TTS audio to {output_path}")
            
            return {
                "status": "success",
                "file_path": output_path,
                "message": f"Audio saved to {output_path}"
            }
        
        except Exception as e:
            logger.error(f"TTS file generation failed: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def generate_preview(
        self,
        text: str,
        max_chars: int = 500
    ) -> dict:
        """
        Generate TTS preview (truncated text).
        
        Args:
            text: Full text
            max_chars: Maximum characters for preview
        
        Returns:
            Dictionary with preview audio
        """
        # Truncate text if too long
        preview_text = text[:max_chars]
        if len(text) > max_chars:
            preview_text += "..."
        
        return self.text_to_speech(preview_text)


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

tts_service = TTSService()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def text_to_speech(
    text: str,
    language: str = "en"
) -> dict:
    """
    Convert text to speech.
    
    Convenience function.
    
    Args:
        text: Text to convert
        language: Language code
    
    Returns:
        Dictionary with audio data
    """
    tts = TTSService(language=language)
    return tts.text_to_speech(text)


def generate_voice_response(
    answer: str,
    language: str = "en"
) -> dict:
    """
    Generate voice response for an answer.
    
    Convenience function.
    
    Args:
        answer: Text answer
        language: Language code
    
    Returns:
        Dictionary with answer and audio
    """
    tts = TTSService(language=language)
    audio_result = tts.text_to_speech(answer)
    
    return {
        "answer": answer,
        "audio": audio_result.get("audio_base64"),
        "audio_status": audio_result.get("status"),
        "language": language
    }
