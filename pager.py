#!/usr/bin/env python3
import sys
import keyboard
import os
import signal

def handler(signum, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, handler)


inp = sys.stdin.read().split("-"*40)
if len(inp) == 1 and inp[0] == "nothing was found...\n":
    print(inp[0])
    sys.exit(0)

current = 1
total   = len(inp)

os.system("clear")
print("{}/{}".format(current,total))
print(inp[current])
r_pressed = l_pressed = False
while True:
    if keyboard.is_pressed('q'):
        sys.exit(0)
    elif keyboard.is_pressed('right') and not r_pressed:
        if current + 1 >= total:
            current = 1
        else:
            current+= 1
        os.system("clear")
        print("{}/{}".format(current,total))
        print(inp[current])
        r_pressed = True
    elif keyboard.is_pressed('left') and not l_pressed:
        if current - 1 <= 0:
            current = total-1
        else:
            current-= 1
        os.system("clear")
        print("{}/{}".format(current,total))
        print(inp[current])
        l_pressed = True

    if not keyboard.is_pressed("left"):
        l_pressed = False
    if not keyboard.is_pressed("right"):
        r_pressed = False
        
