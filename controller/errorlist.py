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

class TimerError(Exception):
    def __init__(self, message, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status

class InnerArgumentError(Exception):
    code = '520'
    error_code = 1500
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, arguname, status)
        self.message = message
        self.status = status
        self.arguname = arguname

class InnerArgumentInputError(InnerArgumentError):
    code = '520'
    error_code = 1501
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, arguname, status)
        self.message = message
        self.status = status
        self.arguname = arguname

class InnerArgumentOutputError(InnerArgumentError):
    code = '520'
    error_code = 1502
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, arguname, status)
        self.message = message
        self.status = status
        self.arguname = arguname

class PostParaError(Exception):
    code = '521'
    error_code = '1600'
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, arguname, status)
        self.message = message
        self.status = status
        self.arguname = arguname

class PostNoParaError(PostParaError):
    code = '521'
    error_code = '1601'
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, arguname, status)
        self.message = message
        self.status = status
        self.arguname = arguname

class PostParaEmptyError(PostParaError):
    error_code = '1602'
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, arguname, status)
        self.message = message
        self.status = status
        self.arguname = arguname