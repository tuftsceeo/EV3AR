import signal,sys,termios,tty

def getch2():
    fd = sys.stdin.fileno()
    print("start")
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    try:
        while True:
            ch = sys.stdin.read(1)
            if not ch or ch == chr(4):
                break
            print('%02x'%ord(ch)),
    except (KeyboardInterrupt, EOFError):
        pass
#    if ch != "None":
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

while True:
    char = getch2()
    print(start)
    print(char)
    if char == 'q':
        exit()