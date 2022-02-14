# -*- coding: utf-8 -*-
# @Time : 2022/1/12 10:09 上午
# @Author : 王凤祥
# @File : SUE.py
# @Software: PyCharm

import numpy as np
from random import choice
from collections import Counter


class SUE_USER(object):
    def __init__(self, epsilon, domain, data):
        super(SUE_USER, self).__init__()
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

        # 为使用方便，定义e^\epsilon2
        e_epsilon2 = np.exp(self.epsilon / 2)

        # 协议中的扰动概率
        self.p = e_epsilon2 / (e_epsilon2 + 1)
        self.q = 1 / (e_epsilon2 + 1)

    def run(self):
        encode_x = self.encode(self.data)
        perturb_x = self.perturb(encode_x)
        self.per_data = perturb_x

    # 此时传入的是用户的原始数据，并不是该数据在domain中的位置
    def encode(self, x) :
        l = list()
        for i in range(self.d):
            if i == x:
                l.append(1)
            else:
                l.append(0)
        #print(l)
        return l

    # 返回的是扰动后的数据，并不是在domain中的
    def perturb(self, x) :
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


class SUE_SERVER(object):
    def __init__(self, epsilon, domain, per_datalist):
        super(SUE_SERVER, self).__init__()
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

        # 为使用方便，定义e^\(epsilon/2)
        e_epsilon2 = np.exp(self.epsilon / 2)

        # 协议中的扰动概率
        self.p = e_epsilon2 / (e_epsilon2 + 1)
        self.q = 1 / (e_epsilon2 + 1)

    def estimate(self):
        m = list()
        for i in range(self.d):
            m.append(0)
            for l in self.per_datalist:
                if l[i] == 1:
                    m[i] += 1

        for x in self.domain:
            x_count = m[x]
            rs = (x_count - self.n * self.q) / (self.n * (self.p - self.q))
            self.es_data.append(rs)

    def get_es_data(self):
        return self.es_data

