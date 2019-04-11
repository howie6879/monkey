#!/usr/bin/env python
"""
 Created by howie.hu at 2018/10/15.
"""
import os

import jieba

from monkey.config import Config


def gen_stop_words():
    """
    停用词选取哈工大停用词表
    https://github.com/goto456/stopwords/blob/09002cceefe2e47487b21d5d6cf49c60ef3c1ee5/%E5%93%88%E5%B7%A5%E5%A4%A7%E5%81%9C%E7%94%A8%E8%AF%8D%E8%A1%A8.txt
    :return:
    """
    with open(os.path.join(Config.BASE_DIR, 'common/stop_words.txt'), 'r') as fp:
        stop_words = [_.strip() for _ in fp.readlines()]
    return stop_words


def text_seg(text: str, stop_words: list = None) -> list:
    """
    对输入的文本利用jieba分词进行分词
    :param text:
    :return: []
    """
    seg_list = []
    if not stop_words:
        stop_words = gen_stop_words()
    for each in jieba.cut(text):
        if each not in stop_words and not each.isspace():
            # 对于单词 全部默认小写
            seg_list.append(each.lower())

    return seg_list


if __name__ == '__main__':
    print(text_seg('学习c语言的教材'))
