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
