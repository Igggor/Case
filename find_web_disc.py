from bs4 import BeautifulSoup as bs
from requests import get
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
words = {
    "messenger":["вконтакте", "одноклассники", "общение", "друзья", "контакт", "сообщения", "социальная", "сеть", "отправляйте", "получайте", "сообщения", "whatsapp", "send", "receive", "messages"],
    "news" : ["новости", "события", "москве", "россии", "мире", "сегодня", "дня", "оперативная", "информация", "событий", "радиоэфир", "последние", "темы", "статьи"],
    "shops" : ["магазин", "купить", "цена", "интернет-магазин", "ассортимент", "товары", "доставка", "бренд", "техника", "маркет", "покупки", "скидки", "акции", "кешбек", "авито", "продать"]
}

def get_meta(link = r"https://vk.com"):
    href = get(link).text
    s = ""
    soup = bs(href, 'lxml')
    # meta = soup.find("meta", name="title")
    try:
        meta = soup.title.text
        s += meta.lower().strip() + " "
    except Exception as ex:
        print("заголовок не найден")
        print(ex)
   # print(meta.strip())


    try:
        description = soup.find("meta", attrs={"name": "description"})["content"]

        if (description):
            s += (description + " ").lower()
    except Exception as ex:
        try:
            description = soup.find("meta", attrs={"name": "description"})["content"]
            if (description):
                s += (description + " ").lower()
        except Exception as e:
            print("Описание не найдено")
            print(ex, e)
    try:
        keywords = soup.find("meta", attrs={"name": "keywords"})["content"]
        s += keywords.lower().strip() + " "
    except Exception as ex:
        print("Ключевые слова не найдены")
        print(ex)
    s = s.replace(" и ", " ")
    s = s.replace(" в ", " ")
    s = s.replace(" на ", " ")
    s = s.replace(" с ", " ")
    s = s.replace(" под ", " ")
    s = s.replace(" за ", " ")
    s = s.replace(" для ", " ")
    s = s.replace(" мы ", " ")
    print(s)
    return (s)

def counts_info_words(s):
    s = s.split()
    a = s
    cmes = 0
    for el in s:
        mes = process.extract(el, words["messenger"])
        for i in mes:
            if (i[1] > 80): cmes += 1

    cnews = 0
    for i in range(len(a)):
        mes = process.extract(a[i], words["news"])
        for j in mes:
            if(j[1] > 80): cnews += 1
    cshop = 0
    for i in range(len(a)):
        mes = process.extract(a[i], words["shops"])
        for j in mes:
            if(j[1] > 80): cshop += 1
    print(f"mes: {cmes} \nnews: {cnews}\nshops: {cshop}")




print(counts_info_words(get_meta("https://www.youtube.com/watch?v=7hn1_t2ZtJQ")))
