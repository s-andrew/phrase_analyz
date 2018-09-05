from functools import reduce
import json

SCHEMA_NAME = 'schema_name'
TABLE_NAME = 'table_name'
TABLES = 'tables'

def dict_xpath(root: dict, path: str, sch='/'):
    return reduce(lambda acc, nxt: acc[nxt], path.split(sch), root)


def scheme_mapper_factory(config_file:str, schema_in_name:bool=False, path_sch:str='.',
                          esc:str='"', esc_close:str=None, special_keys:dict=None):
    with open(config_file) as file:
        config = json.loads(file.read())
    schema_name = config[SCHEMA_NAME] if schema_in_name else None
    tables = config[TABLES]
    if special_keys is None:
        special_keys = dict()
    return SchemeMapper(tables, schema_name, path_sch, esc, esc_close, special_keys)


class SchemeMapper():
    def __init__(self, tables:dict, schema_name:str=None, path_sch:str='.',
                 esc:str='"', esc_close:str=None, special_keys:dict=None):
        self.tables = tables
        self.schema_name = schema_name
        self.path_sch = path_sch
        self.esc = esc
        if esc_close is not None:
            self.esc_close = esc_close
        else:
            self.esc_close = esc
        if special_keys is not None:
            self.special_keys = special_keys
        else:
            self.special_keys = dict()
        return

    def __getitem__(self, item):
        return self.special_keys.get(item, self.__get_object_name(item))

    def __escape_object_name(self, o):
        return str(self.esc) + str(o) + str(self.esc_close)

    def __get_object_name(self, path):
        if path[0] == '.':
            o = dict_xpath(self.tables, path[1:], sch=self.path_sch)
            return self.__escape_object_name(o)
        first_sch = path.find(self.path_sch)
        table_key, other = path[:first_sch], path[first_sch+1:]
        table = dict_xpath(self.tables, table_key, sch=self.path_sch)
        result = []
        if self.schema_name is not None:
            result.append(self.schema_name)
        result.append(dict_xpath(table, TABLE_NAME, sch=self.path_sch))
        if other != TABLE_NAME:
            result.append(dict_xpath(table, other, sch=self.path_sch))
        return '.'.join(map(self.__escape_object_name, result))


