import os
import time
import requests as rq
from bs4 import BeautifulSoup as bs
import re

words = """race, dog, alex"""
ALLWORDS = words.split(", ")
ALLPREFIX = """un-, in-, im-, il-, ir-, non-, mis-, mal-, dis-, anti-, de-, under-"""
ALLSUFIX = """ee, en, """
HEAD = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 YaBrowser/20.8.1.79 Yowser/2.5 Safari/537.36',
    'accept': '*/*'}
allprefix = ALLPREFIX.split("-, ")
allsufix = ALLSUFIX.split(", ")


def create_pref_sufx(MyList):
    pref = list()
    sufx = list()
    for i in MyList:
        if i[0] != '':
            pref.append(i[0])
        if i[-1] != '':
            sufx.append(i[-1])
    return pref, sufx


def get_modify_word(result, word):
    data = bs(result.text, 'html.parser')
    items = str(data.find_all("ul", class_="preflist"))
    all_find_word = re.findall(r'>(\w*)</a>', items)
    PrePotList = [re.split(re.compile(rf'(\s+)?{word}(\s+)?'), i) for i in all_find_word]
    pref, sufx = create_pref_sufx(PrePotList)
    return str("".join(f"({p})" for p in pref) + f" {word} " + "".join(f"({s})" for s in sufx))


if __name__ == '__main__':
    try:
        os.mkdir("Find_result")
    except:
        pass
    # Для массива слов
    for i in ALLWORDS:
        result = rq.get("https://www.niftyword.com/prefix-suffix-derived/" + i.lower() + "/", headers=HEAD)
        if result.status_code == 200:
            result = rq.get("https://www.niftyword.com/prefix-suffix-derived/" + i.lower() + "/", headers=HEAD)
            with open(f'Find_result\\{i}.txt', 'w', encoding='utf-8') as f:
                res = get_modify_word(result, i.lower())
                f.write(res)
        elif result.status_code == 502:
            raise requests.HTTPError("Проблеммы сервера")
        else:
            print(f"Слова {word} нет в словаре")

    # Для одного слова
    # word = str("cat").lower()
    # result = rq.get("https://www.niftyword.com/prefix-suffix-derived/" + word + "/", headers=HEAD)
    # print(get_modify_word(result, word))
