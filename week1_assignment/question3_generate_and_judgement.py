#!/usr/bin/python
# -*- coding: UTF-8 -*-


import re
import jieba
from collections import Counter
import random


def create_grammar(grammar, split='='):
    gram = {}
    for line in grammar.split("\n"):
        if not line.strip():
            continue
        exp, stmt = line.split(split)
        gram[exp.strip()] = [s.split() for s in stmt.split(" | ")]
    return gram


def generate_sentence(grammar, target):
    if target not in grammar:
        return target
    expend = [generate_sentence(grammar, t) for t in random.choice(grammar[target])]
    return ''.join([e for e in expend])


def generate_n_sentence(grammar, target, n):
    result = []
    while n > 0:
        n -= 1
        result.append(generate_sentence(grammar, target))
    return result


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

    insurance = """
        insurance = 称谓 动作 东西
        称谓 = 指代我 | 指代你 | 指代他
        指代我 = 我 | 我们 | 俺们 | 俺
        指代你 = 你 | 你们 | 您们
        指代他 = 他 | 她 | 他们
        动作 = 想要 | 想买 | 去买 | 去得到
        东西 = 汽车保险 | 房屋保险 | 健康保险 | 人寿保险 | 火车保险 | 卡车保险 | 人道主义
    """

    gram = create_grammar(insurance)

    print("Please input number ...")
    number = int(input())
    need_compareds = generate_n_sentence(gram, "insurance", number)

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

    sorted_list = []
    for need_compared in need_compareds:
        sorted_list.append((need_compared, get_probability(need_compared)))
    best_sentence = sorted(sorted_list, key = lambda x:x[1], reverse=True)[0]
    print('{} is more possible'.format(best_sentence[0]))
    print('-'*4 + ' {} with probability {}'.format(best_sentence[0], best_sentence[1]))




# 缺点： 1套语法只能生成1个句子, 当我们想要用1套语法生成多个句子时,合理性就大大降低,花费很长时间才能生成1个较合理的句子
# 如何提升： 创造多套语法, 1套语法尽可能生成多个合理句子,不必要求非常合理,但是要让人明白其意思（基于花费时间和句子合理性来生成）
