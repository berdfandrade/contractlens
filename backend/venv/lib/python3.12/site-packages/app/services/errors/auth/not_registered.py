class EmailNotRegistered(Exception):
    def __init__(self, message: str = "e-mail not registered"):
        super().__init__(message)
