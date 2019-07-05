#!/usr/bin/python
# -*- coding: UTF-8 -*-


import re
import jieba
from collections import Counter


def token(string):
    return re.findall(r'\w+', string)


def cut(string):
    return list(jieba.cut(string))


def prob_1(word):
    return word_count[word]/len(TOKEN)


def prob_2(word1, word2):
    if word1 + word2 in words_count_2:
        return words_count_2[word1 + word2] / word_count[word1]
    else:
        return 1 / len(TOKEN_2_GRAM)  # 或者可以定义为 (prob_1(word1) + prob_1(word2)) / 2


def get_probability(sentence):
    words = cut(sentence)

    sentence_pro = prob_1(words[0])

    for i, word in enumerate(words[:-1]):
        next_ = words[i + 1]
        probalitity = prob_2(word, next_)

        sentence_pro *= probalitity
    return sentence_pro


if __name__ == '__main__':

    # Cleaning data and save it into train_clean.txt
    # with open("train.txt", 'r', encoding="UTF-8", errors="ignore") as f:
    #     insurance_clean = [''.join(token(str(line.split("++$++")[2]))) for line in f.readlines()]
    # with open("train_clean.txt", 'w', encoding="UTF-8", errors="ignore") as f:
    #     for a in insurance_clean:
    #         f.write(a + '\n')

    # Reading data from text and then jieba cut them
    TOKEN = []

    for i, line in enumerate(open('train_clean.txt', encoding="UTF-8", errors="ignore")):
        TOKEN += cut(line)
    TOKEN = [str(t) for t in TOKEN]

    # Obtaining the count of each word
    word_count = Counter(TOKEN)

    # Obtaing 2-gram list
    TOKEN_2_GRAM = [''.join(TOKEN[i:i + 2]) for a in range(len(TOKEN[:-1]))]

    # Counting the number of each two words
    words_count_2 = Counter(TOKEN_2_GRAM)

    need_compared = [
        '保险怎么卖 吃什么保险',
        '保险有什么用 保险无用',
        '我喜欢来十个保险 我喜欢来1000个保险',
        '飞一份保险 保险来一份'
    ]

    for s in need_compared:
        s1, s2 = s.split()
        p1, p2 = get_probability(s1), get_probability(s2)
        better = s1 if p1 > p2 else s2
        print('{} is more possible'.format(better))
        print('-'*4 + ' {} with probability {}'.format(s1, p1))
        print('-'*4 + ' {} with probability {}'.format(s2, p2))



