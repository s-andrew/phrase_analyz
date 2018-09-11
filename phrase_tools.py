from typing import List, Tuple, Set, Callable, NewType
from itertools import combinations, chain

from phrase_storage import Phrase, PhraseStorage

PhraseText = NewType('PhraseText', str)
PhraseOwnerId = NewType('PhraseOwnerId', str)
Period = NewType('Period', int)


def create_phrase_with_required_attrs(value: PhraseText, phrase_owner_id: PhraseOwnerId, period: Period) -> Phrase:
    return Phrase(value=value, phrase_owner_id=phrase_owner_id, period=period)


def save_phrases(phrases: List[Phrase], storage: PhraseStorage) -> None:
    session = storage.get_session()
    session.add_all(phrases)
    session.commit()
    return


def emplace_and_save_phrases(phrases_details: List[Tuple[PhraseText, PhraseOwnerId, Period]],
                             storage: PhraseStorage) -> List[Phrase]:
    phrases = [create_phrase_with_required_attrs(*phrd) for phrd in phrases_details]
    save_phrases(phrases, storage)
    return phrases


def get_phrases_by_owner_id(owners_list: List[str], storage: PhraseStorage) -> List[Phrase]:
    session = storage.get_session()
    return session.query(Phrase).filter(Phrase.phrase_owner_id.in_(owners_list)).all()


def generate_phrase_grams_keys(phrase: Phrase, preprocessor: Callable[[str], Tuple[str]],
                               gram_key_generator: Callable[[Tuple[str, ...]], str], gram_size: int) -> List[str]:
    words = preprocessor(phrase.value)
    return [gram_key_generator(words_) for words_ in combinations(words, gram_size)]


def get_owner_grams_keys(owners_list: List[str], storage: PhraseStorage, preprocessor: Callable[[str], Tuple[str]],
                         gram_key_generator: Callable[[Tuple[str, ...]], str], gram_size: int = 3) -> Set[str]:
    phrases = get_phrases_by_owner_id(owners_list, storage)
    return set(chain(*[generate_phrase_grams_keys(phrase, preprocessor, gram_key_generator, gram_size) for phrase in phrases]))
