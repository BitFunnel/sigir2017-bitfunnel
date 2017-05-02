# from bf_utilities import run
#
# run("dir", r"d:\temp");


import time
from threading import Thread

class Foobar:
    def __init__(self):
        self.foo = "xyz"

    def sleeper(self, i):
        print("thread %d sleeps for 2 seconds" % i)
        print(self.foo)
        time.sleep(2)
        print("thread %d woke up" % i)

    def start(self):
        for i in range(10):
            t = Thread(target=self.sleeper, args = (i, ))
            t.start()

x = Foobar()
print(x.foo)
#x.sleeper()
x.start()
