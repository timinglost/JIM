from socket import socket, AF_INET, SOCK_STREAM
import time, json, sys
from utils import *


def massege_treatment(massage, config):
    if config['ACTION'] in massage \
            and massage[config['ACTION']] == config['PRESENCE'] \
            and config['TIME'] in massage \
            and config['USER'] in massage \
            and massage[config['USER']][config['ACCOUNT_NAME']] == 'Ivan':
        return {"response": '200',
                "time": time.time(),
                "alert": "успешное завершение"}
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
        print('После -\'p\' необходимо указать порт')
        sys.exit(1)
    except ValueError:
        print(
            'Порт должен быть указан в пределах от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            address = sys.argv[sys.argv.index('-a') + 1]
        else:
            address = ''

    except IndexError:
        print(
            'После \'a\'- необходимо указать адрес для ')
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
    main()
