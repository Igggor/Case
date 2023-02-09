from words_count import *
from  Neron_for_case import get_state
link = input("Введите ссылку\n")
a = get_meta(link=link)
a = counts_info_words(a)
if (a != "Can't connect"):
    print(get_state(a))
else: print("Ошибка, невозможно подключиться к сайту")
