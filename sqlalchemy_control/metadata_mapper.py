from sqlalchemy.orm import  mapper, relationship


def map_model(tables, Phrase, Word, Gram):

    mapper(Phrase, tables['phrases'],
           properties=dict(
               words=relationship(Word, tables['phrase_word']),
               grams=relationship(Gram, tables['phrase_gram'])
           ))
    mapper(Word, tables['words'],
           properties=dict(
               phrases=relationship(Phrase, tables['phrase_word']),
               grams=relationship(Word, tables['gram_word'])
           ))
    mapper(Gram, tables['grams'],
           properties=dict(
               words=relationship(Word, tables['gram_word']),
               phrases=relationship(Phrase, tables['phrase_gram'])
           ))