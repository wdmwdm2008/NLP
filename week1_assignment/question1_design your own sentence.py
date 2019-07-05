#!/usr/bin/python
# -*- coding: UTF-8 -*-


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


if __name__ == '__main__':
    weather = """
        weather = 某时 某地 气象 助词 情况
        某时 = 某年 | 某天
        某年 = 今年 | 明年 | 前年 | 去年 | 多年以前
        某天 = 今天 | 明天 | 前天 | 后天
        某地 = 河南省 | 河北省 | 山东省
        河南省 = 郑州 | 开封 | 洛阳
        河北省 = 邯郸 | 大名 | 石家庄
        山东省 = 济南 | 青岛
        气象 = 天气 | 气候
        助词 = 很 | 非常 | 太
        情况 = 热 | 冷 | 湿 | 干
    """

    movie = """
        movie = 代指 电影 助词 表达
        代指 = 这个 | 那个
        电影 = 英雄 | 泰坦尼克号 | 漫威 | 黑客帝国
        助词 = 很 | 非常 | 太
        表达 = 好看了 | 难看了 | 垃圾了 | 惨了
    """
    gram = create_grammar(movie)

    # First grammar
    # print(generate_sentence(gram, "weather"))

    # Second grammar
    print("Please input number ...")
    number = int(input())
    print(generate_n_sentence(gram, "movie", number))
