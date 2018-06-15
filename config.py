# -*- coding: utf-8 -*-
import time

goRegister = False


def log(**kwargs):
    try:
        log.logs += 1
        print("IN LOG!!!")
    except AttributeError:
        log.logs = 0
    res = '-----------------------------------------------------------\n'
    res += 'Log#' + str(log.logs) + ' at ' + str(time.asctime(time.localtime(time.time()))) + '\n'
    for i in range(len(kwargs)):
        ln = list(kwargs.popitem())
        res += str(ln[0]) + " : " + str(ln[1]) + '\n'
    print(res)
