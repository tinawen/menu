#!/usr/bin/env python
 
import os
import signal

def main():
    f = open('paster_8080.pid', 'r')
    if f:
        pid = f.read()
        os.kill(int(pid), signal.SIGHUP)
    os.system("cd menuproject/scripts/")
    os.system("dump_MenuProject_db production.ini")
    os.system("cd ../../")
    os.system("/usr/local/bin/pserve --daemon --pid-file=paster_8080.pid production.ini")

if __name__ == "__main__":
    main()
