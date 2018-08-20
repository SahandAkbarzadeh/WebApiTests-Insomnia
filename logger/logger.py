class Logger:
    __instance = None

    _debug_messages: [str] = []

    @staticmethod
    def get() -> 'Logger':
        """ Static access method. """
        if Logger.__instance is None:
            Logger()
        return Logger.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Logger.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Logger.__instance = self

    def debug(self, message: str):
        self._debug_messages.append(message)
        print(message)
