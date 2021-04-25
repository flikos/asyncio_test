''' добавляем очередь сокетов в deque
где будем отслеживать их готовность и 
работать только с готовыми
'''

from threading import Thread
import socket
import time


from collections import deque
from select import select

class Even_loop:
    def __init__(self):
        self.tasks = deque()
        self.stopped = {}

    def add_task(self, task):
        self.tasks.append(task)

    def add_future(self, future):
        self.tasks.append(future_monitor())

    def run_forever(self):
        while any([self.tasks, self.stopped]):
            # наполнение списка задач теми корутинами, которые готовы дальше работать
            while not self.tasks:
                # проверяем селектом какие сокеты уже готовы отдавать (принимать) данные
                # оказывается select тоже блокирующая
                ready_to_read, _write_sockets, _error_sockets = select(self.stopped.keys(), [], [], 1.0)
                for r in ready_to_read:
                    self.tasks.append(self.stopped.pop(r))
            # выполнение задач
            while self.tasks:
                task = self.tasks.popleft()
                try:
                    sock = next(task)
                    self.stopped[sock] = task
                except StopIteration:
                    print('query done')


# класс, расширяющий функционал сокета
class AsyncSocket(socket.socket):
    # генератор: йелдит себя и потом себя из себя читает
    def AsyncRead(self, capacity=100)
        yield self
        return self.recv(100)


class Future:
    def __init__(self, done_callback):
        self.notify, self.event = socket.pair()
        self.done_callback = done_callback
        self.result = None

    def set_done(self, result):
        self.result = result
        self.


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


def run_request_producer():
    while True:
        time.sleep(1.0)
        future_done()

# служебный вызов, создающий 2 сокета: для записи, второй для чтения
future_notify, future_event = socket.socketpair()


def future_done():
    tasks.append(make_request())
    future_notify.send(b'done')


def future_monitor():
    while True:
        yield future_event
        future_event.recv(100)


tasks.append(future_monitor())
t = Thread(target=run_request_producer)
t.start()
