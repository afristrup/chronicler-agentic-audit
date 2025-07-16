"""
Exception classes for Chronicler services
"""


class ChroniclerError(Exception):
    """Base exception for Chronicler service errors"""

    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class RegistryError(ChroniclerError):
    """Exception raised for registry-related errors"""

    pass


class AuditError(ChroniclerError):
    """Exception raised for audit-related errors"""

    pass


class AccessControlError(ChroniclerError):
    """Exception raised for access control errors"""

    pass


class ConfigurationError(ChroniclerError):
    """Exception raised for configuration errors"""

    pass


class NetworkError(ChroniclerError):
    """Exception raised for network-related errors"""

    pass
