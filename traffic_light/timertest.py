import threading
import time

global a
a= 0





              time.sleep(1)

    def turnoff(self):
        global a
        a=0

    def test(self):
        global t
        t=threading.Timer(10, self.turnoff)

        a=1
        print ('a=%d' % a)
        t.start()
        while a!=0:
            print ('a=%d' % a)
            time.sleep(1)
