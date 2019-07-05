import random
import pandas as pd
import jieba
import re
from functools import reduce
from operator import add, mul
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


def adj():
    return random.choice('蓝色的 | 小小的 | 好看的'.split(' | ')).split()[0]


def adj_star():
    return random.choice([None, adj() + adj()])


def create_grammar(adj_grammar, split='=>'):
    grammar = {}
    for line in adj_grammar.split("\n"):
        if not line.strip():
            continue
        exp, stmt = line.split(split)
        grammar[exp.strip()] = [s.split() for s in stmt.split(" | ")]
    return grammar


def generate(gram, target):
    if target not in gram:
        return target
    expend = [generate(gram, t) for t in random.choice(gram[target])]
    return ''.join([e for e in expend if e != 'null'])


def cut(string):
    return list(jieba.cut(string))


def prob_1(word):
    return word_count[word]/len(TOKEN)


def prob_2(word1, word2):
    if word1 + word2 in words_count_2:
        return words_count_2[word1 + word2] / len[TOKEN_2_GRAM]
    else:
        return 1 / len(TOKEN_2_GRAM)  # 或者可以定义为 (prob_1(word1) + prob_1(word2)) / 2


def get_probability(sentence):
    words = cut(sentence)

    sentence_pro = 1

    for i, word in enumerate(words[:-1]):
        next_ = words[i + 1]
        probalitity = prob_2(word, next_)

        sentence_pro *= probalitity
    return sentence_pro


def token(string):
    return re.findall(r'\w+', string)


if __name__ == '__main__':

    # Question 1

    print(adj_star())

    # Question 2

    adj_grammar = """
        Adj* => null | Adj Adj*
        Adj => 蓝色的 | 好看的 | 小小的
    """

    # Question 3

    simple_grammar = """
        sentence => noun_phrase verb_phrase
        noun_phrase => article Adj* noun
        Adj* => null | Adj Adj*
        verb_phrase => verb noun_phrase

        article => 一个 | 这个
        noun => 女人 | 篮球 | 桌子 | 小猫
        verb => 看着 | 坐在 | 听着 | 看见
        Adj => 蓝色的 | 好看的 | 小小的
    """

    temp_grammar = create_grammar(simple_grammar)

    print(generate(gram=temp_grammar, target='sentence'))

    filename = "C:/study/sqlResult_1558435.csv"
    content = pd.read_csv(filename, encoding='gb18030')
    articles = content['content'].tolist()

    # Cleaning data
    articles_clean = [''.join(token(str(a))) for a in articles]

    # Writing data into text
    with open('article_9k.txt', 'w', encoding='UTF-8', errors='ignore') as f:
        for a in articles_clean:
            f.write(a + '\n')

    # Reading data from text and then jieba cut them
    TOKEN = []

    for i, line in enumerate(open('article_9k.txt', encoding="UTF-8")):
        if i > 50000:
            break
        TOKEN += cut(line)
    TOKEN = [str(t) for t in TOKEN]

    # Obtaining the count of each word
    word_count = Counter(TOKEN)

    # Obtaing 2-gram list
    TOKEN_2_GRAM = [''.join(TOKEN[i:i+2]) for a in range(len(TOKEN[:-2]))]

    # Counting the number of each two words
    words_count_2 = Counter(TOKEN_2_GRAM)



    # 可视化 - 单词频率
    #
    # for sen in [generate(gram=example_grammar, target='sentence') for i in range(10)]:
    #     print("sentence: {} with Prob: {}".format(sen, get_probility(sen)))

    need_compared = [
        '我今天晚上请你吃大餐,我们一起吃日料 明天晚上请你吃大餐,我们一起吃苹果',
        '真事一只好看的小猫 真是一只好看的小猫',
        '今晚我去吃火锅 今晚火锅去吃我',
        '洋葱奶昔来一杯 养乐多绿来一杯'
    ]

    for s in need_compared:
        s1, s2 = s.split()
        p1, p2 = get_probability(s1), get_probability(s2)
        better = s1 if p1 > p2 else s2
        print('{} is more possible'.format(better))
        print('-'*4 + ' {} with probability {}'.format(s1, p1))
        print('-'*4 + ' {} with probability {}'.format(s2, p2))
