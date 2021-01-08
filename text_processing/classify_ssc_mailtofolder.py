from logging.config import dictConfig
from logger import CONFIG
import pandas as pd
import logging
import json
import sys
import re
import os

dictConfig(CONFIG)
logger = logging.getLogger('detect_language')

text = sys.argv[1]
text_language = sys.argv[2]


def clean_string(text):
    try:
        import string
        import re
        text = text.lower()
        text = ''.join([word for word in text if word not in string.punctuation])
        text = re.sub('[\n]', ' ', text)
        text = re.sub('[\r]', ' ', text)
        text = re.sub(' {2,}', ' ', text)
        text = text.strip()
    except Exception as e:
        logger.error(e)
    return text


def clean_string_stopwords(language, text):
    from nltk.corpus import stopwords
    stop_words = set_stopwords(language)
    text = clean_string(text)
    if language is not None:
        if language == 'de':
            set(stopwords.words("german"))
            logger.debug('Set stopwords to "german"')
            text = ' '.join([word for word in text.split() if word not in stop_words])
        elif language == 'en':
            set(stopwords.words("english"))
            logger.debug('Set stopwords to "english"')
            text = ' '.join([word for word in text.split() if word not in stop_words])
        else:
            logger.warning('Undefined stopwords language: ' + str(language))
    else:
        logger.warning('No language defined')

    return text


def clean_string_german(text):
    import unicodedata
    if isinstance(text, list):
        cleaned_list = []
        for item in text:
            cleaned_list.append(unicodedata.normalize('NFKD', item).encode('ASCII', 'ignore').decode("utf-8"))
        return cleaned_list
    else:
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode("utf-8")


def set_stopwords(language_iso2):
    from nltk.corpus import stopwords
    if language_iso2 is not None:
        if language_iso2 == 'de':
            return stopwords.words("german")
            logger.debug('Set stopwords to "german"')
        elif language_iso2 == 'en':
            return stopwords.words("english")
            logger.debug('Set stopwords to "german"')
        else:
            logger.warning('Undefined stepwords language: ' + str(language_iso2))
    else:
        logger.warning('No language detected')


def split_address(str_address):
    sentences = []
    parser_address_name = 'gmbh'
    address_name = str_address[
                   :str_address.find(parser_address_name) + len(parser_address_name)].strip()
    address = str_address[
              str_address.find(parser_address_name) + len(parser_address_name):].strip()
    street = split_street(address)
    city = split_pc_city(address)
    sentences.append(address_name)
    sentences.append(street)
    try:
        sentences.append(city.split(' ', 1)[0])
        sentences.append(city.split(' ', 1)[1])
    except:
        logging.error('Split city address failed for: ' + city)
        sentences.append(city)
    sentences = clean_string_german(sentences)
    logger.info(sentences)
    return sentences


def split_street(address):
    switcher = {
        1: re.split('(\d{4})', address, 1)[0],
        3: re.split('(\d{5})', address, 1)[0]
    }
    return switcher.get(len(re.split('(\d{5})', address, 1))).strip()


def split_pc_city(address):
    if len(re.split('(\d{5})', address, 1)) == 1:
        return str(re.split('(\d{4})', address, 1)[1] + re.split('(\d{4})', address, 1)[2])
    elif len(re.split('(\d{5})', address, 1)) == 3:
        return str(re.split('(\d{5})', address, 1)[1] + re.split('(\d{5})', address, 1)[2])
    else:
        return None


try:
    ref_list = pd.read_excel(io='text_processing/data/address_folders.xlsx', header=0, engine='openpyxl')
except Exception as e:
    ref_list = None
    logger.error("Parsing json_ref_list failed" + str(e))
if text is not None:
    if text_language is not None:
        logger.debug('Input_string: ' + text)
        logger.debug('Input_string_language: ' + text_language)

        if ref_list.empty == False:
            max_match = 0;
            folder_names=[]
            classified_folders = []
            cleaned_input = clean_string_german(clean_string_stopwords(text_language, text))
            logger.debug('Cleaned_input_string: ' + text)

            for index, row in ref_list.iterrows():
                found_senteces = 0;
                cleaned_reference = clean_string_german(clean_string(row['ADDRESS']))
                sentences = split_address(cleaned_reference)
                logger.debug('sentences: ' + str(sentences) + '}')

                for sentence in sentences:
                    if sentence in cleaned_input:
                        found_senteces += 1;
                if found_senteces >= max_match and found_senteces > 1:
                    if row['FOLDER_NAME'] in folder_names:
                        continue
                    else:
                        new_row = {'folder': row['FOLDER_NAME'], 'folder_test': row['FOLDER_NAME_TEST'], 'address': clean_string_german(row['ADDRESS']),
                                  'matching': found_senteces / len(sentences)}
                        folder_names.append(row['FOLDER_NAME'])
                        classified_folders.append(new_row)

            classified_folders = sorted(classified_folders, key=lambda i: i['matching'], reverse=True)
            logger.info('classified_folders: ' + str(classified_folders) + '}')
            json_rep = json.dumps(classified_folders, indent=2)

            print('{ "classified_folders" : ' + str(json_rep) + '\n}')
        else:
            print('Reference text not defined')
    else:
        print('No input_text_language defined')
else:
    print('No input_text defined')
