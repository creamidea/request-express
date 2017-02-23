#!/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

def Fetch ():
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    root_url = 'https://sp0.baidu.com/9_Q4sjW91Qh3otqbppnN2DJv/pae/channel/data/asyncqury'
    payload = {
        'cb':'jQueryXBaidu',
        'appid': 4001,
        'com':'yunda',
        'nu': '',
    }
    cookies = dict(
        BAIDUID='7CA49FEAEE0E4CC48282DEE42E336B14:FG=1'
    )

    def request(nu, proxy = ''):
        payload['nu'] = nu
        proxies = {
            "http": proxy,
        }
        resp = requests.get(root_url,
                            headers = headers,
                            params = payload,
                            cookies = cookies,
                            proxies = proxies)
        return json.loads(resp.text[5+len(payload['cb']): -1])

    return request
