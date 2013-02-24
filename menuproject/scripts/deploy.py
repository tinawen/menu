#!/usr/bin/env python
 
import os
import signal

def main():
    if os.path.isfile('paster_8080.pid'):
        f = open('paster_8080.pid', 'r')
        if f:
            pid = f.read()
            if pid:
                try:
                    os.kill(int(pid), signal.SIGHUP)
                except:
                    print "process not running"
    os.chdir("./menuproject/scripts/")
    os.system("dump_MenuProject_db ../../production.ini")
    os.chdir("../../")
    os.system("/usr/local/bin/pserve --daemon --pid-file=paster_8080.pid production.ini")

if __name__ == "__main__":
    main()
