from socket import socket, AF_INET, SOCK_STREAM
import time, sys, logging
from utils import *
import log.client_log_config


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
                s.close()
                client_log.info('Подключение закрыто')
                print(response_treatment(answer, config))
        except ConnectionRefusedError:
                client_log.error('400: Bad Request')


if __name__ == '__main__':
        main()
