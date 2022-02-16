# -*- coding: utf-8 -*-
# @Time : 2022/1/12 10:10 上午
# @Author : 王源源
# @File : OUE.py
# @Software: PyCharm



import numpy as np
import math
from random import choice
from collections import Counter


class OUE_USER(object):
    def __init__(self, epsilon: float, domain: list, data: int):
        super(OUE_USER, self).__init__()
        self.epsilon = epsilon  # 隐私预算
        self.domain = domain  # 原始数据定义域
        self.d = len(domain)  # 原始数据定义域的长度
        self.data = data  # 用户的原始数据
        self.per_data = []  # 扰动数据

        e_epsilon = np.exp(self.epsilon)  # 为使用方便，定义e^\epsilon

        # 协议中的扰动概率
        self.p = 1 / 2
        self.q = 1 / (e_epsilon + 1)

    def run(self):
        encode_x = self.encode(self.data)
        perturb_x = self.perturb(encode_x)
        self.per_data = perturb_x

    def encode(self, x) -> list:
        l = list()
        for i in range(self.d):
            if i == x:
                l.append(1)
            else:
                l.append(0)
        return l

    def perturb(self, x: list) -> list:
        for i in range(self.d):
            if np.random.uniform(0, 1) < self.p:
                continue
            else:
                if x[i] == 0:
                    x[i] = 1
                else:
                    x[i] = 0
        return x

    def get_per_data(self):
        return self.per_data


class OUE_SERVER(object):
    def __init__(self, epsilon: float, domain: list, per_datalist: list):
        super(OUE_SERVER, self).__init__()
        self.epsilon = epsilon  # 隐私预算
        self.domain = domain  # 原始数据定义域
        self.d = len(domain)  # 原始数据定义域的长度
        self.per_datalist = per_datalist  # 所有用户的扰动数据
        self.n = len(per_datalist)  # 用户数量
        self.es_data = []  # 频率估计结果

        e_epsilon = np.exp(self.epsilon)  # 为使用方便，定义e^\epsilon

        # 协议中的扰动概率
        self.p = 1 / 2
        self.q = 1 / (e_epsilon + 1)

    def estimate(self, per_data: list):
        array = np.sum(per_data, axis=0)
        count_dict = dict(zip(per_data, array))

        for x in self.domain:
            x_count = count_dict.get(x, 0)
            rs = (x_count - self.n * self.q) / (self.n * (self.p - self.q))
            self.es_data.append(rs)

    def get_es_data(self):
        return self.es_data
