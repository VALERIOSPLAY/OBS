import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import Levenshtein
import langdetect
from concurrent.futures import ThreadPoolExecutor

ua = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
proxies = {
    'socks5':'gtnD5u:WogPZf@217.29.53.64:10664'
}

def detect_language(text):
    try:

        return langdetect.detect(text)
    except Exception as e:
        raise e
        return ''
def get_google_search_results(query):
    url = f"https://www.google.com/search?q={query}&lr=lang_{detect_language(query)}"
    response = requests.get(url, proxies=proxies)

    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.text)
    search_results = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')
    suggestion = soup.find('div', class_='Va3FIb EE3Upf lVm3ye')
    print(detect_language(query))
    return [result.text for result in search_results]

def get_duckduckgo_search_results(query):
    url = f"https://html.duckduckgo.com/html/?q={query}"
    response = requests.get(url, headers=ua, proxies=proxies)

    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)
    search_results = soup.select('.result__body')

    return [result.text.strip('\n') for result in search_results]

def get_bing_search_results(query):
    url = f"https://www.bing.com/search?q={query}&setlang=ru"
    response = requests.get(url, proxies=proxies)

    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.text)
    search_results = soup.find_all('h2')
    for i in search_results:
        print(i.text)
    return [result.text.strip() for result in search_results]



def get_ya_search_results(query):
    url = f"https://ya.ru/search/?text={query}&lr=213"
    response = requests.get(url, proxies=proxies)

    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.text)
    search_results = soup.find_all('h2')
    for i in search_results:
        print(i.text)
    return [result.text.strip() for result in search_results]

def decision(book):
    print(f'searching {book}')
    fzr = []
    res = get_ya_search_results(book)

    if res !=[]:
        for i in res:
            fzr.append(fuzz.token_set_ratio(i, query))
        avg = (fzr.pop(fzr.index(max(fzr))) + fzr.pop(fzr.index(max(fzr))) + fzr.pop(fzr.index(max(fzr)))) / 3
        if avg >= 15:
            print('Доверенный источник')
        elif avg > 5 and avg < 10:
            print('Есть сомнения')
        else:
            print('Сомнительная книга')

        print(avg)
    else:
        print('Нет результатов')




query = "Nassim Nicholas Taleb"

queries = ["Lianxian Han - Na pa hai de niao", "Толкиен - Властелин колец", "Максим Ильяхов - Пиши, сокращай"]
#Lianxian Han - Na pa hai de niao | BAD

print(decision(query))


