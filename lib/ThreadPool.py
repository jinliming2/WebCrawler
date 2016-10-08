#! python3
from queue import Queue
from threading import Thread


class ThreadRunner(Thread):
    def __init__(self, queue, timeout=30, daemon=False):
        super().__init__()
        self.queue = queue
        self.timeout = timeout
        self.setDaemon(daemon)
        self.start()

    def run(self):
        while True:
            try:
                callback, args, kwargs = self.queue.get(timeout=self.timeout)
                callback(args, kwargs)
                self.queue.task_done()
            except self.queue.QueueEmpty:
                break
            except Exception as e:
                print(e)
                raise


class ThreadPool:
    def __init__(self, count=10, timeout=30, daemon=False):
        self.queue = Queue()
        self.threads = []
        self.__create_threads(count, timeout=timeout, daemon=daemon)

    def __create_threads(self, count, timeout=30, daemon=False):
        for i in range(count):
            thread = ThreadRunner(count, timeout=timeout, daemon=daemon)
            self.threads.append(thread)

    def add(self, callback, *args, **kwargs):
        self.queue.put((callback, args, kwargs))

    def join(self):
        while len(self.threads):
            thread = self.threads.pop()
            if thread.isAlive():
                thread.join()
