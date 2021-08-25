from pymongo.collection import Collection


class EventToday(Collection):
    def __init__(self, db, col_name):
        super().__init__(db, col_name)