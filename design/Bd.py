import sqlite3

def add_link_to_bd(link = "", type = "None", info = "None", file = "links.db",  data_base = "links"): #Добавление ссылки в бд

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


def find_link(type = "", data_base = "links", file = "links.db"): #Получение массива ссылок по определенному тегу.
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

    cur.execute(f"SELECT count(*) FROM {data_base} WHERE type = ?", (type,))
    is_here = cur.fetchone()[0]
    #print(is_here)
    if is_here == 0:
        return "No links whis this type"
    else:
        cur.execute(f"SELECT link FROM {data_base} WHERE type = ?", (type,)) # поиск ссылок по типу
        a = []
        for result in cur.fetchall():
            a.append(result[0]) # добавление ссылок в массив
        return a

def get_all(data_base = "links", file = "links.db"):
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
    cur.execute(f"SELECT link, type, info FROM {data_base}")
    mass = cur.fetchall()
    return mass

def is_link_in_bd(link = "", file = "links.db",  data_base = "links"): #Проверка, есть ли такая ссылка в базе данных
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
    return cur.fetchone()[0]

def get_link(link = "", file = "links.db",  data_base = "links"): #Проверка, есть ли такая ссылка в базе данных
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
    cur.execute(f"SELECT link, type, info FROM {data_base} WHERE link = ?", (link,))
    return cur.fetchone()
def clear_bd(link = "", file = "links.db",  data_base = "links"):
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
    if (link == ""):
        cur.execute(f"DELETE FROM {data_base};")
        con.commit()
    else:
        cur.execute(
            f"SELECT count(*) FROM {data_base} WHERE link = ?", (link,))
        is_here = cur.fetchone()[0]
        if is_here != 0:
            cur.execute(f"DELETE FROM {data_base} WHERE link='{link}';")
            con.commit()
