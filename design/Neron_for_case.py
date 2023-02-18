import numpy as np

def sigmond(x):
    return 1 / (1 + np.exp(-x))

weights_for_mes = [[ 3.88105321],
 [-2.81334491],
 [-2.36816253],
 [-1.64470656],
 [-2.63580266]]

weights_for_news =  [[-3.97306201],
 [ 2.7839932 ],
 [-2.37905604],
 [-2.25493282],
 [-2.59028626]]

weights_for_video = [[-1.8283527 ],
 [-2.89855271],
 [-0.99843655],
 [-0.37912343],
 [ 1.24145097]]
weights_for_shop = [[-4.29257611],
 [-2.73707569],
 [ 3.40345098],
 [-0.53550175],
 [-3.91111886]]

weights_for_games = [[-4.20347251],
 [-2.89961195],
 [-3.20476937],
 [ 4.39985226],
 [-0.49344799]]


def get_state(in_lay):
    a = []
    out = sigmond(np.dot(in_lay, weights_for_mes))
    a.append(out[0])

    out = sigmond(np.dot(in_lay, weights_for_news))
    a.append(out[0])

    out = sigmond(np.dot(in_lay, weights_for_shop))
    a.append(out[0])

    out = sigmond(np.dot(in_lay, weights_for_games))
    a.append(out[0])

    out = sigmond(np.dot(in_lay, weights_for_video))
    a.append(out[0])
    #print(*a)
    maxi = a.index(max(a))
    if (a[maxi]  < 0.8): return "else"
    if(maxi == 0): return "mes"
    if (maxi == 1): return "news"
    if (maxi == 2): return "shop"
    if (maxi == 3): return "games"
    if (maxi == 4): return "video"



