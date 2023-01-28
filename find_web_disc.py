from bs4 import BeautifulSoup as bs
from requests import get

def get_meta(link = r"https://vk.com"):
    href = get(link).text
    s = ""
    soup = bs(href, 'html.parser')
    # meta = soup.find("meta", name="title")
    meta = soup.title.string
   # print(meta.strip())
    s += meta.lower().strip()

    description = soup.find("meta", attrs={"name": "description"}).get("content")
    if (description):
        s += description
    return (s)
