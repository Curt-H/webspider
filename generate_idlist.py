import json

from utils import log


def load_coser_namelist():
    with open('idList.txt', mode='r', encoding='utf-8') as id_file:
        nl = json.load(id_file)
        log(nl)

    return nl


def write_coser_namelist(namelist):
    with open('idList.txt', mode='w', encoding='utf-8') as id_file:
        json.dump(namelist, id_file)


if __name__ == '__main__':
    cosers = load_coser_namelist()

    while 1:
        coser = input('Coser ID: ')
        if coser == '':
            break
        cosers.append(coser)
        log(f'{coser} has been added!')

    write_coser_namelist(cosers)

    for i in cosers:
        log(i)
