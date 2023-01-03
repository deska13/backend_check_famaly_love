from enum import Enum


class LeisurePreferencesCoincideEnum(Enum):
    NO = 'Не совпадают'
    PARTLY = '50/50'
    YES = 'Совпадают'


class EducationLevelEnum(Enum):
    NO = 'Не совпадают'
    YES = 'Совпадают'


class HousingEnum(Enum):
    NO = 'Не своя'
    YES = 'Своя'
    MORTAGE = 'Ипотека'


class ExploreTogetherEnum(Enum):
    NO = 'Нет'
    SOMETIMES = 'Иногда'
    YES = 'Всегда'


class ExchangeIdeasEnum(Enum):
    NO = 'Нет'
    SOMETIMES = 'Иногда'
    YES = 'Всегда'
