class InvalidRefreshToken(Exception):
    def __init__(self, message: str = "Invalid refresh token"):
        super().__init__(message)
