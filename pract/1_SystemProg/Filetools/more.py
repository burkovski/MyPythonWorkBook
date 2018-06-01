import sys

def getreply():
    if sys.stdin.isatty():
        return input("?")
    else:
        if sys.platform[:3] == "win":
            import msvcrt
            msvcrt.putch(b"?")
            key = msvcrt.getche()
            msvcrt.putch(b"\n")
            return key.decode()
        else:
            raise SystemExit("platform not supported!")

def more(text, num_lines=10):
    lines = text.splitlines()
    while lines:
        chunk = lines[:num_lines]
        lines = lines[num_lines:]
        for line in chunk:
            print(line)
        if lines and getreply() not in ['y', 'Y']: break


if __name__ == '__main__':
    if len(sys.argv) == 1:
        more(sys.stdin.read())
    else:
        more(open(sys.argv[1]).read())
