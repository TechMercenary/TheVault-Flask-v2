from cryptography.fernet import Fernet
from . import logger

import os
import json


os.environ['LOCAL_SETTINGS_FILE'] = os.path.join(os.environ['APP_HOME'], 'local_settings.json')
os.environ['FERNET_KEY_FILE'] = os.path.join(os.environ['APP_HOME'], 'fernet_key.txt')

def _check_env():
    try:
        assert os.environ['ENV'] in ['development', 'production'], f"Invalid environment: {os.environ['ENV']}"
    except AssertionError as e:
        logger.exception(e)
        exit(1)


def _check_fernet_key_file() -> None:
    try:
        assert os.path.exists(os.environ['FERNET_KEY_FILE']), f"Fernet key file not found in {os.environ['FERNET_KEY_FILE']}"
    except AssertionError as e:
        logger.exception(e)
        exit(1)
        
    with open(os.environ['FERNET_KEY_FILE'], 'r') as f:
        os.environ['FERNET_KEY'] = f.read().strip()


def _load_local_settings() -> None:
    # ensure local settings file exists
    if not os.path.exists(os.environ['LOCAL_SETTINGS_FILE']):
        with open(os.environ['LOCAL_SETTINGS_FILE'], 'w') as f:
            f.write(json.dumps({
                'SERVER_NAME': 'localhost:5000',
                'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@localhost:5432/postgres',
                'DB_SCHEMA': 'app',
                'ENV': 'development',
                'DEFAULT_COUNTRY': 'AR',
                'UI_TIMEZONE': 'America/Argentina/Buenos_Aires',
                'DEFAULT_CURRENCY': 'ARS',
                'FILES_ROOT_DIR': 'P:\\TheVault',
            }))
    
    # load local settings
    with open(os.environ['LOCAL_SETTINGS_FILE']) as f:
        local_settings = json.load(f)
        
    # set local settings as environment variables
    for key in local_settings:
        os.environ[key] = local_settings[key]


def _load_global_settings():
    
    os.environ['GLOBAL_SETTINGS_FILE'] = os.path.join(os.environ['FILES_ROOT_DIR'], 'config', 'global_settings.json')
    
    # ensure global settings file exists
    os.makedirs(os.path.dirname(os.environ['GLOBAL_SETTINGS_FILE']), exist_ok=True)
    
    fernet = Fernet(os.environ['FERNET_KEY'].encode())
    
    if not os.path.exists(os.environ['GLOBAL_SETTINGS_FILE']):
        secrets = {
            'FERNET_KEY': os.environ['FERNET_KEY'],
        }
        json_data = json.dumps(secrets)
        encrypted_data = fernet.encrypt(json_data.encode())

        with open(os.environ['GLOBAL_SETTINGS_FILE'], 'wb') as f:
            f.write(encrypted_data)
 
    # load global settings
    with open(os.environ['GLOBAL_SETTINGS_FILE'], 'rb') as f:
        encrypted_data = f.read()
    
    json_data = fernet.decrypt(encrypted_data).decode()
    secrets = json.loads(json_data)
    
    # set global settings as environment variables
    for key in secrets:
        os.environ[key] = secrets[key]
        

def load_settings():
    _check_env()
    _check_fernet_key_file()
    _load_local_settings()
    _load_global_settings()

        