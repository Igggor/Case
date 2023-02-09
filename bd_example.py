import sqlite3

con = sqlite3.connect("tutorial.db") #Отркитие БД
cur = con.cursor() # создание курсора для работы с бд

cur.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT, 
    password TEXT,
    cash BIGINT
)""") #Если такой бд нет, то создаст. Если есть, то скипнет.
con.commit() #Сохранение бд.

user_login = input("ЛОГИН: \n")
user_pass = input("ПАРОЛЬ: \n")

cur.execute("SELECT login FROM users")
#if (cur.fetchone() is None):
  #  cur.execute(f"INSERT INTO users  VALUES (?, ?, ?)", (user_login, user_pass, 0)) #Добавление данных  в таблицу
  #  con.commit()
 #   print("ЗАрегистрированно")
#else: print("Noneeeeee")

cur.execute(f"INSERT INTO users  VALUES (?, ?, ?)", (user_login, user_pass, 0)) #Добавление данных  в таблицу
con.commit()
for value in cur.execute("SELECT * FROM users"):
    print(value) #value - Кортеж, можно получать по индексам, типо value[0]


cur.execute("SELECT count(*) FROM users WHERE user_id = ?", ("QQQ"))#Проверка, есть ли такое значение в бд
info = cur.fetchone()[0]
if info == 0:
    pass
         # выполняем если id нема в базе
else:
    pass
         # выполняем если id есть в баз

#cur.execute("""CREATE TABLE IF NOT EXISTS movie(title, year, score)""") # Создание таблицы moviе, если такая существует, то не создает
