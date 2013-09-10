'''
[Narith]
Author: Saad Talaat
Date:    9th September 2013
Brief:    Lightweight Thread Pool implementation
'''
import threading
from Queue import Queue

class TaskPool(object):
    max = 1024
    
    class Work(object):
        def __init__(self, routine, args):
            self.routine = routine
            self.args    = args

    def __init__(self, thread_num):
         self.size 		= thread_num
         self.current_size 	= 0
         self.lock 		= threading.Lock()
         self.non_empty		= threading.Condition(self.lock)
         self.empty		= threading.Condition(self.lock)
         self.threads		= []
         self.works		= Queue()
         self.terminate		= False

         for _ in range(self.size):
             self.threads.append(threading.Thread(target=self.pool_thread))
         for x in self.threads:
             x.start()
    def alive(self):
	return sum(map(lambda x: x.isAlive(), self.threads))

    def kill(self):
        self.terminate = True
        if self.alive():
           self.add_task(self.kill)

    def pool_thread(self):
        while not self.terminate:
            self.lock.acquire()
            while self.current_size == 0:
                self.non_empty.wait()

            wl = self.works.get()
            self.current_size -=1
            if self.current_size == (self.max - 1):
                self.empty.notifyAll()
            
            self.lock.release()
            if wl.args:
                wl.routine(wl.args)
            else:
                wl.routine()
  
            del wl
            
    def add_task(self, task, args=[]):
        self.lock.acquire()
        while self.current_size == self.max:
            self.empty.wait()
        wl = self.Work(task, args)
        self.works.put(wl)
        if self.current_size == 0:
            self.non_empty.notify()
        self.current_size += 1

        self.lock.release()
