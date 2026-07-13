"""Custom exception types for the App Store scraper."""


class AppStoreException(Exception):
    """Thrown when an error occurs in the App Store scraper."""


class NotFoundError(AppStoreException):
    """Raised when Apple returns no matching app for a requested ID."""


class TemporaryBlockException(AppStoreException):
    """Raised when the App Store temporarily blocks or rate-limits requests."""
