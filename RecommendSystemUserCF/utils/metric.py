"""
RMSE代表均方根误差（Root Mean Square Error），是一种常用的衡量预测模型误差的指标。它是均方误差（Mean Square Error，MSE）的平方根。
MSE是计算预测值与真实值之间差异的平方的平均值。具体而言，对于每个数据点，计算预测值与真实值之差的平方，然后将所有差值的平方求和并除以数据点的数量，即可得到MSE。MSE越小，表示预测模型的拟合效果越好。
RMSE是MSE的平方根，它与原始数据的单位相匹配，因此更容易解释。RMSE越小，表示预测模型的预测误差越小。通常情况下，我们更倾向于使用RMSE来评估模型的性能，因为它对较大误差的惩罚更重，并且与原始数据的单位一致，更易于解释。
"""

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


"""
准确率（Precision）是一个用于衡量推荐系统的评估指标之一，它衡量了推荐系统在给用户推荐物品时，推荐的物品中有多少是用户实际感兴趣的物品。
准确率的计算方式是通过将推荐系统返回的与用户实际感兴趣的物品相匹配的物品数量，除以推荐系统返回的物品总数量。准确率的计算公式如下：
准确率 = 推荐结果中与用户实际感兴趣的物品相匹配的物品数量 / 推荐结果的物品总数量
准确率的取值范围在0到1之间，越接近1表示推荐系统的推荐结果中更多的物品是用户感兴趣的。
需要注意的是，准确率只关注推荐结果的准确性，而不考虑推荐系统是否找回了用户感兴趣的所有物品。因此，在实际评估中，通常会综合考虑准确率、召回率、排序质量等指标来综合评估推荐系统的性能。
"""


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


"""
在推荐系统中，召回率（Recall）是一种用于衡量推荐系统性能的评估指标之一。召回率衡量了推荐系统在给用户推荐物品时，成功将用户感兴趣的物品找回的能力。
召回率的计算方式是通过将推荐系统返回的与用户实际感兴趣的物品相匹配的物品数量，除以用户实际感兴趣的物品的总数量。召回率的计算公式如下：
召回率 = 推荐结果中与用户实际感兴趣的物品相匹配的物品数量 / 用户实际感兴趣的物品总数量
召回率的取值范围在0到1之间，越接近1表示推荐系统能够更好地找回用户感兴趣的物品。
召回率是评估推荐系统的重要指标之一，它强调推荐系统找回用户感兴趣的物品的能力。然而，召回率并不能完全衡量推荐系统的质量，因为它忽略了推荐系统的准确性和推荐结果的排序。因此，在实际评估中，通常会综合考虑召回率、准确率、排序质量等指标来综合评估推荐系统的性能。
"""


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


"""
在推荐系统中，覆盖率（Coverage）是衡量推荐系统推荐物品的多样性和能够涵盖到的物品范围的指标。它衡量了推荐系统能够推荐到多少不同的物品或物品类别。
覆盖率通常通过计算推荐系统能够覆盖的物品数量或物品类别数量来衡量。具体的计算方式可以根据具体的定义和需求而有所不同。
覆盖率较高表示推荐系统能够涵盖更广泛的物品或物品类别，提供更多样化的推荐结果。这对于推荐系统的用户体验和推荐的新颖性都是有益的。然而，覆盖率较高可能也意味着推荐系统更偏向于热门或流行的物品，而忽略了长尾（Long Tail）物品的推荐。
因此，在实际评估中，需要综合考虑覆盖率、准确率、召回率、排序质量等指标来综合评估推荐系统的性能，以找到一个平衡点，既能提供多样化的推荐结果，又能准确地满足用户的个性化需求。
"""


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


"""
在推荐系统中，流行度（Popularity）是衡量物品在整个用户群体中的普遍程度或受欢迎程度的指标。它衡量了物品在推荐系统中的受欢迎程度或广泛程度。
流行度可以用于衡量不同物品的推荐优先级或权重。一般来说，流行度较高的物品在推荐系统中可能会被更多的用户看到或被更多的用户选择。相反，流行度较低的物品可能在推荐系统中被较少的用户看到或选择。
流行度的计算方式可以有多种形式，具体取决于推荐系统的设计和需求。一种常见的计算方式是根据物品的点击量、购买量、评分或其他相关指标来衡量流行度。较高的点击量、购买量或评分通常表示物品更受用户欢迎，因此具有较高的流行度。
在推荐系统中，流行度可以用于优化推荐算法的效果。例如，可以将一定比例的推荐结果保留给热门物品，以确保满足用户的广泛需求和兴趣。然而，过度依赖流行度可能导致推荐系统的偏向性，忽略了个性化的推荐需求和长尾物品的推荐。因此，在推荐系统中，需要综合考虑流行度、个性化度、多样性等指标，以平衡推荐结果的准确性和用户体验。
"""


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
