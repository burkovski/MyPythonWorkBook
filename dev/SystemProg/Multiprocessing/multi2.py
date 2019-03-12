"""
Реализует взаимодействие с помощью анонимных каналов из пакета multiprocessing.
Возвращаемые 2 объекта Connection представляют концы канала: объекты передаются
в один конец и принимаются из другого конца, хотя каналы по умолчанию являются
двунаправленными
"""

from multiprocessing import Process, Pipe


def sender(pipe):
    """
    передает объект родителю через анонимный канал
    """
    pipe.send(['spam'] + [42, 'eggs'])
    pipe.close()


def talker(pipe):
    """
    передает и принимает объекты из канала
    """
    pipe.send(dict(name="Bob", spam=42))
    reply = pipe.recv()
    print("talker got:", reply)


if __name__ == '__main__':
    parent_end, child_end = Pipe()
    Process(target=sender, args=(child_end, )).start()      # породить потомка с каналом
    print("parent got:", parent_end.recv())                 # принять от потомка
    parent_end.close()                                      # или может быть закрыт автоматически сборщиком мусора

    parent_end, child_end = Pipe()
    child = Process(target=talker, args=(child_end, ))
    child.start()
    print("parent got:", parent_end.recv())                 # принять от потомка
    parent_end.send({x * 2 for x in "spam"})                # передать потомку
    child.join()                                            # ждать завершения потомка
    print("Parent exit")