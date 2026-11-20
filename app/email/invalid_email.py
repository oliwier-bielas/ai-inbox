class InvalidEmailError(Exception):
    def __init__(self, missing_key: str):
        super().__init__(
            f"Warning: skipping invalid email (missing field: {missing_key})")
