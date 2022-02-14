# -*- coding: utf-8 -*-
# @Time : 2022/1/12 10:10 上午
# @Author : 金严
# @File : BLH.py
# @Software: PyCharm

import random
import sys

import numpy as np
from collections import Counter

import xxhash


class BLH_USER(object):
    def __init__(self, epsilon, data, domain):
        super(BLH_USER, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 用户的原始数据
        self.data = data
        # hash函数key、扰动数据
        self.per_data = []
        # 原始数据定义域
        self.domain = domain

        e_epsilon = np.exp(self.epsilon)

        # 协议中的扰动概率
        self.p = e_epsilon / (e_epsilon + 1)
        self.q = 1 / (e_epsilon + 1)

    def run(self):
        encode_x = self.encode(self.data)
        perturb_x = self.perturb(encode_x)
        self.per_data = perturb_x

    def encode(self, raw_data: int):  # 返回hash函数seed、哈希值
        seed = random.randint(0, sys.maxsize)
        hash_data = (xxhash.xxh32(str(raw_data), seed=seed).intdigest() % 2)
        return seed, hash_data

    def perturb(self, encode_list):  # 返回hash函数seed、扰动结果
        per_x = encode_list[1]
        if np.random.uniform(0, 1) < self.p:
            return encode_list
        else:
            #per_data = random.randint(0, 1)
            # 当随机选择的元素与之前的x一致时，再进行随机选择，直到不一致为止
            #while per_data == encode_list[1]:
                #per_x = random.randint(0, 1)
            per_x = per_x ^ 1
            return encode_list[0], per_x

    def get_per_data(self):
        return self.per_data


class BLH_SERVER(object):
    def __init__(self, epsilon: float, per_datalist: list, domain: list):
        super(BLH_SERVER, self).__init__()
        # 隐私预算
        self.epsilon = epsilon
        # 所有用户的扰动数据（hash函数key、对应扰动数据值）
        self.per_datalist = per_datalist
        # 用户数量
        self.n = len(per_datalist)
        # 频率估计结果
        self.es_data = []
        # 值域
        self.domain = domain

        e_epsilon = np.exp(self.epsilon)

        # 协议中的扰动概率
        self.p = e_epsilon / (e_epsilon + 1)
        self.q = 1 / 2

    def estimate(self):
        # count = Counter(per_data)
        # count_dict = dict(count)
        for x in self.domain:
            count = 0
            for data in self.per_datalist:
                if xxhash.xxh32(str(x), seed=data[0]).intdigest() % 2 == data[1]:
                    count = count + 1
            rs = (count - self.n * self.q) / (self.n * (self.p - self.q))
            self.es_data.append(rs)

    def get_es_data(self):
        return self.es_data


# if __name__ == '__main__':
#     data = np.concatenate(
#         ([1] * 300, [2] * 40, [3] * 222, [4] * 100, [5] * 80))
#     original_freq = list(Counter(data).values()) # True frequencies of the dataset
#     l = len(data)
#     for index, item in enumerate(original_freq):
#         frequency = item/l
#         original_freq[index] = frequency
#
#
#     epsilon = 3
#     d = 5
#
#     per_data = []
#
#     for item in data:
#         blh_user = BLH_USER(epsilon, item, range(1, 6))
#         blh_user.run()
#         per_data.append(blh_user.get_per_data())
#         # print("原始数据：%d" % item)
#         # print(blh_user.get_per_data())
#
#     blh_server = BLH_SERVER(epsilon, per_data, range(1, 6))
#     blh_server.estimate()
#     print("频率估计：")
#     print(blh_server.get_es_data())
#     print("原始频率：")
#     print(original_freq)