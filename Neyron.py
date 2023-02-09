import numpy as np

def sigmond(x):
    return 1 / (1 + np.exp(-x))

# Формат: Mes, News, Shops, Games, Videos
training_inputs = np.array([[5, 0, 0, 0, 0],   #Ватсап
                            [14, 0, 2, 2, 1], #Одноклассники
                            [0, 31, 0, 0, 7], #РИА новости
                            [1, 0, 0, 0, 13], #Ютуб
                            [0, 3, 0, 0, 0],
                            [0, 0, 0, 0, 18], #ТИкток
                            [4, 1, 5, 1, 3], #МФТИ
                            [7, 16, 10, 6, 10],
                            [1, 2, 15, 1, 2], #ЛАМОДА
                            [12, 1, 3, 7, 33],#Какие-то новости
                            [2, 4, 11, 2, 2], #НН магаз
                            [0, 0, 4, 1, 0], #Еще 1 нн магаз
                            [2, 6, 6, 5, 7], # Яндекс Игры
                            [0, 0, 0, 2, 2], #Велкий сайт с играми
                            [1, 0, 2, 7, 2] #НН сайт с играми
                            ])

traning_outputs = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]]).T # Исходы

np.random.seed(1)

s_w = 2 * np.random.random((5, 1)) - 1

print(f"Веса: {s_w}")
in_lay = training_inputs
#out = sigmond(np.dot(in_lay, s_w))
#print(f"Результат\n {out}")
print("\n"
      "\n"
      "\n")
for i in range(2_000_000):
    in_lay = training_inputs
    out = sigmond(np.dot(in_lay, s_w))
    err = traning_outputs - out

    adj = np.dot(in_lay.T, err * (out * (1 - out)))

    s_w = s_w + adj

print(f"Веса после обучения\n {s_w}\n\n\n\n")


out = sigmond(np.dot(training_inputs, s_w))
print("Результат:", out)

