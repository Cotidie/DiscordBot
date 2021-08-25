from pymongo.collection import Collection


class RaidTime(Collection):
    def __init__(self, db, col_name):
        super().__init__(db, col_name)