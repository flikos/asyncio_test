''' добавляем очередь сокетов в deque
где будем отслеживать их готовность и 
работать только с готовыми
'''

from threading import Thread
import socket
import time


from collections import deque
from select import select


tasks = deque()
stopped = {}


def run_queries():
    while any([tasks, stopped]):
        # наполнение списка задач теми корутинами, которые готовы дальше работать
        while not tasks:
            # проверяем селектом какие сокеты уже готовы отдавать (принимать) данные
            ready_to_read, _write_sockets, _error_sockets = select(stopped, [], [])
            for r in ready_to_read:
                tasks.append(stopped.pop(r))
        # выполнение задач
        while tasks:
            task = tasks.popleft()
            try:
                sock = next(task)
                stopped[sock] = task
            except StopIteration:
                print('query done')


def make_request():
    start_time = time.time()
    # Инициализируем сокет (AF_INET=Address Family INternET)
    # SOCK_STREAM - передача потока с предварительной установкой соединения
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('0.0.0.0', 8000))
    print('send')
    sock.send(b'GET /\n\n')
    
    print('yield')
    # раз ожидание, попробуем добавить yield и создать генератор
    yield sock 
    
    print('recv')
    # блокирующая фунция, которая ждёт, когда в сокете появятся данные
    resp = sock.recv(100)

    print('close')
    sock.close()
    end_time = time.time()
    print(time.strftime('%H:%M:%S'), end_time-start_time)


tasks.append(make_request())
run_queries()
