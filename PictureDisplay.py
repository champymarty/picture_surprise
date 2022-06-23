from datetime import datetime, timedelta


class PictureDisplay:
    def __init__(self, timedelta: timedelta, search: str = None, list_name: str = None, max_search: int = None) -> None:
        self.search = search
        self.list_name = list_name
        self.timedelta = timedelta
        self.max_search = max_search
        self.lastSent = datetime.now()
        
    def isListSearch(self) -> bool:
        return not self.list_name is None