import signal,sys,termios,tty

def getch2():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

while True:
    print("start")
    char = getch2()
    print(char)
    if char == 'q':
        exit()