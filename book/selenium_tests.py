#from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import ast
import tqdm
from fuzzywuzzy import fuzz
from  seleniumwire import webdriver


service = Service(executable_path="D:\BookScan\msedgedriver.exe")
options = webdriver.EdgeOptions()
#options.add_argument("--headless")
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
options.add_argument("--disable-extensions")  # Отключение расширений
options.add_argument("--disable-gpu")  # Отключение GPU
options.add_argument("--disable-infobars")  # Отключение инфо-панели
options.add_argument("--disable-javascript")  # Отключение JavaScript (если необходимо)
PROXY = "23.227.38.160:80"
USERNAME = "gtnD5u"
PASSWORD = "WogPZf"
#options.add_argument(f'--proxy-server=http://{PROXY}')
driver = webdriver.Edge(service=service, options=options)


def decision(res, request):
    print(f'seartching { request}')
    fzr = []
    if res !=['']:
        for i in res:
            fzr.append(fuzz.token_sort_ratio(i, request))
        avg = (fzr.pop(fzr.index(max(fzr))) + fzr.pop(fzr.index(max(fzr))) + fzr.pop(fzr.index(max(fzr)))) / 3
        if avg >= 70:
            print('Доверенный источник')
        elif avg > 60 and avg < 70:
            print('Есть сомнения')
        else:
            print('Сомнительная книга')

        print(avg)
    else:
        print('Нет результатов')


def make_request(request):
    driver.get(f"https://www.google.com/search?q={request}")
    driver.implicitly_wait(3)
    try:
        quick_results = driver.find_element(By.CSS_SELECTOR, 'div.dURPMd')
    except Exception as e:
        return ['']
    return quick_results.text.split('\n')

start_time = time.time()




with open('out.txt', 'rt', encoding='utf-8') as f:
    for ln in f:
        time.sleep(1)
        a = ast.literal_eval(ln)
        for i in a[1]:
            time.sleep(1)
            s = f'{a[0]} - {i}'
            res = make_request(s)
            decision(res, s)

driver.quit()




