import threading
import queue
class LockingQueue(queue.SimpleQueue):
    def __init__(self):
        super().__init__()
        self.empty = threading.Semaphore(10)
        self.full = threading.Semaphore(0)
        self.qLock = threading.Lock()
    def put(self, item):
        self.empty.acquire() 
        self.qLock.acquire() 
        super().put(item) 
        self.qLock.release() 
        self.full.release() 

    def get(self): 
        self.full.acquire() 
        self.qLock.acquire() 

        i=super().get() 
        self.qLock.release() 
        self.empty.release()
        return i