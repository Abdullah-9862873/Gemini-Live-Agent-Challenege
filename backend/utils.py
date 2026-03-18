import re
import os

def sanitize_error_message(error_text: str) -> str:
    """
    Remove sensitive information from error messages to prevent API key exposure.
    """
    if not error_text:
        return "An unknown error occurred"
    
    sanitized = error_text
    
    api_key_patterns = [
        r'(Bearer\s+)[A-Za-z0-9_\-]+',
        r'(bearer\s+)[A-Za-z0-9_\-]+',
        r'(api_key["\']?\s*[:=]\s*["\']?)[A-Za-z0-9_\-]+',
        r'(api-key["\']?\s*[:=]\s*["\']?)[A-Za-z0-9_\-]+',
        r'gsk_[A-Za-z0-9_\-]{20,}',
        r'(pin_[A-Za-z0-9_\-]{20,})',
        r'(hf_[A-Za-z0-9]{20,})',
        r'(github_pat_[A-Za-z0-9_\-]{20,})',
        r'(xox[baprs]-[A-Za-z0-9]{10,})',
    ]
    
    for pattern in api_key_patterns:
        sanitized = re.sub(pattern, r'\1[REDACTED]', sanitized)
    
    return sanitized


def safe_error_response(original_error: str, user_message: str = "An error occurred while processing your request") -> str:
    """
    Return a safe error message to the user without exposing sensitive data.
    """
    return user_message


def log_sanitized_error(logger, error_text: str, extra_context: str = ""):
    """
    Log an error message with sensitive data redacted.
    """
    sanitized = sanitize_error_message(error_text)
    if extra_context:
        logger.error(f"{extra_context}: {sanitized}")
    else:
        logger.error(sanitized)
