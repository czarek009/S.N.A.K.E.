from keras import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
from keras.models import load_model
import random
import numpy as np
import string
import os
import operator
from scoring import scoring
from shutil import copyfile
import gc

args = {'n_layers': 1, 
        'n_activation': 'sigmoid',
        'n_neurons': 64,
        'hm_models': 50,
        'input_shape': 6,
        'output_shape': 3,
        'top_best':3,
        'total_survivors':6,
        'mutation_chance':0.05}

def generate_networks(args = args):

    folder = 'weights/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    model_pocket = []
    for _ in range(args['hm_models']):
        model = Sequential()
        model.add(Dense(units = args['n_neurons'], input_shape = (1,args['input_shape']), activation = 'sigmoid'))
        model.add(Dense(args['output_shape']))
        sgd= SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='mse', optimizer=sgd)
        model_pocket.append(model)

    names = []

    for _ in model_pocket:
        name = random.sample(string.ascii_lowercase, 5)
        name = ''.join(name)

        if name in names:
            while name in names:
                name = random.sample(string.ascii_lowercase, 5)
                name = ''.join(name)

        names.append(name)

    paths = []

    for i in range(len(names)):
        path = 'weights/'+str(names[i])+'.h5'
        paths.append(path)
        model_pocket[i].save(path)

    return paths

def selection():

    surv = []
    folder = 'weights/'
    surv_folder = 'survivors/'

    for the_file in os.listdir(surv_folder):
        file_path = os.path.join(surv_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

    with open('results_log/log.txt', 'r') as text_file:
        for line in text_file:
            line = str(line)
            name, score = line.split(':::')
            score = int(score)
            surv.append([name,score])

    surv.sort(key=lambda x: x[1], reverse = True)
    survivors = surv[:args['top_best']]

    current_hottness = survivors[0][0]
    current_hottness_score = survivors[0][1]
    old_hottness_score = 0

    with open('current_hottness/hottness_score.txt','r') as f:
        for line in f:
            old_hottness_score = int(line)

    if current_hottness_score >= old_hottness_score:
        for the_file in os.listdir('current_hottness/'):
            file_path = os.path.join('current_hottness/', the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

        current_hottness_path = 'current_hottness/'+str(current_hottness)+'.h5'
        current_hottness_old = 'weights/'+str(current_hottness)+'.h5'
        copyfile(current_hottness_old, current_hottness_path)

        with open('current_hottness/hottness_score.txt','w') as f:
            f.write(str(current_hottness_score))



    while len(survivors)<args['total_survivors']:
        candidate = random.choice(surv)
        if candidate not in survivors:
            survivors.append(candidate)
    
    survivors_names = ['weights/'+str(i[0])+'.h5' for i in survivors]


    for candidate in os.listdir(folder):
        #print (candidate)
        candidate_path = os.path.join(folder, candidate)
        if candidate_path in survivors_names:
            new_path = os.path.join(surv_folder, candidate)
            copyfile(candidate_path, new_path)

    #print(survivors_names)

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path) and file_path not in survivors_names:
                #print(file_path)
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def mutator(subject):

    if random.random() < args['mutation_chance']:
        mutated_gene = random.randint(0,len(subject)-1)
        subject[mutated_gene] = subject[mutated_gene]*random.uniform(0,2)

    return subject

def procreation(parent1, parent2):
    parent1 = str(parent1)
    parent2 = str(parent2)

    model1 = load_model(parent1)
    model2 = load_model(parent2)

    child_model1 = model1
    child_model2 = model2

    weights1 = model1.get_weights()
    weights2 = model2.get_weights()

    new_weights1 = weights1
    new_weights2 = weights2

    split_point_1 = random.randint(0,len(new_weights1[0])-1)
    split_point_2 = random.randint(0,len(new_weights1[1])-1)

    new_weights1[0] = np.concatenate((weights1[0][:split_point_1],weights2[0][split_point_1:]), axis=0)
    new_weights2[0] = np.concatenate((weights2[0][:split_point_1],weights1[0][split_point_1:]), axis=0)
    new_weights1[0] = mutator(new_weights1[0])
    new_weights2[0] = mutator(new_weights2[0])
    new_weights1[1] = np.concatenate((weights1[1][:split_point_2],weights2[1][split_point_2:]), axis=0)
    new_weights2[1] = np.concatenate((weights2[1][:split_point_2],weights1[1][split_point_2:]), axis=0)
    new_weights1[1] = mutator(new_weights1[1])
    new_weights2[1] = mutator(new_weights2[1])

    child_model1.set_weights(new_weights1)
    child_model2.set_weights(new_weights2)

    return child_model1, child_model2

def repopulate():
    current_population = args['total_survivors']

    survivors_names = []
    population_names = []
    folder = 'weights/'
    surv_folder = 'survivors/'

    for the_file in os.listdir(surv_folder):
        file_path = os.path.join(surv_folder, the_file)
        population_path = os.path.join(folder, the_file)
        #print(file_path)
        #print(population_path)
        survivors_names.append(file_path)
        population_names.append(population_path)

    while current_population < args['hm_models']:
        parent1 = random.choice(survivors_names)
        parent2 = random.choice(survivors_names)
        while parent2 == parent1:
            parent2 = random.choice(survivors_names)
        
        child1,child2 = procreation(parent1, parent2)

        child1_name, child2_name = ''.join(random.sample(string.ascii_lowercase, 5)), ''.join(random.sample(string.ascii_lowercase, 5))
        child1_name, child2_name = os.path.join(folder, child1_name), os.path.join(folder, child2_name)
        child1_name, child2_name  = str(child1_name)+'.h5', str(child2_name)+'.h5'
        #print(child1_name)
        #print(child2_name)
        while child1_name in population_names or child2_name in population_names:
            child1_name, child2_name = ''.join(random.sample(string.ascii_lowercase, 5)), ''.join(random.sample(string.ascii_lowercase, 5))
            child1_name, child2_name = os.path.join(folder, child1_name), os.path.join(folder, child2_name)
            child1_name, child2_name  = str(child1_name)+'.h5', str(child2_name)+'.h5'

        population_names.append(child1_name)
        population_names.append(child2_name)

        child1.save(child1_name)
        child2.save(child2_name)

        current_population+=2

    return population_names

def genetics():
    names = generate_networks(args)
    counter = 1
    print('New population created')
    while True:
        gc.collect()
        scoring(names)
        selection()
        names = repopulate()
        print('Generation passed: '+str(counter))
        counter+=1

def restore():
    names = []
    counter = 1
    print('Genes restored')
    while True:
        names = repopulate()
        scoring(names)
        selection()
        gc.collect()
        print('Generation passed (this session): '+str(counter))
        counter+=1

if __name__ == '__main__':

    if os.listdir('survivors/')==[]:
        genetics()
    else:
        restore()