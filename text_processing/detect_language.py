from langdetect import detect_langs, DetectorFactory
from classes import Language, LanguageEncoder
from logging.config import dictConfig
from logger import CONFIG
import logging
import json
import sys

DetectorFactory.seed = 0
text = sys.argv[1]
languages = []
response = str(languages)

dictConfig(CONFIG)
logger = logging.getLogger('detect_language')

if text.strip():
    try:
        detected_languages = detect_langs(text)
        logger.error('test')
        if detected_languages:
            for language in detected_languages:
                detected_language = Language(iso2=str(language).split(':')[0],
                                             language_prob=float(str(language).split(':')[1]))
                languages.append(detected_language)
            languages.sort(key=lambda x: x.language_prob, reverse=True)
            result_text = json.dumps(languages, cls=LanguageEncoder)
            response = json.loads(result_text)
            logger.info(response)
            print(response)
    except Exception as e:
        print(str(e))
