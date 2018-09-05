import datetime
from sqlalchemy import Table, Column, Integer, String, UnicodeText, DateTime, MetaData, ForeignKey


def metadata_factory(scheme_mapper):
    metadata = MetaData()

    phrases = Table(scheme_mapper['phrases.table_name'], metadata,
                    Column(scheme_mapper['.phrases.columns.phrase_id'], Integer, primary_key=True, key='phrase_id'),
                    Column(scheme_mapper['.phrases.columns.phrase_owner_id'], String(50), nullable=False, key='phrase_owner_id'),
                    Column(scheme_mapper['.phrases.columns.value'], String(255), default='', key='value'),
                    Column(scheme_mapper['.phrases.columns.create_time'], DateTime, default=datetime.datetime.now(), key='create_time'),
                    Column(scheme_mapper['.phrases.columns.period'], Integer, nullable=False, key='period')
                    )

    words = Table(scheme_mapper['words.table_name'], metadata,
                  Column(scheme_mapper['.words.columns.word_id'], Integer, primary_key=True, key='word_id'),
                  Column(scheme_mapper['.words.columns.value'], String(100), unique=True, key='value')
                  )

    grams = Table(scheme_mapper['grams.table_name'], metadata,
                  Column(scheme_mapper['.grams.columns.gram_id'], Integer, primary_key=True, key='gram_id'),
                  Column(scheme_mapper['.grams.columns.key'], String(256), unique=True, key='key')
                  )

    phrase_word = Table(scheme_mapper['phrase_word.table_name'], metadata,
                        Column(scheme_mapper['.phrase_word.columns.phrase_id'], Integer, ForeignKey(phrases.c.phrase_id),
                               primary_key=True, key='phrase_id'),
                        Column(scheme_mapper['.phrase_word.columns.word_id'], Integer, ForeignKey(words.c.word_id),
                               primary_key=True, key='word_id')
                        )

    phrase_gram = Table(scheme_mapper['phrase_gram.table_name'], metadata,
                        Column(scheme_mapper['.phrase_gram.columns.phrase_id'], Integer, ForeignKey(phrases.c.phrase_id),
                               primary_key=True,  key='phrase_id'),
                        Column(scheme_mapper['.phrase_gram.columns.gram_id'], Integer, ForeignKey(grams.c.gram_id),
                               primary_key=True, key='gram_id')
                        )

    gram_word = Table(scheme_mapper['gram_word.table_name'], metadata,
                      Column(scheme_mapper['.gram_word.columns.gram_id'], Integer, ForeignKey(grams.c.gram_id), primary_key=True, key='gram_id'),
                      Column(scheme_mapper['.gram_word.columns.word_id'], Integer, ForeignKey(words.c.word_id), primary_key=True, key='word_id')
                      )

    tables = dict(
        phrases=phrases,
        words=words,
        grams=grams,
        phrase_word=phrase_word,
        phrase_gram=phrase_gram,
        gram_word=gram_word
    )
    return metadata, tables
