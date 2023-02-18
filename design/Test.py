from words_count import *
from Bd import *
from  Neron_for_case import get_state
link = input("Введите ссылку\n")
a = get_meta(link=link)
a = counts_info_words(a)
if (a != "Can't connect"):
    f = get_state(a)
    print(f)
else: print("Ошибка, невозможно подключиться к сайту")
add_link_to_bd(link=link, type=f)
print(get_all())