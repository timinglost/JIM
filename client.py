from socket import socket, AF_INET, SOCK_STREAM
import time, sys
from utils import *


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
                print('Порт должен быть указан в пределах от 1024 до 65535')
                sys.exit(1)
        s = socket(AF_INET, SOCK_STREAM)
        try:
                print(address, type(port))
                s.connect((address, port))
                massage = create_massege(config)
                post_data(s, massage, config)
                answer = get_data(s, config)
                s.close()
                print(response_treatment(answer, config))
        except ConnectionRefusedError:
                print('400: Bad Request')


if __name__ == '__main__':
    main()
