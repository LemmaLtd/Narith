'''
[Narith]
Author: Saad Talaat
Date:    9th September 2013
Brief:    Lightweight Thread Pool implementation
'''
import threading

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
         self.works		= []

         for _ in range(self.size):
             self.threads.append(threading.Thread(target=self.pool_thread))
         for x in self.threads:
             x.start()

    def pool_thread(self):
        while True:
            self.lock.acquire()
            while self.current_size == 0:
                self.non_empty.wait()

            wl = self.works[0]
            self.current_size -=1
            self.works = self.works[1:]
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
        self.works.append(wl)
        if self.current_size == 0:
            self.non_empty.notify()
        self.current_size += 1

        self.lock.release()
