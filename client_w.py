from socket import socket, AF_INET, SOCK_STREAM
import time, sys, logging
from utils import *
import log.client_log_config
from functools import wraps
import inspect


def log(func):
        @wraps(func)
        def call(*args, **kwargs):
                client_log_use = logging.getLogger('client_log_config_use')
                client_log_use.setLevel(logging.INFO)

                my_file_handler_use = logging.FileHandler('log/client.log')
                client_formatter_use = logging.Formatter("%(asctime)s - %(message)s ")
                my_file_handler_use.setFormatter(client_formatter_use)
                my_file_handler_use.setLevel(logging.INFO)
                client_log_use.addHandler(my_file_handler_use)
                previous_func = inspect.stack()[1][3]
                client_log_use.info(f'Функция {func.__name__} вызвана из функции {previous_func}')
                return func(*args, **kwargs)
        return call

@log
def create_massege(config):
        return {
                "action": config['PRESENCE'],
                "time": time.time(),
                "type": "status",
                "user": {
                        "account_name":  'Ivan',
                        "status":      "Yep, I am here!"
                }
        }


@log
def response_treatment(answer, config):
        if config['RESPONSE'] in answer:
                return f'"response": {answer["response"]}\n"time": {answer["time"]}\n"alert": {answer["alert"]}'


def main():
        client_log = logging.getLogger('client_log_config')
        config = load_config()
        try:
                address = sys.argv[1]
                port = int(sys.argv[2])
                if not 65535 >= port >= 1024:
                        raise ValueError
        except IndexError:
                address = config['DEFAULT_IP_ADDRESS']
                port = config['DEFAULT_PORT']
        except ValueError:
                client_log.warning('Порт должен быть указан в пределах от 1024 до 65535')
                sys.exit(1)
        s = socket(AF_INET, SOCK_STREAM)
        try:
                s.connect((address, port))
                client_log.info('Установленно подключение')
                massage = create_massege(config)
                post_data(s, massage, config)
                answer = get_data(s, config)
                print(response_treatment(answer, config))
                while True:
                    answer_get = get_data(s, config)
                    if answer_get != '':
                        print(answer_get)
                s.close()
                client_log.info('Подключение закрыто')
        except ConnectionRefusedError:
                client_log.error('400: Bad Request')


if __name__ == '__main__':
        main()