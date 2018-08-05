from bcy_model import Post, Coser
import requests
import os
from pyquery import PyQuery as Pq
from html import unescape
from utils import log


def cached_url(url, filename):
    """
    缓存网页
    :param url: 网址
    :param filename: 缓存的名字
    :return: 返回网页页面的HTML代码
    """
    u = url
    fname = filename

    folder = 'bcy'
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, fname)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
            return s
    else:
        r = requests.get(u)
        content = unescape(r.text)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            return content


def get_posts_urls(pq_root, coser_id):
    e = pq_root('.pager .pager__item a')
    cid = coser_id

    page_nums = int(e.attr('href').split('=')[-1])
    log(f'用户<{cid}>POST列表页共有{page_nums}页')

    url_template = f'https://bcy.net/u/{cid}/post?&p={{}}'
    urls = [url_template.format(p + 1) for p in range(page_nums)]
    log(urls)
    return urls


def get_post_models(url, index, cid):
    u = url
    i = index
    ms = list()
    e = Pq(cached_url(u, f'{cid}-cache-{i}'))

    posts = e('.gridList li.js-smallCards')
    for p in posts:
        link = Pq(p)('a.db')

        post = Post()
        post.coser_id = cid
        post.coser_name = link.attr('title').replace(' ', '')
        post.post_url = f'https://bcy.net{link.attr("href")}'
        post.post_id = post.post_url.split('/')[-1]
        post.post_urls
        ms.append(post)
        log(post)
    return ms


def __main():
    coser_id = '25216'
    coser_homepage_url = f'https://bcy.net/u/{coser_id}/post?&p=1'
    e = Pq(cached_url(coser_homepage_url, f'{coser_id}-cache-1'))

    urls = get_posts_urls(e, '25216')
    post_models = []
    for i, u in enumerate(urls):
        post_models += get_post_models(u, i + 1, coser_id)
    log(post_models)


if __name__ == '__main__':
    __main()
