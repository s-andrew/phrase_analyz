import re
from typing import List, Tuple

import pymorphy2


class PhrasePreprocessor:
    def __init__(self, regex: List[str]=None, min_max_word_len: Tuple[int, int]=(1, 10),
                 min_max_phrase_len: Tuple[int, int]=(1, 100), stop_pos: List[str]=None):
        if regex is not None:
            self.regex = list(map(lambda r: re.compile(r), regex))
        else:
            self.regex = []
        self.morph = pymorphy2.MorphAnalyzer()
        self.min_word_len, self.max_word_len = min_max_word_len
        self.min_phrase_len, self.max_phrase_len = min_max_phrase_len
        if stop_pos is not None:
            self.stop_pos = stop_pos
        else:
            self.stop_pos = []

    def normalize(self, text: str):
        text = text.lower()
        for r in self.regex:
            text = r.sub(' ', text)
        words = text.split()
        words = map(lambda w: w.strip(), words)
        words = filter(lambda w: self.min_word_len <= len(w) <= self.max_word_len, words)
        words = map(self.word_normalize, words)
        words = filter(lambda wp: wp[1] not in self.stop_pos, words)
        words = map(lambda wp: wp[0], words)
        words = list(set(words))
        return words

    def word_normalize(self, word: str):
        w = self.morph.parse(word)
        w = w[0]
        return w.normal_form, w.tag.POS


