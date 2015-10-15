#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lhcpig'

import urllib.parse
import urllib.request
import json

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Host": "account.bilibili.com",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://account.bilibili.com/answer/promotion",
    "Cookie": "DedeUserID=15918638; SESSDATA=9e675993%2C1476433710%2Ce2a48dbd",
    "Connection": "keep-alive"
}


def send_request(qs_ids):
    url = "https://account.bilibili.com/answer/goPromotion"
    param = dict()
    param['qs_ids'] = ','.join(qs_ids.keys())
    for k, v in qs_ids.items():
        param['ans_hash_' + k] = v
    req = urllib.request.Request(url, urllib.parse.urlencode(param).encode('utf-8'), header)
    r = urllib.request.urlopen(req)
    return_str = r.read().decode('utf-8')
    return json.loads(return_str)

qs_ids={'324':"hhhh",'3453453':"hhhhxx"}
param = dict()
param['qs_ids'] = ','.join(qs_ids.keys())
for k, v in qs_ids.items():
    param['ans_hash_' + k] = v
print(param)
