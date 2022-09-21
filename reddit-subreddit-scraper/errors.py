class SubredditInaccessibleError(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)


class DataIsNoneError(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)


class DateError(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)
