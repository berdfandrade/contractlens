class MustProvideSecretKeyError(ValueError):
    def __init__(self, message: str = "Must Provide secret key"):
        super().__init__(message)
