import json
from xml.dom import minidom
from typing import List, Tuple, Callable

from phrase_storage import PhraseStorage, Phrase
from phrase_tools import PhraseText, PhraseOwnerId, Period, emplace_and_save_phrases, get_owner_grams_keys
from models import CrossModel


class PhraseNotFoundInXml(Exception):
    pass


def xml_parse(xml_str: str) -> List(Tuple[PhraseText, PhraseOwnerId, Period]):
    xml = minidom.parseString(xml_str)
    owner: PhraseOwnerId = xml.getElementsByTagName('id')[0].childnodes[0].data
    phrases_tags = xml.getElementsByTagName('phrase')
    phrases_details = [(tag.childNodes[0].data, owner, tag.getAttribute('period')) for tag in phrases_tags]
    return phrases_details


def save_xml_data(xml_str: str, storage:PhraseStorage) -> List[Phrase]:
    phrases_details = xml_parse(xml_str)
    if len(phrases_details) == 0:
        raise PhraseNotFoundInXml('Phrase not found in xml!')
    return emplace_and_save_phrases(phrases_details, storage)



def load_model(models_id: int) -> CrossModel:
    with open('') as file:
        models_dict = json.loads(file.read())
    return CrossModel.fromDict(models_dict)


def predict_risk_group_by_owner(owner_list: List[str], models_id: List[int], storage: PhraseStorage,
                                preprocessor: Callable[[str], Tuple[str]]):
    grams_key = get_owner_grams_keys(owner_list, storage, preprocessor, lambda words: '_'.join(sorted(words)))
    prediction = dict()
    for model_id in models_id:
        model = load_model(model_id)
        prediction.update({model_id: model.getRiskGroup(list(grams_key))})
    return prediction
