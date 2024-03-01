# -*- coding: utf-8 -*-
# @CreateTime : 2024/2/22 022 11:31
# @Author : 瑾瑜@20866
# @IDE : PyCharm
# @File : JupyterProjects/metric.py
# @Description : 
# @Interpreter : python 3.10
# @Motto : You must take your place in the circle of life!
# @Site : https://github.com/wephiles or https://gitee.com/wephiles

import math


def RMSE(records):
    """计算RMSE 

    :param records: 预测评价与真实评价的一个list
    :return: RMSE值
    """
    numerator = sum([(pred_rating - actual_rating) ** 2 for pred_rating, actual_rating in records])  # 分子
    denominator = float(len(records))  # 分母
    return math.sqrt(numerator / denominator)


def MSE(records):
    """计算MSE

    :param records: 预测评价与真实评价的一个list
    :return: MSE值
    """
    numerator = sum([(pred_rating - actual_rating) ** 2 for pred_rating, actual_rating in records])  # 分子
    denominator = float(len(records))  # 分母
    return numerator / denominator


def precision(recommends, tests):
    """计算准确度

    :param recommends: 给用户推荐的商品 dict {UserID: 推荐的物品}
    :param tests: 测试集 dict {UserID: 实际发生事务的物品}
    :return: float 精确度 precision
    """
    n_union = 0
    user_sum = 0
    for user_id, items in recommends.items():
        recommend_set = set(items)
        test_set = set(tests[user_id])
        n_union += len(recommend_set & test_set)
        user_sum += len(test_set)
    return n_union / user_sum


def recall(recommends, tests):
    """计算召回率

    :param recommends: 给用户推荐的商品 dict {UserID: 推荐的物品}
    :param tests: 测试集 dict {UserID: 实际发生事务的物品}
    :return: 召回率 recall
    """
    n_union = 0
    recommend_sum = 0
    for user_id, items in recommends.items():
        recommend_set = set(items)
        test_set = set(tests[user_id])
        n_union += len(recommend_set & test_set)
        recommend_sum += len(recommend_set)
    return n_union / recommend_sum


def coverage(recommends, all_items):
    """计算覆盖率

    :param recommends:  dict     {UserID: Items}
    :param all_items:   list/set 所有的item
    :return:            float    覆盖率
    """
    recommend_items = set()
    for _, items in recommends.items():
        for item in items:
            recommend_items.add(item)
    return len(recommend_items) / len(all_items)


def popularity(item_popular, recommends):
    """计算流行度

    :param item_popular: 商品流行度　dict形式{ itemID : popularity}
    :param recommends: dict形式 { userID : Items }
    :return: 平均流行度
    """
    popularity = 0.
    n = 0
    for _, items in recommends.items():
        for item in items:
            popularity += math.log(1. + item_popular.get(item, 0.))
            n += 1
    return popularity / n

# END
