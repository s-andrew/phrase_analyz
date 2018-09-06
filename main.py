from sqlalchemy_control import SqlalchemyControl
from sqlalchemy_control.phrase_factory import phrase_consistency_factory
from PhrasePreprocessor import PhrasePreprocessor
from get_phrase_gram_keys import get_phrase_gram_keys

if __name__ == '__main__':
    phrases = [
        "Hello, I love you, won't you tell me your name",
        "Hello, I love you, let me jump in your game"
    ]

    db = SqlalchemyControl('config/sqlite_connection.json', 'config/schema.json', create=True)
    session = db.get_session()
    preprocessor = PhrasePreprocessor()
    gram_key_func = lambda words: '_'.join(sorted(words))

    keys = [get_phrase_gram_keys(phrase, preprocessor.normalize, gram_key_func) for phrase in phrases]
    print(*keys, sep='\n')


    phrases = [phrase_consistency_factory(text, 'PHRASE_OWNER_STUB', 666, session,
                                          commit=False, preprocessor=preprocessor.normalize) for text in phrases]
    session.commit()