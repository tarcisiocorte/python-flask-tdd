class AccessDeniedError(Exception):
    def __init__(self):
        super().__init__("Access denied")
