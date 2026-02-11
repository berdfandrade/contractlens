class UserAlreadyExistsError(ValueError):
    def __init__(self, message: str = "User already exists"):
        super().__init__(message)
