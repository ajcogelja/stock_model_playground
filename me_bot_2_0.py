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
    for n in cur.fetchall():
        print('n ', n)
    messages = pd.read_sql_query("select * from message limit 800", conn)
    for col in messages.columns:
        print(col)
    
    text = []
    for index, row in messages.iterrows():
        if row['text'] is not None:
            print(row['text'])
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

    print('prefix max: ', max(weighted_pref_freq, key=weighted_pref_freq.get))
    print('suffix max: ', max(weighted_suff_freq, key=weighted_suff_freq.get))
    #print("messages: ", messages)
    print("Hello and welcome to the M.e Bot ai program trained!")



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