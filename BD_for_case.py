import sqlite3

def add_link_to_bd(link = "", type = "None", info = "None", file = "links.db",  data_base = "links"):

    con = sqlite3.connect(file) #Создание или открытие бд
    cur = con.cursor()
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {data_base} (
                link TEXT, 
                type TEXT,
                info TEXT
            )"""
    )
    con.commit()

    cur.execute(
        f"SELECT count(*) FROM {data_base} WHERE link = ?", (link,))
    is_here = cur.fetchone()[0]
    if is_here == 0:
        cur.execute(f"INSERT INTO {data_base}  VALUES (?, ?, ?)", (link, type, info))  # Добавление данных  в таблицу
        con.commit()
        return "New line added"
        # выполняеся если ссылки нема в базе
    else:
        return "Link is already in bd"
    # выполняется если ссылка есть в базе


def find_link(link = "", data_base = "links", file = "links.db"):
    con = sqlite3.connect(file)
    cur = con.cursor()

    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {data_base} (
                    link TEXT, 
                    type TEXT,
                    info TEXT
                )"""
    )
    con.commit()

    cur.execute(f"SELECT count(*) FROM {data_base} WHERE link = ?", (link,))
    is_here = cur.fetchone()
    print(is_here)

print(add_link_to_bd(link="Igerda"))

find_link(link="Igerda")
