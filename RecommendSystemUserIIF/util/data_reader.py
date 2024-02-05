import random


# 生成器函数
def load_data(file_path):
    """加载数据——生成器函数
    
    :param file_path: 文件路径
    :return: None
    """
    with open(file_path, "r") as fp:
        for line in fp:
            yield line


def read_rating_data():
    pass
