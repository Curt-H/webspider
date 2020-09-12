from spider_server import WebPage
from pyquery import PyQuery as pq
from utils import log, name_filter
import os
from time import sleep

class Novel(object):
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.pq = pq(self.raw_text)

        self.get_title()
        self.get_content()

    def get_title(self):
        title = self.pq('title').text().replace("18av,", "")
        title = name_filter(title)
        log("Title size:", len(title))
        self.title = title

    def get_content(self):
        content = self.pq('table').text()
        log('Content size:', len(content))
        self.content = content

    def save_to_text(self, path, index="0"):

        if not os.path.exists(path):
            log('Path not exists, try to create')
            os.makedirs(path)

        filename = f'{path}\\{index}-{self.title}.txt'
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.content)


if __name__ == "__main__":

    path = input('指定保存路径: ')

    for i in range(3547, 8000):
        log(i)
        wp = WebPage(f'http://18av.mm-cg.com/novel_{i}.html')

        novel = Novel(wp.content)
        novel.save_to_text(path, index=f'{i}')

        sleep(2)