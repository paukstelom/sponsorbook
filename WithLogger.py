import structlog


class WithLogger:
    def __init__(self):
        self.log = structlog.getLogger(self.__class__.__name__)
