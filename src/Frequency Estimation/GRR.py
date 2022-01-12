# -*- coding: utf-8 -*-
# @Time : 2022/1/12 10:09 上午
# @Author : 贺星宇
# @File : GRR.py
# @Software: PyCharm


import numpy as np
from random import choice
from collections import Counter


class GRR_USER(object):
    def __init__(self, epsilon: float, domain: list, data: int):
        super(GRR_USER, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 原始数据定义域
        self.domain = domain
        # 原始数据定义域的长度
        self.d = len(domain)
        # 用户的原始数据
        self.data = data
        # 扰动数据
        self.per_data = -1

        # 为使用方便，定义e^\epsilon
        e_epsilon = np.exp(self.epsilon)

        # 协议中的扰动概率
        self.p = e_epsilon / (e_epsilon + self.d - 1)
        self.q = 1 / (e_epsilon + self.d - 1)

    def run(self):
        encode_x = self.encode(self.data)
        perturb_x = self.perturb(encode_x)
        self.per_data = perturb_x

    # 此时传入的是用户的原始数据，并不是该数据在domain中的位置
    def encode(self, x: int) -> int:
        return x

    # 返回的是扰动后的数据，并不是在domain中的
    def perturb(self, x: int) -> int:
        if np.random.uniform(0, 1) < self.p:
            return x
        else:
            per_x = choice(self.domain)
            # 当随机选择的元素与之前的x一致时，再进行随机选择，直到不一致为止
            while per_x == x:
                per_x = choice(self.domain)
            return per_x

    def get_per_data(self):
        return  self.per_data

class GRR_SERVER(object):
    def __init__(self, epsilon: float, domain: list, per_datalist: list):
        super(GRR_SERVER, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 原始数据定义域
        self.domain = domain
        # 原始数据定义域的长度
        self.d = len(domain)
        # 所有用户的扰动数据
        self.per_datalist = per_datalist
        # 用户数量
        self.n = len(per_datalist)
        # 频率估计结果
        self.es_data = []

        # 为使用方便，定义e^\epsilon
        e_epsilon = np.exp(self.epsilon)

        # 协议中的扰动概率
        self.p = e_epsilon / (e_epsilon + self.d - 1)
        self.q = 1 / (e_epsilon + self.d - 1)

    def estimate(self, per_data: list):
        # 在获取扰动数据中元素频率时，一定要用字典，可以大大节省运行时间
        count = Counter(per_data)
        count_dict = dict(count)

        for x in self.domain:
            x_count = count_dict.get(x, 0)
            rs = (x_count - self.n * self.q) / (self.n * (self.p - self.q))
            self.es_data.append(rs)

    def get_es_data(self):
        return self.es_data