"""
OpsPilot — Custom Exceptions
==============================
Application-specific exception classes for clean error handling.
"""

from typing import Any


class OpsPilotError(Exception):
    """Base exception for all OpsPilot errors."""

    def __init__(self, message: str = "An unexpected error occurred", details: Any = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class NotFoundError(OpsPilotError):
    """Raised when a requested resource is not found."""

    def __init__(self, resource: str = "Resource", resource_id: str = ""):
        message = f"{resource} not found"
        if resource_id:
            message = f"{resource} with id '{resource_id}' not found"
        super().__init__(message=message)


class AlreadyExistsError(OpsPilotError):
    """Raised when attempting to create a resource that already exists."""

    def __init__(self, resource: str = "Resource", field: str = "", value: str = ""):
        message = f"{resource} already exists"
        if field and value:
            message = f"{resource} with {field} '{value}' already exists"
        super().__init__(message=message)


class AuthenticationError(OpsPilotError):
    """Raised on authentication failures."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message)


class AuthorizationError(OpsPilotError):
    """Raised when a user lacks permission for an action."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message)


class ValidationError(OpsPilotError):
    """Raised when input validation fails at the service layer."""

    def __init__(self, message: str = "Validation error", details: Any = None):
        super().__init__(message=message, details=details)


class ExternalServiceError(OpsPilotError):
    """Raised when an external service (LLM, Neo4j, ChromaDB) fails."""

    def __init__(self, service: str = "External service", message: str = ""):
        full_message = f"{service} error"
        if message:
            full_message = f"{service}: {message}"
        super().__init__(message=full_message)


class DocumentProcessingError(OpsPilotError):
    """Raised when document processing (OCR, parsing, embedding) fails."""

    def __init__(self, message: str = "Document processing failed", details: Any = None):
        super().__init__(message=message, details=details)


class BadRequestError(OpsPilotError):
    """Raised when the client sends a bad or malformed request."""

    def __init__(self, message: str = "Bad request", details: Any = None):
        super().__init__(message=message, details=details)
