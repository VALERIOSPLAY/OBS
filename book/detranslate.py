from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tqdm
import ast

# Инициализация драйвера
driver = webdriver.Chrome()

tabs = []
for _ in range(10):
    driver.execute_script("window.open('https://translate.google.com/#view=home&op=translate&sl=auto&tl=ru');")
    tabs.append(driver.window_handles[-1])

word_list = []
with open('out2.txt', 'rt', encoding='utf-8') as f:
    for counter, line in enumerate(tqdm.tqdm(f, desc='books formed'), start=1):
        a = ast.literal_eval(line)
        for i in a[1]:
            s = f'{a[0]} - {i}'
            word_list.append(s)


translated_list = []
st = time.time()
i = 0
while i < len(word_list):
    current_tabs = []
    for j, tab in enumerate(tabs):
        # Переключение на вкладку
        driver.switch_to.window(tab)

        try:
            # Ввод слова для перевода
            input_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'er8xn')))
            input_box.clear()
            input_box.send_keys(word_list[i + j])
            current_tabs.append(tab)
        except IndexError:
            break

    time.sleep(0.5)

    for tab in current_tabs:
        try:
            driver.switch_to.window(tab)
            translated_word = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ryNqvb')))
            print(translated_word.text)
            translated_list.append(translated_word.text)
        except Exception as e:
            pass

    i += len(tabs)
print(time.time()-st)
# Закрытие браузера
driver.quit()

# Вывод списка переведенных слов
#print(translated_list)
