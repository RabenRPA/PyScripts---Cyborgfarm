from json import JSONEncoder

class Language:
    def __init__(self, iso2=None, language_prob=None):
        self.iso2 = iso2
        self.language_prob = language_prob


class LanguageEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__