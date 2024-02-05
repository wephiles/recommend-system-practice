import random


# 根据文件名载入数据
def load_file(file_name):  # 生成器函数
    with open(file_name, "r") as fp:
        for line in fp:
            yield line

            
def read_rating_data(path="./data/ml-100k/u.data", train_rate=1., seed=1):
    """载入评分数据
    
    :param path: 文件路径
    :param train_rate: 训练集占整个数据集的大小，默认为1，表示整个数据集都是训练集
    :param seed: 
    :return: tuple
    """
    train_set = list()
    test_set = list()

    random.seed(seed)

    for line in load_file(file_name=path):
        user, movie, rating, _ = line.split("\t")
        if random.random() < train_rate:
            train_set.append([int(user), int(movie), int(rating)])
        else:
            test_set.append([int(user), int(movie), int(rating)])
    return train_set, test_set


def all_items(path="./data/ml-100k/u.data"):
    """返回所有的电影信息。
    
    :param path: 数据路径。
    :return: tuple of movie。
    """
    items = set()
    for line in load_file(path):
        _, movie, _, _ = line.split("\t")
        items.add(movie)
    return items


def read_all_data(path):
    data_list = []
    for line in load_file(path):
        user, movie, rating, _ = line.replace("\n", "").split("\t")
        data_list.append([user,movie,rating])
    return data_list
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    