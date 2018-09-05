import json
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .metadata_factory import metadata_factory
from .metadata_mapper import map_model
from .models import Phrase, Word, Gram
from .schema_mapper import scheme_mapper_factory


def connection_string_from_config(file_name:str):
    with open(file_name) as file:
        config = json.loads(file.read())
    connection_string = config.get('connection_string')
    params = {k: quote_plus(v) for k, v in config.get('connection_params', dict()).items()}
    connection_string = connection_string.format_map(params)
    return connection_string


class SqlalchemyControl:
    def __init__(self, connection_config_file, scheme_config_file, create=False):
        scheme_mapper = scheme_mapper_factory(scheme_config_file, esc='')
        connection_string = connection_string_from_config(connection_config_file)
        self.metadata, tables = metadata_factory(scheme_mapper)
        map_model(tables, Phrase, Word, Gram)
        self.engine = create_engine(connection_string, echo=True)
        self.metadata.create_all(self.engine)
        self.get_session = sessionmaker(bind=self.engine)
        return