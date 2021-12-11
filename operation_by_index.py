import numpy as np
import pandas as pd
import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def main():
    lower = 0
    upper = 200
    natural_numbers = gen_nats(lower, upper)
    new_set = scramble_nats_2(natural_numbers)
    graph_additions(new_set)

    graph_mult(new_set)
    cont = True
    ###while cont:
    ##    print('lets do some wacky addition! ')
    ##    print('type number 1 to add:\n')
    ##    num_one = int(input())
    ##    print('type number 2 to add:\n')
    ##    num_two = int(input())
    ##    print(num_one, ' + ', num_two, ' = ', new_set[num_one + num_two])
    ##    print('continue?')
    ##    cont_ask = input()
    ##    if len(cont_ask) == 0:
    ###        cont = False
    ###

def graph_additions(scrambled):
    x = []
    y = []
    out = []
    upper = int(len(scrambled)/2) - 1
    for i in range(upper):
        for j in range(upper):
            if scrambled[i] + scrambled[j] < len(scrambled):
                x.append(i)
                y.append(j)
                out.append(scrambled[scrambled[i] + scrambled[j]]) #make this scrambled[i] + scrambled[j], but hard to get domain not to break i guess
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    print('x: ', x, '\ny:', y, '\nz: ', out)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.plot3D(x, y, out, 'green')
    #ax.plot_wireframe(x, y, out, 'green')
    plt.show()

def graph_mult(scrambled):
    x = []
    y = []
    out = []
    upper = len(scrambled)#int(math.sqrt(len(scrambled)))
    for i in range(upper):
        for j in range(upper):
            if scrambled[i] * scrambled[j] < len(scrambled):
                x.append(i)
                y.append(j)
                out.append(scrambled[scrambled[i]*scrambled[j]])
    fig = plt.figure()
    print('x: ', x, '\ny:', y, '\nz: ', out)

    ax = plt.axes(projection='3d')
    ax.plot3D(x, y, out, 'green')#scatter(x, y, out, 'green')
    #ax.plot_wireframe(x, y, out, 'green')
    ax.set_xlabel('$X$', fontsize=20)
    ax.set_ylabel('$Y$')
    plt.show()    

def gen_nats(lower, upper):
    nats = {
    }
    index = 0
    for i in range(int(lower), int(upper)):
        nats[index] = i
        index += 1
    
    return nats

def scramble_nats_1(nats):
    scrambled = {

    }
    shift_index = random.randint(1, len(nats) - 1)
   # shift_val = random.randint(0, len(nats) - 1)
   # this is redundant because we are only offsetting by a constant anyways
   # while shift_index == shift_val:
   #     shift_val = random.randint(0, len(nats) - 1)
    
    #delta = shift_index
    for i in range(0, len(nats)):
        delta = i - shift_index
        if delta < 0:
            delta += len(nats)
        scrambled[i] = delta
    
    #fairly basic shift, then shifted again to create a more stable shift
    double_shift = {

    }

    for i in range(0, len(nats)):
        double_shift[i] = scrambled[scrambled[i]]

    print('double shift: ', double_shift)
    return double_shift

def scramble_nats_2(nats):
    scrambled = {

    }
    used_ind = []
    used_val = []
    for i in range(len(nats)):
        shift_index = random.randint(0, len(nats) - 1)
        shift_val = random.randint(0, len(nats) - 1)
        while shift_index in used_ind:
            shift_index = random.randint(0, len(nats) - 1)
        while shift_val in used_val:
            shift_val = random.randint(0, len(nats) - 1)
        used_ind.append(shift_index)
        used_val.append(shift_val)
        scrambled[shift_index] = shift_val

    print('scrambled: ', scrambled  )
    return scrambled

if __name__ == "__main__":
    main()