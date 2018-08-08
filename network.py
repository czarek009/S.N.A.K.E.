from keras import Sequential
from keras.layers import Dense
import random
import numpy as np
import string

args = {'n_layers': 1, 
        'n_activation': 'sigmoid',
        'n_neurons': 16,
        'hm_models': 1,
        'input_shape': 6,
        'output_shape': 3}


def generate_networks(args):
    model_pocket = []
    for _ in range(args['hm_models']):
        model = Sequential()
        model.add(Dense(units = args['n_neurons'], input_shape = (1,args['input_shape']), activation = 'sigmoid'))
        model.add(Dense(units = args['output_shape'], activation = 'softmax'))
        #print(model.summary())
        model_pocket.append(model)

    names = []

    for _ in model_pocket:
        name = random.sample(string.ascii_lowercase, 5)
        name = str(name)
        if name not in names:
            names.append(name)

    pack = []

    for i in range(len(names)):
        p = [names[i], model_pocket[i]]
        pack.append(p)

    return pack



if __name__ == '__main__':
    false_input = [0,0,1,0,0,1]
    false_input = np.reshape(false_input, newshape=(1,1,6))
    pack = generate_networks(args)
    network = pack[0][1]
    #print(network.summary())
    prediction = network.predict(false_input)
    print(prediction)
    result = np.argmax(prediction,2)
    print(result)
