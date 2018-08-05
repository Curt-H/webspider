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
        # 电影名
        self.name = ""
        # 电影评分
        self.score = ""
        # 一句话影评
        self.quote = ""
        # 热度
        self.hot = ""
        # 封面URL
        self.cover_url = ""

    def __repr__(self):
        """
        重定义Print函数
        """
        attr_list = [f"{k}: {v}" for k, v in self.__dict__.items()]
        result = '\n'.join(attr_list)
        return result

    def save(self):
        """
        将对象信息生成为一个md文件
        """
        fname = self.name.split('/')[0].replace(' ', '')

        with open(f'cache\\{fname}.md', 'w', encoding='utf-8') as f:
            f.write(self.__repr__())
            f.write(f'\r\n![{fname}]({fname}.jpg)')


def collect_data(content):
    """
    分析页面内的数据
    :param content: 页面HTML源代码
    """
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
    """
    将封面的图片下载下来
    :param movie: movie实例
    """
    fname = movie.name.split('/')[0] + '.jpg'
    fname = fname.replace(' ', '')

    cached_url(movie.cover_url, fname)


def cached_url(url, filename):
    """
    缓存网页
    :param url: 网址
    :param filename: 缓存的名字
    :return: 返回网页页面的HTML代码
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
    """
    生成所有的页面URL
    :return: URL列表
    """
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
