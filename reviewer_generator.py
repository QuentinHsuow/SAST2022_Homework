# -*- coding: utf-8 -*-
import argparse
from random import shuffle
import os
import re


def parse_data():
    """
    用来解析命令行参数
    1. -n 表示用户希望从自己所选择范围内具体想要复习的单词数量
    2. --r 表示用户希望随机选择单词（不输入 --r 则表示不希望随机选择）
    3. -s 表示用户希望从第几个单词开始
    4. -l 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
    :return: num, is_random, start, length
    """

    parser = argparse.ArgumentParser(
        prog="TOELF words reviewer",
        description="choose random or sorted method.",
        allow_abbrev=True,
    )
    parser.add_argument(
        "-n",
        "--num",
        dest="num",
        type=int,
        default=50,
        help="how many words would you like to review",
    )
    parser.add_argument(
        "--r",
        action="store_true",
        dest="random",
        help="if you want to random select, then input --r, ohterwise do not",
    )
    parser.add_argument(
        '-s',
        dest="start",
        type=int,
        default=0,
        help='which index to start reading from',
    )
    parser.add_argument(
        '-l',
        dest="length",
        type=int,
        default=0,
        help='how many words would you randomly choose from',
    )
    args = parser.parse_args()
    return args.random, args.num, args.start, args.length


def get_index():
    """
    使用 os.walk 方法来获取所有单词本的编号，返回单词本的最大编号，即 index
    :return: index - 单词本的最大编号
    """
    for _, dirs, ___ in os.walk("."):
        index = 0
        for dire in dirs:
            if dire.startswith('workbook'):
                index = max(
                    index, max([int(each) for each in (re.findall(r"\d+", dire))])
                )
    return index


def generate_workbook(num, is_random, start, length):
    """
    :param num: int 具体想要复习的单词数量
    :param is_random: bool True表示随机选取单词
    :param start: int 从第几个单词开始
    :param length: int 希望复习的单词范围
    """

    # extract所有单词
    with open('collection.txt', 'r', encoding="utf-8") as f:
        words = list(filter(lambda x: x != '', f.read().split('\n')))

    # 缩小words到指定范围
    if 0 <= length < len(words):
        if start + length > len(words):
            words = words[start::]
        elif start + length <= len(words):
            words = words[start:start + length]
        if num > len(words):
            num = len(words)

    # if is_random 就将words随机排序
    if is_random:
        shuffle(words)

    # 将words划分为许多小list,每一个小list单独生成一个txt文件
    words_lists = [[words[i*num+j] for j in range(num)] for i in range(len(words) // num)]
    words_lists.append([words[i] for i in range(num * (len(words) // num), len(words))])

    # 进行翻译
    wordbook_index = get_index()
    for list_idx, word_list in enumerate(words_lists):
        # untranslated
        with open(f'workbook{wordbook_index}/untranslated${list_idx}.txt', 'w') as f:
            for word_idx, words in enumerate(word_list):
                similar_words = words.split(',')
                f.write(f'第{word_idx}组单词为: ' + '  '.join(similar_words) + '\n')

        # translated
        with open(f'workbook{wordbook_index}/translated${list_idx}.txt', 'w') as f:
            for word_idx, words in enumerate(word_list):
                similar_words = words.split(',')
                f.write(f'第{word_idx}组单词为: ' + '  '.join(similar_words) + '\n')


if __name__ == '__main__':
    generate_workbook(*parse_data())
