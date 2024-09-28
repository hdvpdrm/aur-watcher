import sys, tty, termios


def read_single_char(fix_counter):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if str(ch) in "CABD":
            fix_counter = True
        else:
            fix_counter = False
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
