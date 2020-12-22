CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] [%(filename)s - %(funcName)s():%(lineno)s] %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        }, "errors": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": 'ERROR',
            "filename": "text_processing\logger\errors.log",
            "maxBytes": 1024000,
            "backupCount": 20
        }, "text_processing": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": 'INFO',
            "filename": "text_processing/logger/text_processing.log",
            "maxBytes": 1024000,
            "backupCount": 20
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
        'detect_language': {
            'handlers': ['errors','text_processing'],
            'level': 'INFO',
            'propagate': False
        },
        'clean_string': {
            'handlers': ['errors','text_processing'],
            'level': 'INFO',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default', 'errors'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
