'''создаём однопоточный запрос'''

import socket
import time


def make_request():
    start_time = time.time()
    # Инициализируем сокет (AF_INET=Address Family INternET)
    # SOCK_STREAM - передача потока с предварительной установкой соединения
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8000))
    sock.send(b'GET /\n\n')
    # recv долго ждёт ответа, тормозит запросы
    resp = sock.recv(100)
    sock.close()
    end_time = time.time()
    print(end_time-start_time)


while True:
    make_request()
