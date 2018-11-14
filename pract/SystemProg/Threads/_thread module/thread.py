# Порождает потоки выполнения, пока не будет нажата клавиша 'q'
import _thread


def child(t_id):
    print("Hello from thread", t_id)


def parent():
    i = 0
    while True:
        i += 1
        _thread.start_new_thread(child, (i, ))
        if input() == 'q': break


parent()
