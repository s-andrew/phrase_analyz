from typing import List, Tuple, Callable

from phrase_storage import PhraseStorage
from phrase_tools import PhraseText, PhraseOwnerId, Period, emplace_and_save_phrases, get_owner_grams_keys
from models import CrossModel


def xml_parse(xml_str: str) -> List(Tuple[PhraseText, PhraseOwnerId, Period]):
    return []


def save_xml_data(xml_str: str, storage:PhraseStorage) -> None:
    phrases_details = xml_parse(xml_str)
    emplace_and_save_phrases(phrases_details, storage)
    return


def load_model() -> CrossModel:
    pass


def predict_risk_group_by_owner(owner_list: List[str], storage: PhraseStorage,
                                preprocessor: Callable[[str], Tuple[str]]):
    model = load_model()
    grams_key = get_owner_grams_keys(owner_list, storage, preprocessor, lambda words: '_'.join(sorted(words)))
    return model.getRiskGroup(grams_key)
