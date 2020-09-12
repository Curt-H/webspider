import requests as req
from utils import log

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
}

class WebPage(object):

    def __init__(self, url, use_proxy=True, proxy="127.0.0.1:10809"):
        self.url = url
        self.use_proxy = use_proxy
        self.proxy = proxy

        self.get_content()


    def get_content(self):
        if self.use_proxy:
            proxies = {
                "http": "http://127.0.0.1:10809",
                "https": "http://127.0.0.1:10809",
            }
        response = req.get(self.url, headers=headers, proxies=proxies)
        self.content = response.text
        log('html content length:', len(self.content))
    
    def save_to_html(self):
        with open('test.html', 'w+', encoding='utf-8') as f:
            f.write(self.content)

