class InvalidCredentialsError(Exception):
    def __init__(self, message: str = "Wrong e-mail or password"):
        super().__init__(message)
