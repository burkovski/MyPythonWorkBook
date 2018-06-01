import sys
import random
from math import ceil


replicas_num = 2
shards_num = 15


class Manager:
    def not_empty(self, dictionary):
        return filter(lambda key: dictionary[key] > 0, dictionary)

    def get_shards(self, *, count, rand=None):
        not_empty = list(self.not_empty(self.shards))
        if rand: random.shuffle(not_empty)
        res = set()
        for x in not_empty[:count]:
            res.add(x)
            self.shards[x] -= 1
        return res

    def random(self):
        res = self.get_shards(count=self.shards_on_server, rand=True)
        shards_len = len(res)
        if shards_len < self.shards_on_server:
            res.update(
                self.get_shards(count=(self.shards_on_server - shards_len))
            )
        return res

    def mirror(self):
        count = self.shards_on_server
        if self.shards_on_server % 2 != 0:
            count -= 1
        return self.get_shards(count=count)

    def kill_server(self):
        killed = random.choice(self.servers)
        self.servers.remove(killed)
        count = 0
        for serv in self.servers:
            for shard in killed.data:
                if shard in serv.data:
                    count += 1
                    break
        template = "Killing 2 arbitrary servers results in data loss in {0:.2%} cases"
        print(template.format(count / (self.servers_num - 1)))


class Server:
    def __init__(self, data):
        self.data = data


class DataBase(Manager):
    def __init__(self, servers_num, mode_key):
        self.servers_num = servers_num
        self.shards = {i: replicas_num for i in range(1, shards_num + 1)}
        self.shards_on_server = ceil((shards_num * 2) / servers_num)
        self.servers = [Server(modes[mode_key](self))
                        for _ in range(servers_num)]


def get_args():
    try:
        n, servers_num, mode_key = sys.argv[1:]
    except ValueError as exc:
        print(str(exc).capitalize())
    else:
        if servers_num.isdigit():
            if mode_key in modes:
                return n, int(servers_num), mode_key
            else:
                print("Unknown placement mode: <{0}>\nAllowed modes:".format(
                    mode_key), modes)
        else:
            print("Second arg must be <int>, not <{0}>".format(
                servers_num.__class__.__name__))
    exit(-1)


modes = {
    '--random': Manager.random,
    '--mirror': Manager.mirror,
}

if __name__ == '__main__':
    n, servers_num, mode_key = get_args()
    db = DataBase(servers_num, mode_key)
    db.kill_server()
