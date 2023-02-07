import numpy as np

def sigmond(x):
    return 1 / (1 + np.exp(-x))

training_inputs = np.array([[0, 0, 1, 0, 0],
                            [1, 1, 1, 0, 0],
                            [1, 0, 1, 0, 0],
                            [0, 1, 1, 0, 0],
                            [0, 0, 0, 0, 0]])

traning_outputs = np.array([[0, 1, 1, 0, 0]]).T

np.random.seed(1)

s_w = 2 * np.random.random((5, 1)) - 1

print(f"Веса: {s_w}")
in_lay = training_inputs
out = sigmond(np.dot(in_lay, s_w))
print(f"Результат\n {out}")
print("\n"
      "\n"
      "\n")
for i in range(200_000):
    in_lay = training_inputs
    out = sigmond(np.dot(in_lay, s_w))
    err = traning_outputs - out

    adj = np.dot(in_lay.T, err * (out * (1 - out)))

    s_w = s_w + adj

print(f"Веса после обучения {s_w}")



new = np.array([1, 1, 0, 0, 0])
out = sigmond(np.dot(new, s_w))

print(f"Новая ситуация \n {out}")

new = np.array([1, 1, 1, 0, 0])
out = sigmond(np.dot(new, s_w))

print(f"Новая ситуация \n {out}")
