# -*- coding: utf-8 -*-
# @Time : 2022/1/12 10:10 上午
# @Author : 李炳翰
# @File : OLH.py
# @Software: PyCharm


import numpy as np
import xxhash
import random
import sys


class OLH_USER(object):
    def __init__(self, epsilon, domain, data):
        super(OLH_USER, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 原始数据定义区间
        self.domain = domain
        # 用户的原始数据
        self.data = data
        # 扰动数据
        self.per_data = []

        # 为使用方便，定义e^\epsilon
        e_epsilon = np.exp(self.epsilon)

        #设置g为最佳本地哈希的值
        self.g = int(round(e_epsilon)) + 1

        # 协议中的扰动概率
        self.p = e_epsilon / (e_epsilon + self.g - 1)
        self.q = 1.0 / (e_epsilon + self.g - 1)

    def run(self):
        encode_x = self.encode(self.data)
        perturb_x = self.perturb(encode_x)
        self.per_data = perturb_x


    def encode(self, v: int):
        seed = random.randint(0, sys.maxsize)
        hash = (xxhash.xxh32(str(v), seed=seed).intdigest() % self.g)
        return seed, hash

    def perturb(self, encode_list):
        for i in len(encode_list)
            if np.random.uniform(0, 1) < self.p:
                return encode_list
            else:
                per_data = random.randint(0, self.g)
                # 当随机选择的元素与之前的x一致时，再进行随机选择，直到不一致为止
                while per_data == encode_list[i]:
                    per_x = random.randint(0, self.g)
                return per_x

    def get_per_data(self):
        return self.per_data


class OLH_SERVER(object):
    def __init__(self, epsilon: float, per_datalist: list, domain: list):
        super(OLH_SERVER, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 扰动数据列表
        self.per_datalist = per_datalist
        # 用户数量
        self.n = len(per_datalist)
        # 频率估计结果
        self.es_data = []
        # 值域
        self.domain = domain

        e_epsilon = np.exp(self.epsilon)

        # 设置g为最佳本地哈希的值
        self.g = int(round(e_epsilon)) + 1

        # 协议中的扰动概率
        self.p = e_epsilon / (e_epsilon + self.g - 1)
        self.q = 1 / self.g

    def estimate(self):
        for x in self.domain:
            count = 0
            for data in self.per_datalist:
                if xxhash.xxh32(str(x), seed=data[0]).intdigest() % self.g == data[1]:
                    count = count + 1
            rs = (count - self.n * self.q) / (self.n * (self.p - self.q))
            self.es_data.append(rs)

    def get_es_data(self):
        return self.es_data
