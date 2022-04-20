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

class AuthError(Exception):
    code = '401'
    error_code = '1400'
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, arguname, status)
        self.message = message
        self.status = status
        self.arguname = arguname

class AuthNoUserNameError(AuthError):
    error_code = '1401'
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, arguname, status)
        self.message = message
        self.status = status
        self.arguname = arguname

class AuthNoPasswdError(AuthError):
    error_code = '1402'
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, arguname, status)
        self.message = message
        self.status = status
        self.arguname = arguname

class AuthDupUserError(AuthError):
    error_code = '1403'
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status
        self.arguname = arguname

class AuthNoPermissionError(AuthError):
    error_code = '1404'
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, status)
        self.message = message
        self.status = status
        self.arguname = arguname

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

class DBDataError(Exception):
    code = '523'
    error_code = '1700'
    def __init__(self, message, arguname, status=-1):
        super().__init__(message, arguname, status)
        self.message = message
        self.status = status
        self.arguname = arguname