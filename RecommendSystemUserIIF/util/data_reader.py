import random


# 生成器函数
def generate_data(file_path):
    """加载数据——生成器函数
    
    :param file_path: 文件路径
    :return: None
    """
    with open(file_path, "r") as fp:
        for line in fp:
            yield line


def split_dataset(data_path=r"./RecommendSystemUserIIF/data/ml-100k/u.data", train_rate=0.8, seed=1):
    """划分数据集。

    :param data_path: 数据文件路径
    :param train_rate: 训练数据集的大小，默认值为0.8，即80%
    :param seed:
    :return: ([train_set], [test_set]) 元组
    """
    train_set, test_set = [], []
    random.seed(seed)

    for line in generate_data(data_path):
        user, item, rating, _ = line.split("\t").replace("\n", "")
        if random.random() < train_rate:
            train_set.append([int(user), int(item), int(rating)])
        else:
            test_set.append([int(user), int(item), int(rating)])
    return train_set, test_set


def all_items(data_path=r"./RecommendSystemUserIIF/data/ml-100k/u.data"):
    """得到所有movie信息

    :param data_path: 文件存储路径
    :return:
    """
    items = set()

    for line in generate_data(data_path):
        _, item, _, _ = line.replace("\n", "").split("\t")
        items.add(item)
    return items
