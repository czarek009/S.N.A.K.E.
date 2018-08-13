from queue import Queue
import threading
from silent_net_snake import playing_game
from network import generate_networks, args
from keras.models import load_model
import numpy as np

args2 = {'hm_threads': 1}

q = Queue()

def exampleJob(name):
    print(name)
    name = str(name)
    game_result = playing_game(name,100)
    save_lock = threading.Lock()
    with save_lock:
        with open('/results_log/log.txt', 'a') as f:
            line = str(name)+':::'+str(game_result)+'\n'
            f.write(line)

def threader():
    while True:
        # gets an worker from the queue
        pack = q.get()

        # Run the example job with the avail worker in queue (thread)
        exampleJob(pack)

        # completed with the job
        q.task_done()

def threads(args_dict):

    names = generate_networks(args)
    print(names)
    
    for _ in range(args_dict['hm_threads']):
        t = threading.Thread(target= threader)
        t.daemon = True
        t.start()

    for i in names:
        q.put(i)

    q.join()

if __name__ == '__main__':
    threads(args2)