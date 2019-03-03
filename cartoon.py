import time


states = ["-", "\\", "|", "/"]
i = 0
while True:
    print("{}\r".format(states[i % 4]), end='')
    i += 1
    time.sleep(0.1)
