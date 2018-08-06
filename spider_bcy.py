from bcy_model import Post, Coser
import requests
import os
from pyquery import PyQuery as Pq
from html import unescape
from utils import log
from time import sleep


def cached_url(url, filename):
    """
    缓存网页
    :param url: 网址
    :param filename: 缓存的名字
    :return: 返回网页页面的HTML代码
    """
    u = url
    fname = filename

    folder = 'bcy\\cache'
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


def save_pics(post_model, index, all):
    m = post_model
    ix = index
    a = all
    pic_nums = len(m.pic_urls)

    folder = f'bcy\\{m.coser_id}-{m.coser_name}'
    if not os.path.exists(folder):
        os.makedirs(folder)

    for i, u in enumerate(m.pic_urls):
        fname = f'{m.post_id}-{i}.jpg'
        path = os.path.join(folder, fname)

        r = requests.get(u)
        content = r.content
        with open(path, 'wb') as f:
            f.write(content)
        sleep(1)
        log(f'下载POST<{m.post_id}>中......\n'
            f'第{i+1}/{pic_nums}图片成功\n'
            f'URL:{u}\n'
            f'处理的是第{ix}/{a}个POST')


def get_pic_urls(url, filename, post_id):
    pid = post_id
    u = url
    fname = filename

    e = Pq(cached_url(u, f'{fname}-post-{pid}'))
    pics = e('.detail_std')
    pic_urls = []

    for p in pics:
        url = Pq(p).attr('src').replace('/w650', '')
        pic_urls.append(url)

    return pic_urls


def get_posts_urls(pq_root, coser_id):
    e = pq_root('.pager .pager__item a')
    cid = coser_id

    log()
    if len(e) > 0:
        pager = Pq(e[-1]).attr('href')
        page_nums = int(pager.split('=')[-1])
    else:
        page_nums = 1
    log(f'用户<{cid}>POST列表页共有{page_nums}页')

    url_template = f'https://bcy.net/u/{cid}/post?&p={{}}'
    urls = [url_template.format(p + 1) for p in range(page_nums)]
    log(urls)
    return urls


def get_post_models(url, index, coser_id):
    u = url
    i = index
    cid = coser_id

    ms = list()
    fname = f'{cid}-cache-{i}'
    e = Pq(cached_url(u, fname))

    posts = e('.gridList li.js-smallCards')
    for p in posts:
        link = Pq(p)('a.db')

        post = Post()
        post.coser_id = cid
        post.coser_name = link.attr('title').replace(' ', '')
        post.post_url = f"https://bcy.net{link.attr('href')}"
        post.post_id = post.post_url.split('/')[-1]
        post.pic_urls = get_pic_urls(post.post_url, fname, post.post_id)
        ms.append(post)
        log(post)

    return ms


def __main():
    coser_id = '54783'
    coser_homepage_url = f'https://bcy.net/u/{coser_id}/post?&p=1'
    e = Pq(cached_url(coser_homepage_url, f'{coser_id}-cache-1'))

    urls = get_posts_urls(e, coser_id)
    post_models = []
    for i, u in enumerate(urls):
        post_models += get_post_models(u, i + 1, coser_id)

    post_nums = len(post_models)
    log(f'COSER({coser_id})共{post_nums}个POST')
    for i, post in enumerate(post_models):
        save_pics(post, i + 1, post_nums)


if __name__ == '__main__':
    __main()
