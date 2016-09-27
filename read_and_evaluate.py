#!/usr/bin/python3
# -*- coding: utf-8 -*-

from config import ARTICLE_PATH, LABEL_PATH
from os import listdir
from os.path import isfile

if __name__ == "__main__":
    for article in set(listdir(ARTICLE_PATH)).difference(set(LABEL_PATH)):
        print("#####")
        with open(ARTICLE_PATH + article, 'r') as text:
            print("Please evaluete this article")
            print(text.read())
            print("if you liked this article press Y or y, press N or n  otherwise")
            answer = input()
            if answer in ['Y', 'y']:
                result = '1'
            elif answer in ['N', 'n']:
                result = '0'
            else:
                continue
            with open(LABEL_PATH + article, 'w') as f:
                f.write(result)
        print("if you want to exit read_and_evaluate you need to write key-word 'exit'")
        if input() == "exit":
            break
        print("###")
