from collections import namedtuple
from pydoc import locate

from pymongo import MongoClient


phrase_fields_schema = {
    'fields': [
        {'name': 'phrase_owner_id', 'type': 'str', 'required':True},
        {'name': 'value', 'type': 'str', 'required':True},
        {'name': 'period', 'type': 'int'}
    ]
}

Field = namedtuple('Field', 'name type required')

PHRASE_FIELDS = [Field(field['name'], field['type'], field.get('required', False)) for field in phrase_fields_schema['fields']]


def phrase_validator(phrase:dict):
    required_fields = {'phrase_owner_id', 'value', 'period'}
    optional_fields = {}

    for field in PHRASE_FIELDS:
        value = phrase.get(field['name'])
        if value is None and field['required']:
            raise KeyError()
        if isinstance()


class MongoStorage:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)

    def save_phrase(self, text:str, phrase_owner_id:str, period:int):
        phrase = dict(
            phrase_owner_id=phrase_owner_id,
            value=text,
            period=period
        )