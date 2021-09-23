import asyncio
import re
import aiohttp
import requests as rq
from bs4 import BeautifulSoup as bs
import time
import re

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 YaBrowser/20.8.1.79 Yowser/2.5 Safari/537.36',
    'accept': '*/*'}


def get_data(url):
    response = rq.get(url, headers=HEADERS)
    soup = bs(response.text, "html.parser")
    res = soup.find('table', class_='ws-table-all notranslate')
    final = re.findall(r'>%\w?<', str(res))
    # print("print(".join(map(lambda x: str("x.strftime(\"" + x[1:3] + "\"))\n"), final)))
    return final


async def get_data_async(url, params=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=HEADERS) as response:
            soup = bs(await response.text(), "html.parser")
            try:
                res = soup.find('table', class_='ws-table-all notranslate')
                final = re.findall(r'>%\w?<', str(res))
                print(final)
            except Exception as err:
                print(f'Your error: {err}')
            # print("print(".join(map(lambda x: str("x.strftime(\"" + x[1:3] + "\"))\n"), final)))


async def main():
    tasks = []

    for url in urls:
        task = asyncio.create_task(get_data_async(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    start = time.time()
    urls = ["https://www.w3schools.com/python/python_datetime.asp"]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(time.time() - start)

    start1 = time.time()
    for url in urls:
        print(get_data(url))

    print(time.time() - start1)
