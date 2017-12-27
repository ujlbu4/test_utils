class Language:
    EN = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    RU = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


class Country:
    _reference = {
        'ru': Language.RU,
        'us': Language.EN
    }

    def __init__(self, country):
        self.country = country.lower()
        self.language = self._reference[self.country]
