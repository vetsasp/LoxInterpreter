from app.runtime import MyRuntimeError


class ReturnExcept(MyRuntimeError):
    def __init__(self, val):
        super().__init__(self, val)
        self.val = val