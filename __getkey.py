import termios
import sys

def getch() -> str:
  fd = sys.stdin.fileno()
  term = termios.tcgetattr(fd)
  term[3] &= ~(termios.ICANON | termios.ECHO | termios.IGNBRK | termios.BRKINT)
  termios.tcsetattr(fd, termios.TCSAFLUSH, term)
  return sys.stdin.read(1)

def getkey() -> str:
  c1 = getch()
  if c1 != "\x1B":
    return c1

  c2 = getch()
  if c2 not in "\x4F\x5B":
    return c1 + c2

  c3 = getch()
  if c3 not in "\x31\x32\x33\x35\x36":
    return c1 + c2 + c3

  c4 = getch()
  if c4 not in "\x30\x31\x33\x34\x35\x37\x38\x39":
    return c1 + c2 + c3 + c4

  c5 = getch()
  return c1 + c2 + c3 + c4 + c5