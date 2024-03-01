# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/22 022 16:00
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : JupyterProjects/metric.py
# @Description : 评价指标
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import math


class Metric(object):
    """Metric类，用以实现评价指标。"""

    def __init__(
            self,
            train_set=None,
            test_set=None,
            recommends=None,
            all_items=None,
            records=None,
            item_popularity=None,
            N=1):
        self.train_set = train_set
        self.test_set = test_set
        self.N = N
        self.records = records
        self.recommends = recommends
        self.all_items = all_items
        self.item_popularity = item_popularity

    def RMSE(self, records=None):
        """
        预测准确度-RMSE.
        :param records:
        :type records:
        :return:
        :rtype:
        """
        if records is None:
            records = self.records
        molecule = sum([(pred_rating - actual_rating) ** 2 for pred_rating, actual_rating in records])  # 分子
        denominator = float(len(records))  # 分母
        return math.sqrt(molecule) / denominator

    def MSE(self, records=None):
        """
        计算准确率-MSE.
        Args:
            records ():

        Returns:

        """
        molecule = sum([abs(pred_rating - actual_rating) for pred_rating, actual_rating in records])
        denominator = float(len(records))
        return molecule / denominator

    def precision(self, recommends=None, test_set=None):
        """计算准确率，计算公式参考项亮《操作系统实践》

        Args:
            recommends (dict): 推荐结果集
            test_set (dict): 测试集

        Returns:

        """
        if recommends is None:
            recommends = self.recommends
        if test_set is None:
            test_set = self.test_set
        n_union = 0
        user_sum = 0
        for user, items in recommends.items():  # {user1: {item1, item2, ...}, user2: {item3, item3, ...}}
            recommend_set = set(items)
            testset = set(test_set[user])
            n_union += len(recommend_set & testset)
            user_sum += len(testset)
        return n_union / user_sum

    def recall(self, recommends, test_set):
        """计算召回率.

        :param recommends:
        :type recommends:
        :param test_set:
        :type test_set:
        :return:
        :rtype:
        """
        if recommends is None:
            recommends = self.recommends
        if test_set is None:
            test_set = self.test_set
        n_union = 0
        user_sum = 0
        for user, items in recommends.items():  # {user1: {item1, item2, ...}, user2: {item3, item3, ...}}
            recommend_set = set(items)
            testset = set(test_set[user])
            n_union += len(recommend_set & testset)
            user_sum += len(recommend_set)
        return n_union / user_sum

    def coverage(self, recommends, all_items):
        """
        计算覆盖率。
        Args:
            recommends (dict): {user: items}
            all_items (list): [item1, item2, ...]

        Returns:
            覆盖率
        """
        if recommends is None:
            recommends = self.recommends
        if all_items is None:
            all_items = self.all_items
        recommend_items = set()
        for _, items in recommends.items():
            for item in items:
                recommend_items.add(item)
        return len(recommend_items) / len(all_items)

    def popularity(self, item_popularity, recommends):
        """

        Args:
            item_popularity ():
            recommends ():

        Returns:

        """
        if item_popularity is None:
            item_popularity = self.item_popularity
        if recommends is None:
            recommends = self.recommends
        popularity = 0
        N = 0
        for _, items in recommends.items():
            for item in items:
                popularity += math.log(1 + item_popularity.get(item, 0.))
                N += 1
        return popularity / N

# END
