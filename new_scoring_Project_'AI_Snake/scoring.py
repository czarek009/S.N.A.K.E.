from queue import Queue
import threading
from silent_net_snake import playing_game
from keras.models import load_model
import numpy as np

def scoring(names):

    with open('results_log/log.txt','w') as f:
        f.write('')

    for name in names:
        score = playing_game(name, 100)
        name = name.split('/')[1]
        name = name.split('.')[0]
        line = str(name)+':::'+str(score)+'\n'
        with open('results_log/log.txt','a') as f:
            f.write(line)

'''
if __name__ == '__main__':
    scoring()
'''