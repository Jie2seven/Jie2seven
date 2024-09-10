import re
import jieba
import numpy
import jieba.analyse
import math
import unittest
from simhash import Simhash
"""
 软件工程第二次作业：
    设计一个论文查重算法：在给出一个原文件和一个抄袭文件(_增、删、改_)计算出其重复率

    文件形式：txt文件

    输入形式：从命令行参数当中读入原文件，抄袭文件，答案文件的绝对路径

    输出格式：以文件的形式输出

    输出结果：论文的重复率
"""


def short_analyse(o_file, c_file):
    """
    思路：
        我们首先读取数据然后对数据进行一个jieba分词，同时根据正则匹配来过滤掉标点
    :param o_file: 原始论文的地址
    :param c_file: 抄袭论文的地址
    :return: 返回两个分词结果的列表
    """
    jieba.setLogLevel(jieba.logging.INFO)  # 使用中文词库来进行分词，防止报错
    o_list = []
    c_list = []
    try:
        with open(o_file, 'r', encoding='utf-8') as f:
            o_lines = f.readlines()
        for line in o_lines:
            pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")  # 正则匹配保留中文字符
            target = pattern.sub("", line)
            for data in jieba.lcut(target):
                o_list.append(data)
    except FileNotFoundError:
        print(f"{o_file}这个路径下没有文件")
        raise FileNotFoundError

    try:
        with open(c_file, 'r', encoding='utf-8') as f:
            c_lines = f.readlines()
        for line in c_lines:
            pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")  # 正则匹配保留中文字符
            target = pattern.sub("", line)
            for data in jieba.lcut(target):
                c_list.append(data)

    except FileNotFoundError:
        print(f"{c_file}这个路径下没有文件")
        raise FileNotFoundError

    all_words = list(set(o_list).union(set(c_list)))
    print(all_words)
    la = []
    lb = []
    # 转换为向量的形式
    for word in all_words:
        la.append(o_list.count(word))
        lb.append(c_list.count(word))

    # 计算余弦相似度
    laa = numpy.array(la)
    lbb = numpy.array(lb)
    cos = (numpy.dot(laa, lbb.T)) / ((math.sqrt(numpy.dot(laa, laa.T))) * (math.sqrt(numpy.dot(lbb, lbb.T))))
    print(f"两篇文章的相似度为{cos}")


def long_analyse(fname):
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"{fname}这个路径下并不存在文件")

    tags = jieba.analyse.extract_tags(content, 15)
    print(tags)
    return tags


def compute_sim(o_file, c_file):
    i = set(o_file).intersection(set(c_file))
    j = set(o_file).union((set(c_file)))
    return round(len(i) / len(j), 2)


def long_ans(o_file, c_file):
    a1 = long_analyse(o_file)
    a2 = long_analyse(c_file)
    return compute_sim(a1, a2)


def save_data(a_file, cos):
    """

    :param a_file: 答案文件的路径
    :return:
    """
    try:
        with open(a_file, 'w', encoding='utf-8') as f:
            f.write(f"这篇文章的抄袭率为{cos}")
    except FileNotFoundError:
        print(f"{a_file}这个路径下没有文件")


def simhash_demo(text_a, text_b):
    """
    求两文本的相似度

    :param text_a:
    :param text_b:
    :return:
    """
    try:
        with open(text_a, 'r', encoding='utf-8') as f:
            content_a = f.read()

    except FileNotFoundError:
        print(f"{text_a}这个路径下文件不存在")
        raise FileNotFoundError

    try:
        with open(text_b, 'r', encoding='utf-8') as f:
            content_b = f.read()

    except FileNotFoundError:
        print(f"{text_a}这个路径下文件不存在")
        raise FileNotFoundError

    a_simhash = Simhash(content_a)
    b_simhash = Simhash(content_b)
    max_hashbit = max(len(bin(a_simhash.value)), len(bin(b_simhash.value)))
    # 汉明距离
    distince = a_simhash.distance(b_simhash)
    # print(distince)
    similar = 1 - distince / max_hashbit
    return similar


if __name__ == '__main__':
    o_file = ".\o_file "
    c_file = ".\c_file "
    short_analyse(o_file, c_file)
    print(f"两个文本之间的相似度为{long_ans(o_file, c_file)}")
    print(f"利用simhash求得相似度{simhash_demo(o_file, c_file)}")