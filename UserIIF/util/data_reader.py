# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/22 022 16:02
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : JupyterProjects/data_reader.py
# @Description : 读取数据工具类
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import random
import sys


class DataReader(object):
    """数据读取类，用以读取数据。"""

    def __init__(self, file_path=r""):
        self.file_path = file_path
        self.ratio = 1.
        self.seed = 1

    def load_file(self):
        """读取文件

        :return: 一个生成器对象，每次调用生成一条数据，不会全部生成
        :rtype: iterable object
        """
        try:
            with open(self.file_path, "r") as fp:
                for line in fp:
                    yield line
        except FileNotFoundError as e:
            print("File Not Found Error: ", e, file=sys.stderr)

    def split_dataset(self):
        """划分数据集

        :return: ([train_set], [test_set])
        :rtype: tuple
        """
        train_set, test_set = [], []
        random.seed(self.seed)
        for line in self.load_file():
            for user, item, rating, time_stamp in line.replace("\n", "").split("\t"):
                if random.random() <= self.ratio:
                    train_set.append((int(user), int(item), int(rating), int(time_stamp)))
                else:
                    test_set.append((int(user), int(item), int(rating), int(time_stamp)))
        return train_set, test_set

    def get_all_items(self):
        """获取所有物品信息(电影信息)

        :return: [(), (), ...]
        :rtype: list[tuple]
        """
        data_list = []
        for line in self.load_file():
            _, item, _, _ = line.replace("\n", "").split("\t")
            data_list.append((int(item),))
        return data_list

    def read_all_data(self):
        """获取所有数据。

        :return: [(), (), ...]
        :rtype: list[tuple]
        """
        all_data_list = []
        for line in self.load_file():
            user, item, rating, time_stamp = line.replace("\n", "").split("\t")
            all_data_list.append((int(user), int(item), int(rating)))
        return all_data_list

# END
