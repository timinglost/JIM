from socket import socket, AF_INET, SOCK_STREAM
import time, json

s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 8888))
s.listen(5)

while True:
    client, addr = s.accept()
    client_data = json.loads(client.recv(1000000).decode("utf-8"))
    if client_data['action'] == 'presence':
        answer = {"response": '200',
                  "time": time.time(),
                  "alert": "успешное завершение"}
        client.send(json.dumps(answer).encode('utf-8'))
    client.close()
