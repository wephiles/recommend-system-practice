def load_file(path):
    
    with open(path, "r") as fp:
        for line in fp:
            yield line    
import os

def main():
    print(os.getcwd())