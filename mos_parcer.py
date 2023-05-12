import json
import requests
from bs4 import BeautifulSoup
import re


def mos_parc(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    news = re.findall(r"pageProps\":(.+),\"__N_SSP*", str(soup))
    news_json = json.loads(news[0])
    news_json_sd = news_json['sectionsData']
    text_arr = []
    url_arr = []
    for element in news_json_sd.items():
        text_element = element[1]
        for text_one in text_element:
            try:
                text_parc = text_one['element']['title']
                text_arr.append(text_parc)
                url_parc = text_one['element']['url']
                if url_parc[0:5] == 'https':
                    url_parc = url_parc
                else:
                    url_parc = 'https://www.mos.ru' + url_parc
                url_arr.append([url_parc, text_parc])
            except Exception as e:
                print(e)
                pass

    return url_arr


if __name__ == '__main__':
    url = mos_parc('https://mos.ru')

    with open('res.txt', 'w') as f:
        for i, url_one in enumerate(url):
            f.write(str(i) + ': ' + url_one[1] + '--->' + url_one[0] + '\n')
