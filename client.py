from socket import socket, AF_INET, SOCK_STREAM
import time, json

name = input('Input your name: ')
s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 8888))

massage = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
                "account_name":  name,
                "status":      "Yep, I am here!"
        }
}
s.send(json.dumps(massage).encode('utf-8'))
answer = json.loads(s.recv(1000000).decode("utf-8"))
s.close()
print(f'"response": {answer["response"]}\n"time": {answer["time"]}\n"alert": {answer["alert"]}')
