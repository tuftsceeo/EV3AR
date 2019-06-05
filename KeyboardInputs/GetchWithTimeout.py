import signal,sys,termios,tty
 
class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass
    def __init__(self, sec):
        self.sec = sec
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
    def raise_timeout(self, *args):
        raise Timeout.Timeout()

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        with Timeout(1):
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
    except Timeout.Timeout:
        print("Timeout")
        ch=''
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    print(ch)
    return ch

while True:
    char = getch()
    print(char)
    if char == 'q':
        exit()
