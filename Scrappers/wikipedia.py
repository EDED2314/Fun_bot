import aiohttp
from bs4 import BeautifulSoup


class Wikipedia:
    def __init__(self):
        self.string_splitting = []
        self.length = 0

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

    async def get_pagee(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = []
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                header = soup.find("h1", class_="firstHeading mw-first-heading")
                result.append(f"**{str(header.text).upper()}**")
                content = soup.find("div", class_="mw-parser-output")
                try:
                    content_children = content.findChildren()
                except AttributeError:
                    return "No article"

                for content_child in content_children:
                    if content_child.name == "h2" or content_child.name == "p" or content_child.name == "h3" or content_child.name == "ul":
                        if content_child.text != "\n":
                            if content_child.name == "h2":
                                resultt = str(content_child.text)
                                if resultt.endswith("[edit]"):
                                    resultt = resultt.replace("[edit]", "")
                                result.append(f"**{resultt}**")

                            elif content_child.name == "h3":
                                resultt = str(content_child.text)
                                if resultt.endswith("[edit]"):
                                    resultt = resultt.replace("[edit]", "")
                                result.append(f"_**{resultt}**_")

                            elif content_child.name == "p":
                                result.append(content_child.text)

                            elif content_child.name == "ul":
                                children = content_child.findChildren("li", recursive=False)
                                for child in children:
                                    result.append(f"> {child.text}\n")

                copy_result = []
                with open("Scrappers/txts/wikipedia.txt", "w", encoding="utf-8") as f:
                    for item in result:
                        copy_result.append(f"{item}\n")
                    f.writelines(copy_result)

                return result




    async def get_page(self, url: str):
        results = await self.get_pagee(url)
        if results == "No article":
            return [f"**{results} found** 😢"]
        for idx, val in enumerate(results):
            await self.split_until_less_2000(val)
        return self.string_splitting


