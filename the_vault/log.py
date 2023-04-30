import logging
import os

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if os.environ['ENV'] == 'development' else logging.INFO)

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handlers
    log_file = os.path.join(os.environ['APP_HOME'], 'logs', 'app.log')
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    error_file = os.path.join(os.environ['APP_HOME'], 'logs', 'error.log')
    error_handler = logging.FileHandler(error_file, mode='w')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    return logger
