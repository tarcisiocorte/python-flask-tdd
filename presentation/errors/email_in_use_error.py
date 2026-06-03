class EmailInUseError(Exception):
    def __init__(self):
        super().__init__("Email already in use")
