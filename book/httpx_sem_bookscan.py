import httpx
import fake_useragent as ua
import time
import ast
from fuzzywuzzy import fuzz
import Levenshtein
import random
import asyncio
from bs4 import BeautifulSoup
import tqdm
import aiofiles

headers = {"User-Agent": str(ua.UserAgent.random)}
clients = {}

with open("proxies.txt","rt", encoding="utf-8") as pr:

    proxy_list=[f"http://{proxy.strip()}" for proxy in pr]
    #proxy_list=proxy_list[:30]

cnt=0
proxy_queue = asyncio.Queue()
for proxy in proxy_list:
    proxy_queue.put_nowait(proxy)

def decision(res, request):
    fzr = []
    if res !=[]:
        for i in res:
            fzr.append(fuzz.token_sort_ratio(i, request))
        avg = round((fzr.pop(fzr.index(max(fzr))) + fzr.pop(fzr.index(max(fzr))) + fzr.pop(fzr.index(max(fzr)))) / 3, 2)
        if avg >= 65:
            pass
            #print(f'Доверенный источник {avg}, for {request}')
        elif avg > 50 and avg < 65:
            pass
            #print(f'Есть сомнения {avg}, for {request}')
        else:
            pass
            #print(f'Сомнительная книга {avg}')

    else:
        pass
        #print(f'Нет результатов for {request}')

async def hx_request(request, client, proxy):
    global cnt
    cnt+=1
    print(f' {cnt}. Requesting {request} with proxy {proxy}')

    #time.sleep(random.uniform(0.001, 0.002))
    response = await client.get(f"https://www.bing.com/search?q={request}", headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    search_results = soup.find_all('h2')
    return [i.text for i in search_results]


start_time = time.time()

async def process_query(query):
    #print(f'queue size: {proxy_queue.qsize()}')
    proxy = await proxy_queue.get()
    #print(f'locking proxy {proxy}')
    try:
        results = await hx_request(query, clients[proxy], proxy)
    except Exception as e:
        clients[proxy] = httpx.AsyncClient(proxies={"http://": proxy, "https://": proxy})
        results = await hx_request(query, clients[proxy], proxy)
    decision(results, query)
    #print(f'setting free proxy {proxy}\n\n')
    proxy_queue.put_nowait(proxy)



sem = asyncio.Semaphore(10000)  # Ограничиваем количество одновременных задач

async def worker(sem, queue):
    async with sem:  # Ограничиваем количество одновременных задач
        while True:
            query = await queue.get()
            if query is None:
                break
            await process_query(query)
            queue.task_done()

async def reader(queue):
    async with aiofiles.open('out.txt', 'rt', encoding='utf-8') as f:
        async for line in f:
            a = ast.literal_eval(line)
            for i in a[1]:
                s = f'{a[0]} - {i}'
                await queue.put(s)

async def main():
    queue = asyncio.Queue(maxsize=10000)

    tasks = []
    for _ in range(10000):
        task = asyncio.create_task(worker(sem, queue))
        tasks.append(task)

    reader_task = asyncio.create_task(reader(queue))

    await reader_task
    await queue.join()

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

asyncio.run(main())
end_time = time.time()
print(end_time-start_time)