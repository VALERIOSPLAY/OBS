import fake_useragent as ua
import time
import ast
import aiohttp
from rapidfuzz import fuzz
import asyncio
import tqdm
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from lxml import html


check_queue = multiprocessing.Queue()

def initialize_process(proxies, queries):

    headers = {"User-Agent": str(ua.UserAgent.random)}
    clients = {}
    proxy_queue = proxies

    def decision(res, request):
        if res != []:
            # fs_time = time.time()
            with ThreadPoolExecutor() as executor:
                fzr = list(executor.map(lambda i: fuzz.token_sort_ratio(i, request), res[:6]))
            top3 = sorted(fzr, reverse=True)[:3]
            avg = sum(top3[i] * (3 - i) for i in range(3)) / 6  # weighted average
            if avg >= 65:
                print(f'Доверенный источник {avg}, for {request}')
            elif avg > 50 and avg < 65:
                print(f'Есть сомнения {avg}, for {request}')
            else:
                print(f'Сомнительная книга {avg}')
            # print(f'compare time is {time.time()-fs_time}')

    async def hx_request(session, query, proxy):
        print(f' Requesting {query} with proxy {proxy}')
        async with session.get(f"https://www.bing.com/search?q={query}", proxy=proxy, headers=headers) as response:
            html_content = await response.text()
            #stime = time.time()
            parsed = html.fromstring(html_content)
            titles = parsed.xpath('//li[@class="b_algo"]//h2/a/text()')
            #print(f'parse time is {time.time() - stime}')
            return titles


    start_time = time.time()

    async def process_query(session, query):  # Добавляем сессию в качестве аргумента
        proxy = await proxy_queue.get()
        try:
            results = await hx_request(session, query, proxy)
            check_queue.put_nowait([results, query])
            decision(results, query)
            proxy_queue.put_nowait(proxy)  # Возвращаем прокси в очередь
        except Exception as e:
            print(f"Error with proxy {proxy}: {e}")


    async def main(batch):
        connector = aiohttp.TCPConnector(limit=100)
        timeout=aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = [process_query(session, query) for query in batch]
            await asyncio.gather(*tasks)



    asyncio.run(main(queries))

    print(time.time()-start_time)

def sep_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


if __name__ == '__main__':
    with open("proxies.txt","rt", encoding="utf-8") as pr:
        proxy_list=[f"http://{proxy.strip()}" for proxy in pr]
        divided_proxy_list = sep_list(proxy_list, 4)
        proxy_queues = [asyncio.Queue() for _ in range(4)]
        for i in range(4):
            for proxy in divided_proxy_list[i]:
                proxy_queues[i].put_nowait(proxy)


    full_text = []
    with open('out1.txt', 'rt', encoding='utf-8') as f:
        for counter, line in enumerate(tqdm.tqdm(f, desc='books formed'), start=1):
            a = ast.literal_eval(line)
            for i in a[1]:
                s = f'{a[0]} - {i}'
                full_text.append(s)


    cnt=0
    text_parts = sep_list(full_text,4)
    processes = []
    for i in range(4):
        p = multiprocessing.Process(target=initialize_process, args=(proxy_queues[i], text_parts[i]))
        p.start()
        processes.append(p)


    for p in processes:
        p.join()