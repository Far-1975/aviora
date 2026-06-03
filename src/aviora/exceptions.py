class AvioraError(Exception):
    """Base exception for Aviora."""


class AvioraAuthError(AvioraError):
    """Raised when authentication fails (invalid API key)."""


class AvioraRateLimitError(AvioraError):
    """Raised when the API rate limit is exceeded."""
