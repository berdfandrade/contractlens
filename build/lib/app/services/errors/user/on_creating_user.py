class ErrorOnCreatingUser(ValueError):
    def __init__(self, message: str = "Error on creating user"):
        super().__init__(message)
