from sqlite3.dbapi2 import connect
import numpy as np
import pandas as pd
import random
import math
import matplotlib.pyplot as plt
import sqlite3

suffix_freq = {}
prefix_freq = {}

conn = sqlite3.connect('chat.db')

def main():
    cur = conn.cursor()
    cur.execute("select name from sqlite_master where type = 'table' ")
    #for n in cur.fetchall():
        #print('n ', n)
    messages = pd.read_sql_query("select * from message limit 1200", conn)
    training_data = messages.sample(frac=.7)
    remaining = messages.drop(training_data.index)
    testing = remaining.sample(frac=.66)
    hold_out = remaining.drop(testing)
    

    for col in messages.columns:
        print(col)
    
    text = []
    for index, row in training_data.iterrows():
        if row['text'] is not None:
            #print(row['text'])
            text.append(row['text'])
            for s in row['text'].split():
                count_prefix_suffix(s)

    sum_prefix = 0
    sum_suffix = 0
    weighted_pref_freq = {}
    weighted_suff_freq = {}
    for key in suffix_freq:
        sum_suffix += suffix_freq[key]*len(key)**1.4
    for key in prefix_freq:
        sum_prefix += prefix_freq[key]*len(key)**1.4
    for key in suffix_freq:
        weighted_suff_freq[key] = (suffix_freq[key]*len(key)**1.4)/sum_suffix
    for key in prefix_freq:
        weighted_pref_freq[key] = (prefix_freq[key]*len(key)**1.4)/sum_prefix

    #print('prefix max: ', max(weighted_pref_freq, key=weighted_pref_freq.get))
    #print('suffix max: ', max(weighted_suff_freq, key=weighted_suff_freq.get))
    #print("messages: ", messages)    
    print("Hello and welcome to the M.e Bot ai program trained!")

    model = train_model(text, weighted_pref_freq, weighted_suff_freq)

def word_vector(word, pref_freq, suff_freq):
    vec_len = 8
    vec = []
    if word is None:
        for i in range(vec_len):
            vec.append(0)
        return vec
    #get prefix
    #get suffix
    
    return vec
    

def train_model(text, pref_freq, suff_freq):
    #gosh what structure even???
    #if variable length, how do i actually apply that for a prediction?
    #if we use last_word, word, and sum?
    #make last_word_vec and word_vec
    #calc slope between them?
    #store sorted based on last_word, slope, sum
    #so when predicting, we have generated k words, we pass in word k, sum, and then the slope from last_last_word to last_word
    #word_1 word_2 (last last) word_3 (last) ...
    #  word_k + 1 = gen_word(word_k, word_k-1, sum)
    model = {

    }

    for entry in text:
        last_word = None
        last_word_vec = []
        sum = 0
        for word in entry.split():
            slope = 0
            if last_word in model:
                model[last_word] = model[last_word].append((slope, sum, word))
            else:
                model[last_word] = [(slope, sum, word)]
            

    #training
    #last word = None
    #sum = 0 vector
    #for word in sentence:
    # vectorize last word, word
    #calc slope or delta word - last word

    #model[word] = [(slope_0, sum_0, index_0), ..., (slope_n, sum_n, index_n)]
    #for p in model[word]:
    #   calculate p with closest 


    return [0]

def gen_word(model, word_k, word_k_1, sum):
    slope = word_k_1 - word_k
    #locate the entry in model with data hashed to word_k with the slope and sum closest to out slope and sum

#preprocessing
def count_prefix_suffix(word):
    #gen word vector based off word and last_word
    
    #detect_pref
    word_len = len(word)

    if word_len == 1:
        if word in prefix_freq:
            prefix_freq[word] += 1
        else:
            prefix_freq[word] = 1
        if word in suffix_freq:
            suffix_freq[word] += 1
        else:
            suffix_freq[word] = 1
        return
    

    suffix = ''
    prefix = ''
    for i in range(word_len):
        if word_len - 1 - i > (word_len/2 - 1):
            suffix += word[word_len - 1 - i]
            if suffix in suffix_freq:
                curr = suffix_freq[suffix]
                suffix_freq[suffix] = (curr + 1)
            else:
                suffix_freq[suffix] = 1
        if i < (word_len/2 + 1):
            prefix += word[i]
            if prefix in prefix_freq:
                curr = prefix_freq[prefix]
                prefix_freq[prefix] = (curr + 1)
            else:
                prefix_freq[prefix] = 1


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


    
if __name__ == "__main__":
    main()