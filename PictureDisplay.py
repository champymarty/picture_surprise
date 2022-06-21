from datetime import datetime, timedelta


class PictureDisplay:
    def __init__(self, search, timedelta: timedelta, max_search: int) -> None:
        self.search = search
        self.timedelta = timedelta
        self.max_search = max_search
        self.lastSent = datetime.now()
        