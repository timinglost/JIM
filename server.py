from socket import socket, AF_INET, SOCK_STREAM
import time, json, sys, logging, log.server_log_config
from utils import *
from functools import wraps
import inspect


class Log:
    def __init__(self):
        pass

    def __call__(self, func):
        @wraps(func)
        def call(*args, **kwargs):
            server_log_use = logging.getLogger('server_log_config_use')
            server_log_use.setLevel(logging.INFO)

            my_file_handler_use = logging.FileHandler('log/server.log')
            client_formatter_use = logging.Formatter("%(asctime)s - %(message)s ")
            my_file_handler_use.setFormatter(client_formatter_use)
            my_file_handler_use.setLevel(logging.INFO)
            server_log_use.addHandler(my_file_handler_use)
            previous_func = inspect.stack()[1][3]
            server_log_use.info(f'Функция {func.__name__} вызвана из функции {previous_func}')
            return func(*args, **kwargs)

        return call


@Log()
def massege_treatment(massage, config):
    if config['ACTION'] in massage \
            and massage[config['ACTION']] == config['PRESENCE'] \
            and config['TIME'] in massage \
            and config['USER'] in massage \
            and massage[config['USER']][config['ACCOUNT_NAME']] == 'Ivan':
        return {"response": '200',
                "time": time.time(),
                "alert": "успешное завершение"}
    server_log.info('400: Неверные данные')
    return {"response": '400',
            "time": time.time(),
            "alert": "Неверные данные"}


def main():
    config = load_config()
    try:
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = config['DEFAULT_PORT']
        if not 65535 >= port >= 1024:
            raise ValueError
    except IndexError:
        server_log.warning('После -\'p\' необходимо указать порт')
        sys.exit(1)
    except ValueError:
        server_log.warning('Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            address = sys.argv[sys.argv.index('-a') + 1]
        else:
            address = ''

    except IndexError:
        server_log.warning('После \'a\'- необходимо указать адрес для ')
        sys.exit(1)
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((address, port))
    s.listen(config['MAX_CONNECTIONS'])

    while True:
        client, addr = s.accept()
        client_data = get_data(client, config)
        answer = massege_treatment(client_data, config)
        post_data(client, answer, config)
        client.close()


if __name__ == '__main__':
    server_log = logging.getLogger('server_log_config')
    main()
