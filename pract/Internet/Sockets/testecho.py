import sys
from pract.launchmodes import QuietPortableLauncher

num_clients = 8


def start(cmd_line):
    QuietPortableLauncher(cmd_line, cmd_line)()


start("echo-server.py")

args = ' '.join(sys.argv[1:])

for i in range(num_clients):
    start("echo-client.py {}".format(args))
