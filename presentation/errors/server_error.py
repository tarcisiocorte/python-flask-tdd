class ServerError(Exception):
    def __init__(self):
        super().__init__("Internal server error")

