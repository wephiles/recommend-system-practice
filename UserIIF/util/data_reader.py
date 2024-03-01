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

    def load_file(self, file_path=r""):
        """读取文件

        :param file_path:
        :rtype file_path:
        :return: 一个生成器对象，每次调用生成一条数据，不会全部生成
        :rtype: iterable object
        """
        if file_path == r"":
            file_path = self.file_path
        try:
            with open(file_path, "r") as fp:
                for line in fp:
                    yield line
        except FileNotFoundError as e:
            print("File Not Found Error: ", e, file=sys.stderr)

    def split_dataset(self, file_path=r"", ratio=0., seed=1):
        """划分数据集

        :return: ([train_set], [test_set])
        :rtype: tuple
        """
        if file_path == r"":
            file_path = self.file_path
        if ratio == 0:
            ratio = self.ratio
        train_set, test_set = [], []
        random.seed(seed)
        for line in self.load_file(file_path):
            user, item, rating, time_stamp = line.replace("\n", "").split("\t")
            if random.random() <= ratio:
                train_set.append((int(user), int(item), int(rating)))
            else:
                test_set.append((int(user), int(item), int(rating)))
        return train_set, test_set

    def get_all_items(self, file_path=r""):
        """获取所有物品信息(电影信息)

        :return: [(), (), ...]
        :rtype: list[tuple]
        """
        if file_path == r"":
            file_path = self.file_path
        data_list = []
        for line in self.load_file(file_path):
            _, item, _, _ = line.replace("\n", "").split("\t")
            data_list.append((int(item),))
        return data_list

    def read_all_data(self, file_path=r""):
        """获取所有数据。

        :return: [(), (), ...]
        :rtype: list[tuple]
        """
        if file_path == r"":
            file_path = self.file_path
        all_data_list = []
        for line in self.load_file(file_path):
            user, item, rating, time_stamp = line.replace("\n", "").split("\t")
            all_data_list.append((int(user), int(item), int(rating), int(time_stamp)))
        return all_data_list

# END
