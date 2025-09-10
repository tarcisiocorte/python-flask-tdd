class InvalidParamError(Exception):
    def __init__(self, param_name: str):
        self.param_name = param_name
        super().__init__(f"Invalid param: {param_name}")
