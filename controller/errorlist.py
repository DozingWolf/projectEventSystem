class AuthError(Exception):
    code = 403
    error_code = 1000
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class AuthNoUserError(AuthError):
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class AuthDupUserError(AuthError):
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class AuthNoParaError(AuthError):
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class AuthNoPermissionError(AuthError):
    error_code = 1004
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class UploadError(Exception):
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class UploadNoFileError(UploadError):
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class IntfError(Exception):
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class IntfNoParaError(IntfError):
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class InnerError(Exception):
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class InnerParaError(InnerError):
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class TimerError(Exception):
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

