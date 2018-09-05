import re
from itertools import combinations
from collections import Callable

from sqlalchemy.orm import sessionmaker, Session

from .models import Phrase, Word, Gram

REGEX = re.compile(r'[^\sa-zA-Zа-яА-Я]')
Session = sessionmaker()


def default_preprocessor(text):
    return REGEX.sub('', text).lower().split()



def phrase_consistency_factory(text:str, session:Session, preprocessor:Callable=None):
    if preprocessor is None:
        preprocessor = default_preprocessor
    words_values = set(preprocessor(text))
    exist_words = session.query(Word).filter(Word.value.in_(words_values)).all()
    exist_words_map = {word.value: word for word in exist_words}
    words = [exist_words_map.get(value, Word(value=value)) for value in words_values]
    session.add_all(words)
    session.flush()

    grams_words = list(set(combinations(words, 3)))
    grams_keys = list(map(gram_key_function, grams_words))
    exist_grams = session.query(Gram).filter(Gram.key.in_(grams_keys)).all()
    exist_gram_map = {gram.key: gram for gram in exist_grams}
    grams = [exist_gram_map.get(key, Gram(key=key, words=list(words))) for key, words in zip(grams_keys, grams_words)]
    session.add_all(grams)
    session.flush()

    phrase = Phrase(phrase_owner_id='PHRASE_OWNER_STUB', value=text, period=666, words=words, grams=grams)
    session.add(phrase)
    session.commit()
    return phrase


def gram_key_function(words):
    return '_'.join(sorted(map(lambda w: str(w.word_id), words)))