from bs4 import BeautifulSoup as bs
from requests import get
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from Words import words
def get_meta(link = r"https://vk.com"):
    headers={"User-Agent":"Mozilla/5.0"}

    href = get(link, headers=headers).text
    s = ""
    soup = bs(href, 'lxml')
    # meta = soup.find("meta", name="title")
    try:
        meta = soup.title.text
        s += meta.lower().strip() + " "
    except Exception as ex:
        pass
        #print("заголовок не найден")
        #print(ex)
   # print(meta.strip())


    try:
        description = soup.find("meta", attrs={"name": "description"})["content"]
        s += (description + " ").lower()
    except Exception as ex:
        try:
            description = soup.find("meta", attrs={"name": "Description"})["content"]
            s += (description + " ").lower()
        except Exception as e:
            pass
            #print("Описание не найдено")
            #print(ex, e)
    try:
        keywords = soup.find("meta", attrs={"name": "keywords"})["content"]
        s += keywords.lower().strip() + " "
    except Exception as ex:
        try:
            keywords = soup.find("meta", attrs={"name": "Keywords"})["content"]
            s += keywords.lower().strip() + " "
        except:
            pass
            #print("Ключевые слова не найдены")
            #print(ex)
    s = s.replace(" и ", " ")
    s = s.replace("|", " ")
    s = s.replace("–", " ")
    s = s.replace("-", " ")
    s = s.replace(" в ", " ")
    s = s.replace(" на ", " ")
    s = s.replace(" с ", " ")
    s = s.replace(" под ", " ")
    s = s.replace(" за ", " ")
    s = s.replace(" для ", " ")
    s = s.replace(" мы ", " ")
    #print(s)
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

    cgames = 0
    for i in range(len(a)):
        mes = process.extract(a[i], words["games"])
        for j in mes:
            if (j[1] > 80): cgames += 1
    cvid = 0
    for i in range(len(a)):
        mes = process.extract(a[i], words["videos"])
        for j in mes:
            if (j[1] > 80): cvid += 1
    output = [cmes, cnews, cshop, cgames, cvid]
    #print(output)
    if (max(output) == 0): return "Can't connect"
    return output
    #print(f"Mes: {cmes} \nNews: {cnews}\nShops: {cshop}\nGames {cgames}\nVideos {cvid}")




#print(counts_info_words(get_meta("https://www.igrixl.ru/")))