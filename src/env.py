import os
from dotenv import load_dotenv


class EnvParameter:
    """ Получение переменных окружения """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """ создать синглтон """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        """ Загрузить переменные окружения из файла """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.split(current_dir)[0]
        filepath = os.path.join(root_dir, '.env')
        if os.path.exists(filepath):
            load_dotenv(filepath)

    @staticmethod
    def api_key(key_name=''):
        """ Получить переменную окружения """
        return os.getenv(key_name)

    @staticmethod
    def db_key():
        """ Получить переменные окружения базы """
        return {
            'host': 'localhost',
            'database': 'sky',
            'user': os.getenv('USER'),
            'password': os.getenv('PASSWORD')}
