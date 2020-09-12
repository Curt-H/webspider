from time import localtime, strftime


def log(*args, **kwargs):
    t = localtime()
    st = strftime('%Y-%m-%d %I:%M:%S', t)

    print(f'[{st}]')
    for i in args:
        print(f'[{i}]')
    for k in kwargs.keys():
        print(f'[{k}={kwargs[k]}]')

    print()

    with open('log.txt', 'a+', encoding='utf-8') as f:
        for i in args:
            print(f'[{i}]', file=f)
        for k in kwargs.keys():
            print(f'{k}={kwargs[k]}', file=f)
        print(file=f)


def name_filter(name: str):
    ban_list = ('/', '?', '\\', '*', '<', '>', ':', '"')
    for b in ban_list:
        name = name.replace(b, '')
    return name

if __name__ == '__main__':
    for i in range(10):
        log('test')
        log('a', c='fuck')
        log('a', 'c', 'b', abc=5)
