class CheckError(Exception):
    def __init__(self, name, actual, expected):
        self.name = name
        self.actual = actual
        self.expected = expected
        super().__init__(f"FAIL: {name} = {actual}, expected {expected}!")
