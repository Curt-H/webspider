class Post(object):
    def __init__(self):
        self.post_id = ''
        self.post_url = ''
        self.coser_id = ''
        self.coser_name = ''
        self.pic_urls = []

    def __repr__(self):
        result = [f'{k}: {v}' for k, v in self.__dict__.items()]

        return '\n'.join(result)


class Coser(object):
    def __init__(self):
        self.coser_id = ''
        self.coser = ''
        self.posts = []

    def __repr__(self):
        result = [f'{k}: {v}' for k, v in self.__dict__.items()]

        return '\n'.join(result)
