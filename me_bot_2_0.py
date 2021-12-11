import numpy as np
import pandas as pd
import random
import math
import matplotlib.pyplot as plt

def main():
    print("Hello and welcome to the M.e Bot ai program trained!")
   
    


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