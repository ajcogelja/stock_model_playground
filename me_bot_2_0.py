import numpy as np
import pandas as pd
import random
import math
import matplotlib.pyplot as plt

def main():
    print("Hello and welcome to the M.e Bot ai program trained!")

suffix_freq = {}
prefix_freq = {}


def process_word(word, last_word, sum):
    #gen word vector based off word and last_word
    
    #detect_pref
    word_len = len(word)
    for i in range(word_len):
        suffix = ''
        prefix = ''
        if max((word_len/2 - 1), 0) < word_len - 1 - i:
            suffix += word[i]
            if suffix_freq.has_key(suffix):
                curr = suffix_freq[suffix]
                suffix_freq[suffix] = (curr + 1)
            else:
                suffix_freq[suffix] = 1
        if i < min((word_len/2 + 1), word_len) :
            prefix += word[i]
            if prefix_freq.has_key(prefix):
                curr = prefix_freq[prefix]
                prefix_freq[prefix] = (curr + 1)
            else:
                prefix_freq[prefix] = 1


    


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



if __name__ == "__main__":
    main()