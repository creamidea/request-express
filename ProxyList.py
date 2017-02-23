#!/bin/env python
# -*- coding: utf-8 -*-

import os

class ProxyList(object):

    __idx = 0

    def __init__(self, filename='proxies.txt'):
        with open(filename, 'rb') as f:
            proxies = f.read()
            self.__proxies = ([x.decode('ascii') for x in proxies.split(os.linesep.encode('ascii')) if x is not None])

    def get(self):

        try:
            proxy = self.__proxies[self.__idx]
        except KeyError:
            self.__idx = 0
            proxy = self.__proxies[self.__idx]

        self.__idx += 1
        return proxy
