import Tkinter
import threading
from Queue import Queue
from time import sleep

main = ''

def modify_var():
    sleep(5)
    queue.put(1)

def update_txt(event = None):
    print "hei"
    if  queue.not_empty :
        a = queue.get()
        print a
    main.after(5000,update_txt)



main = Tkinter.Tk()
txt = Tkinter.Text(main)
txt.grid()

main.after(5000,update_txt)
th = threading.Thread(group=None, target=modify_var, args=(), kwargs={})
th.start()
queue = Queue()
main.mainloop()