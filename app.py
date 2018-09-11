import logging.config
import json

import colorama
from flask import Flask, jsonify, request

from PhrasePreprocessor import PhrasePreprocessor
from phrase_storage import PhraseStorage
from services import save_xml_data, predict_risk_group_by_owner, PhraseNotFoundInXml

with open('') as file:
    logging.config.dictConfig(json.loads((file.read())))
colorama.init()

def create_app():
    app = Flask(__name__)

    phrase_storage = PhraseStorage('')
    phrase_preprocessor = PhrasePreprocessor(regex=['(ht|f)tp[s]?:\/+[^\s]+', '([^a-zа-я\s])'],
                                             min_max_phrase_len=(1, 6),
                                             min_max_word_len=(2, 11),
                                             stop_pos=['INTJ', 'PRCL', 'CONJ', 'PREP', 'NPRO'])

    @app.route('/')
    def index():
        return 'INDEX'

    @app.route('/s', methods=['GET'])
    def scoring():
        owners = request.args.getlist('owner')
        models_id = [int(model_id) for model_id in request.args.getlist('model')]
        if models_id == []:
            models_id = [1]
        app.logger.info('Start prediction')
        prediction = predict_risk_group_by_owner(owners, models_id, phrase_storage, phrase_preprocessor.normalize)
        return jsonify(prediction)

    @app.route('/l', methods=['GET', 'POST'])
    def loading():
        if request.method != 'POST':
            msg = 'Bad method! Use POST!'
            app.logger.warn(msg)
            return jsonify(status='fail', msg=msg), 405
        xml = request.get_data().decode('utf-8')
        try:
            saved_count = len(save_xml_data(xml, phrase_storage))
            msg = 'Saved {} phrase'.format(saved_count)
            print(colorama.Fore.GREEN, end='')
            app.logger.info(msg)
            print(colorama.Fore.RESET, end='')
            return jsonify(status='good', msg=msg), 200
        except PhraseNotFoundInXml:
            msg = 'Phrase no tfound in xml'
            print(colorama.Fore.YELLOW, end='')
            app.logger.info(msg)
            print(colorama.Fore.RESET, end='')
            return jsonify(status='good', msg=msg), 200
        except (SystemExit, KeyboardInterrupt):
            app.logger.exception()
            raise
        except Exception:
            app.logger.exception(xml)
            return jsonify(status='fail'), 400

    return app


print("       _    _    ________    _   _")
print("       \\ \\ | |  |________|  | | / /")
print("        \\ \\| |   ________   | |/ /")
print("         |   |  |________|  |   |")
print("        / /| |   ________   | |\\ \\")
print("       /_/ |_|  |________|  |_| \\_\\")
print("==========================================")
print("       ::  Product by KEK Data   ::")
print("==========================================")
