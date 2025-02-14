class Missing(Exception):
    def __init__(self, msg:str):
        self.msg = msg


class Duplicate(Exception):
    def __init__(self, msg:str):
        self.msg = msg


class Validation(Exception):
    def __init__(self, msg:str):
        self.msg = msg
