"""
    A file dedicated to custom errors to more specifically identify errors.
"""


class SubredditInaccessibleError(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)


class DataIsNoneError(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)


class DateError(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)


class ConfigFileNotFound(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)
