from PhrasePreprocessor import PhrasePreprocessor
from phrase_storage import PhraseStorage
from servises import emplace_and_save_phrases, get_owner_grams_keys

if __name__ == '__main__':
    phrases = [
        "Hello, I love you, won't you tell me your name",
        "Hello, I love you, let me jump in your game"
    ]

    owner = 'PHRASE_OWNER_STUB'
    phrases = [(phrase, owner, 666) for phrase in phrases]
    storage = PhraseStorage("sqlite:///:memory:")
    emplace_and_save_phrases(phrases, storage)

    preprocessor = PhrasePreprocessor()
    grams_keys = get_owner_grams_keys([owner], storage, preprocessor.normalize, lambda words: '_'.join(sorted(words)))
    print(*grams_keys, sep='\n')
