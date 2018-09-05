from sqlalchemy_control import SqlalchemyControl
from sqlalchemy_control.phrase_factory import phrase_consistency_factory

if __name__ == '__main__':
    db = SqlalchemyControl('config/sqlite_connection.json', 'config/schema.json', create=True)
    session = db.get_session()

    phrases = [
        "Hello, I love you, won't you tell me your name",
        "Hello, I love you, let me jump in your game"
    ]

    phrases = [phrase_consistency_factory(text, session) for text in phrases]

