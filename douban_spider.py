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
        self.hot = ""
        self.cover_url = ""

    def __repr__(self):
        attr_list = [f"{k}: {v}" for k, v in self.__dict__.items()]
        result = '\n'.join(attr_list)
        return result

    def save(self):
        fname = self.name.split('/')[0].replace(' ', '')

        with open(f'cache\\{fname}.md', 'w', encoding='utf-8') as f:
            f.write(self.__repr__())
            f.write(f'\r\n![{fname}]({fname}.jpg)')


def collect_data(content):
    e = pq(content)
    items = e(".item")

    for i in items:
        e = pq(i)

        m = Movie()
        m.name = e('.info .title').text().replace(' /', '/')
        m.score = e('.rating_num').text()
        m.quote = e('.inq').text()
        m.hot = e('.star').text().replace(f'{m.score} ', '')
        m.cover_url = e('div.pic img').attr('src')
        save_pic(m)

        m.save()
        log(m)


def save_pic(movie):
    fname = movie.name.split('/')[0] + '.jpg'
    fname = fname.replace(' ', '')

    cached_url(movie.cover_url, fname)


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

    path = os.path.join(folder, fname)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        r = requests.get(u)
        with open(path, 'wb') as f:
            f.write(r.content)
            return r.content


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

        content = cached_url(u, f'page{i}').replace(b'&nbsp;', b'')
        collect_data(content)


if __name__ == '__main__':
    __main()
