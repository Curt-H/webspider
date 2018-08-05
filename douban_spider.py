"""
爬虫, 用于爬取
https://movie.douban.com/top250
页面的电影信息
"""
import os
import requests
from pyquery import PyQuery as pq

from utils import log


class Movie(object):
    def __init__(self):
        self.name = ""
        self.score = ""
        self.quote = ""
        self.cover_url = ""


def collect_data(content):
    e = pq(content)
    items = e(".item")
    return items


def cached_url(url, filename):
    """

    :param url:
    :param filename:
    :return:
    """
    u = url
    fname = filename

    folder = 'cache'
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
            return r.content


def save_pic(movies):
    for path in movies:
        filename = f'{path.name}.png'
        cached_url(path.cover_url, filename)


def get_all_page_url():
    urls = list()
    for i in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={i}"
        urls.append(url)
    return urls


def __main():
    url = get_all_page_url()
    for i, u in enumerate(url):
        log(f'URL is {u}')

        content = cached_url(u, f'page{i}')
        print(collect_data(content))


if __name__ == '__main__':
    __main()
