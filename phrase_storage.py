import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData

from schema_mapper import scheme_mapper_factory


scheme_mapper = scheme_mapper_factory('config/schema.json', esc='')
metadata = MetaData()
phrases = Table(scheme_mapper['phrases.table_name'], metadata,
                Column(scheme_mapper['.phrases.columns.phrase_id'], Integer, primary_key=True, key='phrase_id'),
                Column(scheme_mapper['.phrases.columns.phrase_owner_id'], String(50), nullable=False, key='phrase_owner_id'),
                Column(scheme_mapper['.phrases.columns.value'], String(255), default='', key='value'),
                Column(scheme_mapper['.phrases.columns.create_time'], DateTime, default=datetime.datetime.now(), key='create_time'),
                Column(scheme_mapper['.phrases.columns.period'], Integer, nullable=False, key='period')
                )


class Phrase:
    def __init__(self, phrase_id: int=None, phrase_owner_id: str=None, value: str=None,
                 create_time: datetime.datetime=None, period: int=None):
        if phrase_id is not None:
            self.phrase_id = phrase_id
        if phrase_owner_id is not None:
            self.phrase_owner_id = phrase_owner_id
        if value is not None:
            self.value = value
        if create_time is not None:
            self.create_time = create_time
        if period is not None:
            self.period = period
        return


mapper(Phrase, phrases)


class PhraseStorage:
    def __init__(self, sqlalchemy_connection_string: str):
        self.metadata = metadata
        self.engine = create_engine(sqlalchemy_connection_string)
        self.metadata.create_all(self.engine)
        self.get_session = sessionmaker(bind=self.engine)
        return

