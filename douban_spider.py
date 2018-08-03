"""
爬虫, 用于爬取
https://movie.douban.com/top250
页面的电影信息
"""
import os
import requests
from pyquery import PyQuery as pq


class Movie(object):
    def __init__(self):
        self.name = ""
        self.score = ""
        self.quote = ""
        self.cover_url = ""


if __name__ == '__main__':
    pass
