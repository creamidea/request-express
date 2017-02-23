#!/bin/env python
# -*- coding: utf-8 -*-

import os

def Writer (filename = 'result.txt', limit=10):

    f = open(filename, 'a')
    print('The result will be stored in [{filename}]'.format(filename=filename))
    count = [0] # int 无法被下面函数读取，python3可以用 nonlocal

    # @param {Queue} container store the results
    # @param {string} state doing/done
    def _write(container, state='doing'):

        if container.qsize() is limit or state is 'done':
            result = []

            if state is 'done':
                _range = range(container.qsize())
            else:
                _range = range(limit)

            for i in _range:
                result.append(container.get())

            f.write(os.linesep.join(result) + os.linesep)
            count[0] += 1
            print('>>> #{count} DONE.'.format(count=count[0]))

        if state is 'done':
            f.close()
            print('>>> The file [{filename}] is closed.'.format(filename=filename))

    return _write
