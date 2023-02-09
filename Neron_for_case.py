import numpy as np

def sigmond(x):
    return 1 / (1 + np.exp(-x))

weights_for_mes = [[1.7728539],
 [-2.01395774],
 [-1.72881234],
 [-0.53585767],
 [-1.66562046]]

weights_for_news =  [[-1.86089998],
 [ 2.8960713 ],
 [-0.66429168],
 [-0.10340377],
 [-0.66465724]]
weights_for_video = [[-1.8283527 ],
 [-2.89855271],
 [-0.99843655],
 [-0.37912343],
 [ 1.24145097]]
weights_for_shop = [[-3.22875137],
 [-2.81101606],
 [ 2.82397324],
 [ 0.04012507],
 [-2.33260509]]
weights_for_games = [[-1.84162508],
 [-2.89855174],
 [-3.53101274],
 [ 5.23744183],
 [-0.9508684 ]]
def get_state(in_lay):
    a = []
    out = sigmond(np.dot(in_lay, weights_for_mes))
    a.append(out[0])

    out = sigmond(np.dot(in_lay, weights_for_news))
    a.append(out[0])

    #out = sigmond(np.dot(in_lay, weights_for_shop))
    #a.append(out[0])

    # out = sigmond(np.dot(in_lay, weights_for_games))
    # a.append(out[0])

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



