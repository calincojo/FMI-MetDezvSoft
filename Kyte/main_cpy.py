import Tkinter
import threading
from Queue import Queue
from time import sleep


queue = Queue()

def modify_var():
    sleep(5)
    queue.put(1)

def update_txt(event = None):
    print "hei"
    if queue.empty():
        main.after(2000,update_txt)
    else:
        a= queue.get()
        print a




th = threading.Thread(group=None, target=modify_var, args=(), kwargs={})
th.start()

main = Tkinter.Tk()
txt = Tkinter.Text(main)
txt.grid()

main.after(2000,update_txt)

main.mainloop()