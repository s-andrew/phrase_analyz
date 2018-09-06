import datetime
from functools import total_ordering
from hashlib import md5


class Phrase:
    def __init__(self, phrase_id: int=None, phrase_owner_id: str=None, value: str = None,\
                 create_time: datetime.datetime = None, period: int = None,\
                 words: list= None, grams: list = None):
        self.phrase_id = phrase_id
        self.phrase_owner_id = phrase_owner_id
        self.value = value
        self.create_time = create_time
        self.period = period
        if words is None:
            self.add_words(*words)
        else:
            self.words = words
        if grams is None:
            self.grams = []
        else:
            self.grams = grams
        return

    def add_words(self, *words):
        for word in words:
            if isinstance(word, Word):
                self.words.append(word)
            elif isinstance(word, str):
                self.words.append(Word(value=word))
            else:
                raise TypeError('*words must be list<Word|str>')
        return

    def __str__(self):
        return 'Phrase(phrase_id={phrase_id}, value={value}, words={words}, grams={grams})'.format_map(self.__dict__)

    def __repr__(self):
        return 'Phrase(phrase_id={phrase_id}, value={value}, words={words}, grams={grams})'.format_map(self.__dict__)


@total_ordering
class Word:
    def __init__(self, word_id=None, value: str = None):
        self.word_id = word_id
        self.value = value
        return

    def __str__(self):
        return 'Word(word_id={word_id}, value={value})'.format_map(self.__dict__)

    def __repr__(self):
        return 'Word(word_id={word_id}, value={value})'.format_map(self.__dict__)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if not isinstance(other, Word):
            return False
        return self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, Word):
            return False
        return self.value < other.value


class Gram:
    def __init__(self, gram_id=None, key=None, words:list=None):
        self.gram_id = gram_id
        self.key = key
        self.words = words

    def __str__(self):
        return 'Gram(gram_id={gram_id}, words={words})'.format_map(self.__dict__)

    def __repr__(self):
        return 'Gram(gram_id={gram_id}, words={words})'.format_map(self.__dict__)