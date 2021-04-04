#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import threading
import time


def foo(n):
    print("args is %s" %(n))
    x = 0
    while x < 10:
        print("child thread running", x)
        time.sleep(1)
        x += 1


def fun():
    print("other child thread is runing")


if __name__ == '__main__':
    # 启动一个线程,这里又参数
    t1 = threading.Thread(target=foo, args=(1,), name="thread-0")
    t1.start()
    t1.join()
    print("main thread continue run")

    # 启动一个线程，这里没有参数
    t2 = threading.Thread(target=fun,name="thread-1")
    t2.start()
    t2.join()
    print("main thread continue run")


