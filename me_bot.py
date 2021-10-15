import numpy as np
import pandas as pd
import random
import math
import matplotlib.pyplot as plt

def main():
    print("Hello and welcome to the M.E. Bot ai program")
    user_input_history = []
    responses = []
    conversation = []
    errors = []
    model_parts = []
    if proceed():
        converse = True
        while converse:
            user_input = get_user_input() #get my input
            user_input_history.append(user_input) #save my input
            resp = gen_resp(model_parts) #get ai resp
            responses.append(resp) #save ai resp
            conversation.append(user_input) #add my response
            conversation.append(resp) #add ai response
            print("AI:", resp) #output the ai response
            err = get_user_error_eval()
            errors.append(err)
            model_parts = train_model(user_input, resp, err, model_parts)
            converse = continue_conversation()
    

def train_model(input, response, error, model):
    return model

def continue_conversation():
    print("keep talking?(y/n)")
    while True:
        cont = input()
        if cont == "y":
            return True
        elif cont == "n":
            return False
        else:
            print("invalid response must be y/n")

def get_user_error_eval():
    print("How appropriate is this response?\nPlease rate on a scale of 0-1000, with 0 being a perfect response and 1000 being completely wrong")
    ask = True
    while ask:
        err = input()
        if err.isnumeric():
            val = int(err)
            if val >= 0 and val <= 1000:
                return val
        print("Invalid response, enter number between 0 and 1000, inclusive")            


def get_user_input():
    print("What would you like to say to the program?")
    return input()

def proceed():
    ask = True
    while(ask):
        print("Would you like to have a conversation?(y/n)")
        answer = input()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            ask = True
    return False

def gen_resp():
    so_far = ""
    w_s = 0
    w_s_prime = 0
    last_char = ''
    start = gen_char(last_char, w_s, w_s_prime)
    rep = repeat(start, w_s, w_s_prime)
    while rep:
        new_char = gen_char(last_char, w_s, w_s_prime)
        so_far += new_char
        rep = repeat(last_char, w_s, w_s_prime)
        w_s_prime = w_s
        w_s += update_w_s(so_far, new_char)

def repeat(last_char_gen, w_eq_s, w_eq_s_prime):
    return False

def update_w_s(output_so_far, char, w_s):
    #think of output as a vector
    vec = []
    i = 0
    for c in output_so_far:
        if i == 40:
            break
        vec.append(int(c))
        i += 1
    while i < 40:
        vec.append[0]

    

def gen_char(last_char_gen, w_eq_s, w_eq_s_prime):
    prediction = 0
    return chr(prediction)

if __name__ == "__main__":
    main()