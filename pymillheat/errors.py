class MillHeatException(Exception):
    """Base exception class for Pymillheat."""
    pass

class ApplyAuthCode(MillHeatException):
    """This exception is raised when apply auth code error."""
    pass

class MillHeatSystem(MillHeatException):
    """This exception is raised when system error"""
    pass

class MillHeatUds(MillHeatException):
    """This exception is raised when uds error"""
    pass

class AccessToken(MillHeatException):
    """This exception is raised when access token error."""
    pass

class RefreshToken(MillHeatException):
    """This exception is raised when refresh token error."""
    pass

class DeviceControlForOpenApi(MillHeatException):
    """This exception is raised when device control for open api error."""
    pass
