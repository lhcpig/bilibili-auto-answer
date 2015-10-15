#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'lhcpig'

import urllib.parse
import urllib.request
import json

dede_user_id=""
sess_data=""
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Host": "account.bilibili.com",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "https://account.bilibili.com/answer/promotion",
    "Cookie": "DedeUserID="+dede_user_id+"; SESSDATA="+sess_data,
    "Connection": "keep-alive"
}


def auto_answer():
    url = "https://account.bilibili.com/answer/getQstByType"
    param = urllib.parse.urlencode({
        "qs_ids": "36625,43659,43669,43682,43683,43685,43695,43696,43698,43699,43703,43708,43709,43714,43728,43729,43731,43732,43738,43752",
        "ans_hash_36625": "f0a134c490416c5c47dfe0f431d458e1",
        "ans_hash_43659": "731d1b922e90ce81a4cebfd06f5e351b",
        "ans_hash_43669": "ac0ec70b99578f4019ab29da3864094c",
        "ans_hash_43682": "0c4759b4f52f2028b257f54466b0ff4f",
        "ans_hash_43683": "1a324ffd222ca9cee0ce3d414815645a",
        "ans_hash_43685": "a9e420659261a5650535bb8c33d00f0c",
        "ans_hash_43695": "ca668f1a51f46d6186963fcad6f11e58",
        "ans_hash_43696": "93908f54b8e594c229790dd840034e53",
        "ans_hash_43698": "58e2c613d81b6d4ab1d987d1345485fb",
        "ans_hash_43699": "6c3264cf3950d1512e35f1d95d2870e4",
        "ans_hash_43703": "68f58c133cee921146f43280eab26b48",
        "ans_hash_43708": "94e04c73514c1ebd671e2a15f72795e7",
        "ans_hash_43709": "d75c75e36582f5cc2960cd3ba5645953",
        "ans_hash_43714": "e8537a40df0b9f152bd3ac55c0d3f672",
        "ans_hash_43728": "d53636db2494ca994944096a375f951c",
        "ans_hash_43729": "f5a64158f21639a942f2ee111e7a048e",
        "ans_hash_43731": "589ef64a8746e6dc0ba9be41656c9e8d",
        "ans_hash_43732": "0987286d344b3a0b1465884c4e863a34",
        "ans_hash_43738": "4b87f3f1ff8755a58ed05e256c6dbf7c",
        "ans_hash_43752": "8b28fb80d6675399100604da7e677846",
    })
    req = urllib.request.Request(url, param.encode('utf-8'), header)
    r = urllib.request.urlopen(req)
    return_str = r.read().decode('utf-8')
    return json.loads(return_str)

def send_request():
    url = "https://account.bilibili.com/answer/getQstByType"
    param = urllib.parse.urlencode({
        "type_ids": "14,15,16,17,19,21,23,25,27,28"
    })
    req = urllib.request.Request(url, param.encode('utf-8'), header)
    r = urllib.request.urlopen(req)
    return_str = r.read().decode('utf-8')
    return json.loads(return_str)


def read_ids():
    ids_file = open('ids', 'r')
    ids_str = ids_file.read()
    result = set()
    if len(ids_str) > 0:
        result = eval(ids_str)
    ids_file.close()
    return result


def write_ids(ids):
    ids_file = open('ids', 'w')
    ids_file.write(repr(ids))
    ids_file.close()


qs_ids = read_ids()
f = open('data', 'a', encoding='utf-8')
times = 0
while True:
    unknown_count = 0
    for j in range(10):
        if times % 50 == 0:
            write_ids(qs_ids)
        return_json = send_request()
        i = 0
        if return_json['status']:
            for item in return_json['data']:
                qs_id = item['qs_id']
                if qs_id in qs_ids:
                    continue
                i += 1
                qs_ids.add(qs_id)
                f.write(item['qs_id'])
                f.write('|' + item['ans1_hash'])
                f.write('|' + item['ans2_hash'])
                f.write('|' + item['ans3_hash'])
                f.write('|' + item['ans4_hash'])
                f.write('|' + item['question'])
                f.write('|' + item['ans1'])
                f.write('|' + item['ans2'])
                f.write('|' + item['ans3'])
                f.write('|' + item['ans4'])
                f.write('\n')
            f.flush()
            times += 1
        else:
            answer_result = auto_answer()
            if answer_result['status']:
                continue
            else:
                break
        unknown_count += i
        print(i)
    if unknown_count <= 10:
        print('unknown_count is %d' % unknown_count)
        break
    print('unknown_count %d' % unknown_count)
f.close()
write_ids(qs_ids)
print("end")
