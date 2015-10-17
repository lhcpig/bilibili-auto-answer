#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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


class Topic:
    def __init__(self, data):
        self.question = data[0]
        self.answers = [data[1], data[2], data[3], data[4]]
        self.i = 0

    def set_answer(self, i):
        self.i = i

    def answer(self):
        return self.answers[self.i]


def send_request(question_answer):
    url = "https://account.bilibili.com/answer/goPromotion"
    param = dict()
    param['qs_ids'] = ','.join(question_answer.keys())
    for k, v in question_answer.items():
        param['ans_hash_' + k] = v
    req = urllib.request.Request(url, urllib.parse.urlencode(param).encode('utf-8'), header)
    r = urllib.request.urlopen(req)
    return_str = r.read().decode('utf-8')
    return json.loads(return_str)


def get_topics(file, topic_list, num):
    for i in range(num):
        line = file.readline()
        if not line:
            break
        topic_list.append(Topic(line.split('|')))
    return topic_list

if __name__ == '__main__':
    f = open('data', 'r', encoding='utf-8')
    answer_file = open('answer', 'w+', encoding='utf-8')
    topics = []
    index = 0
    not_find_times = 0
    while True:
        find = False
        topics = get_topics(f, topics, 20 - len(topics))
        if len(topics) < 20:
            print('last ------------------')
            for topic in topics:
                print(topic.question)
            break
        questionToAnswer = {}
        for topic in topics:
            topic.set_answer(index)
            questionToAnswer[topic.question] = topic.answer()
        return_json = send_request(questionToAnswer)
        message = return_json['message']
        if not return_json['status']:
            for topic in topics:
                if topic.question in message:
                    topic.set_answer(index)
                else:
                    find = True
                    topics.remove(topic)
                    answer_file.write(topic.question + '|' + topic.answer()+'\n')
        else:
            for topic in topics:
                answer_file.write(topic.question + '|' + topic.answer()+'\n')
            topics = []
        index = (index + 1) % 4
        if find:
            not_find_times = 0
        else:
            not_find_times += 1
        if not_find_times >= 4:
            for topic in topics:
                print(topic.question)
            not_find_times = 0
            topics = []
