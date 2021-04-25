''' создаём многотопотчный клиент
'''

from threading import Thread
import socket
import time


def make_request():
    start_time = time.time()
    # Инициализируем сокет (AF_INET=Address Family INternET)
    # SOCK_STREAM - передача потока с предварительной установкой соединения
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8000))
    sock.send(b'GET /\n\n')
    # блокирующая фунция, которая ждёт, когда в сокете появятся данные
    resp = sock.recv(100) 
    # похожа на yield в генераторах
    sock.close()
    end_time = time.time()
    print(time.strftime('%H:%M:%S'), end_time-start_time)


def do_request_forever():
    while True:
        make_request()

t1 = Thread(target=do_request_forever)
t2 = Thread(target=do_request_forever)

t1.start()
t2.start()
