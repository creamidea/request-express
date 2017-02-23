#!/usr/local/bin/python
#-*- coding=utf8 -*-

# cdn.bootcss.com/jquery/3.1.1/jquery.min.js
# copy($('table tbody').children().map( function (index, child) { return 'http://' + $(child).children().eq(0).text() + ':' + $(child).children().eq(1).text() } ).toArray())

import os
from threading import Thread
from time import sleep
from queue import Queue
from random import random
from argparse import ArgumentParser

from ProxyList import ProxyList
from Fetch import Fetch
from Writer import Writer

def worker():
    global proxylist, proxy, fetch, writer, q, container

    while True:

        if q.empty():
            break

        item = q.get()
        if item is None or item is '':
            q.task_done()
            continue

        sleep(random())
        print('fetching {item}'.format(item=item))
        package = fetch(item, proxy)

        if package['error_code'] is '0':
            record = package['data']['info']['context'][0]
            last_info = '{item}\t{time}\t{desc}'.format(item=item, time=record['time'], desc=record['desc'])
            container.put(last_info)
        elif package['error_code'] is '3':
            # 订单号不正确
            msg = package['data']['info']['msg']
            last_info = '{item}\t{time}\t{desc}'.format(item=item, time=0, desc=msg)
            container.put(last_info)
        else:
            # 输入验证码
            print(package)
            proxy = proxylist.get()
            q.put(item)

        q.task_done()
        writer(container)

if __name__ == '__main__':

    parser = ArgumentParser(description="Get the information about the express.")
    parser.add_argument('-i', dest="input_filename", required=True,
                        help='input file')
    parser.add_argument('-o', dest="output_filename",
                        default="result.txt",
                        help='output file [default: result.txt]')
    args = parser.parse_args()

    q = Queue()
    container = Queue()

    proxylist = ProxyList()
    proxy = proxylist.get()
    fetch = Fetch()
    writer = Writer(args.output_filename)

    with open (args.input_filename, 'rb') as f:
        nus = f.read()
        [q.put(x.decode('ascii')) for x in nus.split(b'\r\n')]

        for i in range(os.cpu_count()):
            t = Thread(target=worker)
            t.daemon = True
            t.start()
            t.join()

        q.join()
        writer(container, 'done')
        print('>>> ALL DONE')
