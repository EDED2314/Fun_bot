from requests_html import AsyncHTMLSession
import asyncio
import time

'''
urls = []
for x in range(1,50):
    urls.append(f"http://books.toscrape.com/catalogue/page-{x}.html")

async def work(s, url):
    r = await s.get(url)
    products = []
    desc = r.html.find('article.product_pod')
    for item in desc:
        product = {
            'title': item.find('h3 a[title]', first=True).text,
            'price': item.find('p.price_color', first=True).text
        }
        products.append(product)
    return products

async def main(urls):
    s = AsyncHTMLSession()
    tasks = (work(s, url) for url in urls)
    x = await asyncio.gather(*tasks)
    return x

results = asyncio.run(main(urls))
print(results)
'''


# noinspection PyTypeChecker
class Wikipedia:
    def __init__(self):
        self.string_splitting = []
        self.header2s = []
        self.header3s = []

    async def split_until_less_2000(self, string1: str, string2: str = None):
        if string2 is None:
            if len(string1) > 2000:
                string2 = string1[:2000]
                string1 = string1[2000:]
                return await self.split_until_less_2000(string1, string2)
            else:
                self.string_splitting.append(string1)
        if string2 is not None:
            # lst = []
            if len(string1) > 2000:
                string_2 = string1[:2000]
                string_1 = string1[2000:]
                return await self.split_until_less_2000(string_1, string_2)
                # lst.append(string_1)
                # lst.append(string_2)
            if len(string2) > 2000:
                string_3 = string2[:2000]
                string_4 = string2[2000:]
                return await self.split_until_less_2000(string_3, string_4)
                # lst.append(string_3)
                # lst.append(string_4)
            if len(string1) <= 2000:
                self.string_splitting.append(string1)
            if len(string2) <= 2000:
                self.string_splitting.append(string2)

    async def get_page(self, url):
        results = await self.run_thingy(url)
        # print(results)
        for idx, val in enumerate(results[0]):
            await self.split_until_less_2000(val)
        # print(self.string_splitting)
        return self.string_splitting

    async def work(self, s, url):
        r = await s.get(url)
        textt = ""
        desc = []
        for item in r.html.find('div.mw-body'):
            x = str(item.find('h1')[0].text)
            desc.append(f"**{x.upper()}**")
        for idx, item in enumerate(r.html.find('div.mw-parser-output')):
            print(item.text[:4000])
            paragraphs = item.find('p')
            # paragprahs is a list

            self.header2s = []
            self.header3s = []
            header2s = item.find('h2')
            header3s = item.find('h3')
            for itemh2 in header2s:
                self.header2s.append(itemh2.text)

            for itemh3 in header3s:
                self.header3s.append(itemh3.text)

            header2s = self.header2s
            header3s = self.header3s

            for idxx, val in enumerate(paragraphs):
                if len(val.text) != 0:
                    big_textt = str(item.text)
                    big_text_array = big_textt.split("\n")
                    shortened_big_text_array = []

                    # print(big_text_array)

                    for paragraph in big_text_array:
                        # print(len(paragraph))
                        if len(paragraph) < 20:
                            shortened_big_text_array.append(paragraph)

                    # print(shortened_big_text_array)

                    for itemmm in shortened_big_text_array:
                        for item2 in header2s:
                            if str(itemmm) == str(item2):
                                desc.append(f"**{itemmm}**")
                                header2s.remove(itemmm)
                                shortened_big_text_array.remove(itemmm)
                                break
                        for item3 in header3s:
                            if itemmm == str(item3):
                                # header 3??
                                desc.append(f"_**{itemmm}**_")
                                header3s.remove(itemmm)
                                shortened_big_text_array.remove(itemmm)
                                break

                    desc.append(val.text)
                '''
                if len(val.text) != 0:
                    if val.text in item.text:
                        big_text = str(item.text)
                        index = big_text.index(val.text)
                        print(index)
                        new_space_count = 0
                        current_indx = index
                        while 0 <= new_space_count < 2:
                            current_indx -= 1
                            if big_text[current_indx] == "\n":
                                new_space_count += 1

                        print(big_text[current_indx])
                        first_letter = current_indx

                        new_space_count = 0
                        random_str = ""
                        while new_space_count != 1:
                            first_letter += 1
                            random_str += str(big_text[first_letter])
                            if big_text[first_letter] == "\n":
                                new_space_count += 1
                        print(random_str)
                        for item2 in header2s:
                            if random_str == str(item2):
                                # header 2???
                                desc.append(f"**{random_str}**")
                        for item3 in header3s:
                            if random_str == str(item3):
                                # header 3??
                                desc.append(f"_**{random_str}**_")
                    '''
                # e

        # print(desc)
        return desc

    async def run_thingy(self, url):
        s = AsyncHTMLSession()
        tasks = (self.work(s, url))
        x = await asyncio.gather(tasks)
        return x
