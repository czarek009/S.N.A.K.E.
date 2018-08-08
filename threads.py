from queue import Queue
import threading
from silent_net_snake import playing_game
from network import generate_networks, args
import numpy as np

args2 = {'hm_threads': 1}

q = Queue()

def exampleJob(pack):

    name = pack[0]
    network = pack[1]
    print('!!!!!!')
    false_input = [0,0,1,0,0,1]
    false_input = np.reshape(false_input, newshape=(1,1,6))
    pack = generate_networks(args)
    #print(network.summary())
    prediction = network.predict(false_input)
    print(prediction)
    result = np.argmax(prediction,2)
    print(result)

    game_result = playing_game(network,100)
    print('--------------------')
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

    netw_to_do = generate_networks(args)
    
    for _ in range(args_dict['hm_threads']):
        t = threading.Thread(target= threader)
        t.daemon = True
        t.start()

    for i in netw_to_do:
        q.put(i)

    q.join()

if __name__ == '__main__':
    threads(args2)
