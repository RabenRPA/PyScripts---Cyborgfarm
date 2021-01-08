from logging.config import dictConfig
from logger import CONFIG
import logging
import string
import sys
import re

dictConfig(CONFIG)
logger = logging.getLogger('clean_string')

text = str(sys.argv[1].encode('utf8'))

try:
    text = text.lower()
    text = ''.join([word for word in text if word not in string.punctuation])
    text = re.sub('[\n]', ' ', text)
    text = re.sub('[\r]', ' ', text)
    text = re.sub('[\r\n]', ' ', text)
    text = re.sub('[\n\r]', ' ', text)
    text = re.sub(' {2,}', ' ', text)
    text = text.strip()
    print(text)
except Exception as e:
    logger.error(str(e))