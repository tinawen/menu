#!/usr/bin/env python

import os

def main():
    os.chdir("/home/tina/MenuProject/menuproject/scripts")
    os.system("dump_MenuProject_db ../../production.ini")
    os.chdir("../../")

if __name__ == "__main__":
    main()
