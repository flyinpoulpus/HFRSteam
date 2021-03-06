from enum import Enum, auto


class Category(Enum):
    Game       = auto()
    DLC        = auto()
    Collection = auto()


class HFRData:
    def __init__(self, is_available, requirements):
        self.is_available = is_available
        self.requirements = requirements
        self.gift_date    = None


class StoreData:
    def __init__(self):
        self.description  = ''
        self.image        = ''
        self.os           = list()
        self.price        = None
        self.price_date   = ''
        self.genres       = list()
        self.release_date = None
        self.link         = ''
        self.category     = None
        self.avg_review   = None
        self.cnt_review   = None
        self.tags         = list()
        self.details      = list()


class Game:
    def __init__(self, is_available=False, requirements=None):
        self.hfr          = HFRData(is_available, requirements)
        self.store        = StoreData()

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
