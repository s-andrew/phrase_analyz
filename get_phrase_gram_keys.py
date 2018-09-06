from itertools import combinations
from typing import Callable


def get_phrase_gram_keys(phrase: str, preprocessor: Callable, gram_key_function: Callable):
    words = preprocessor(phrase)
    return [gram_key_function(words_) for words_ in combinations(words, 3)]
