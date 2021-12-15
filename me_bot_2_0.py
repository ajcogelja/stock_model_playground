
from sqlite3.dbapi2 import connect
from typing import cast
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
    messages = pd.read_sql_query("select * from message limit 2500", conn)
    training_data = messages.sample(frac=.7)
    remaining = messages.drop(training_data.index)
    testing = remaining.sample(frac=.66)
    hold_out = remaining.drop(testing.index)
    

    #for col in messages.columns:
    #    print(col)
    
    text = []
    for index, row in training_data.iterrows():
        if row['text'] is not None:
            text.append(row['text'].lower())

    
    for index, row in messages.iterrows():
        if row['text'] is not None:
            #text.append(row['text'])
            for s in row['text'].split(' '):
                count_prefix_suffix(s.lower())

    sum_prefix = 0
    sum_suffix = 0
    weighted_pref_freq = {}
    weighted_suff_freq = {}
    for key in suffix_freq.keys():
        sum_suffix += suffix_freq[key]*len(key)**1.4
    for key in prefix_freq.keys():
        sum_prefix += prefix_freq[key]*len(key)**1.4
    for key in suffix_freq.keys():
        weighted_suff_freq[key] = (suffix_freq[key]*len(key)**1.4)/sum_suffix
    for key in prefix_freq.keys():
        weighted_pref_freq[key] = (prefix_freq[key]*len(key)**1.4)/sum_prefix

    #print('prefix max: ', max(weighted_pref_freq, key=weighted_pref_freq.get))
    #print('suffix max: ', max(weighted_suff_freq, key=weighted_suff_freq.get))
    #print("messages: ", messages)    
    #print("Hello and welcome to the M.e Bot ai program trained!")

    model = train_model(text, weighted_pref_freq, weighted_suff_freq)

    print(model.keys())
    ask_phase = True
    while ask_phase:
        not_found = True
        index = 1
        print('Enter a word and me bot will suggest a follow up')
        word = ""
        last_word = None
        last_vec = word_vector(last_word, None, None, 0, 0)
        last_slope = last_vec
        sentence = ""

        while not_found:
            word = input().lower()
            if word in model.keys():
                not_found = False
            else:
                print("word: ", word, ' not found. Enter another: ')
                #word = input()

        sentence += word

        word_vec = word_vector(word, weighted_pref_freq, weighted_suff_freq, 1, 2)
        slope = calc_slope(word_vec, last_vec, index)
        output = gen_word(model, word, word_vec, word_vec, index)
        #(best_tuple_0, min_tuple_dist_0 ,best_tuple_1, min_tuple_dist_1)
        #print('me bots best two tuples under different metrics: ', output)
        preferred_tuple = output[0]
        next_word = preferred_tuple[4]
        last_slope = slope
        last_vec = word_vec
        index += 1
        while next_word in model.keys() and index < 20:
            word = next_word
            sentence += ' ' + word
            word_vec = word_vector(word, weighted_pref_freq, weighted_suff_freq, 1, 2)
            slope = calc_slope(word_vec, last_vec, index)
            output = gen_word(model, word, word_vec, word_vec, index)
            #(best_tuple_0, min_tuple_dist_0 ,best_tuple_1, min_tuple_dist_1)
            #print('me bots best two tuples under different metrics: ', output)
            preferred_tuple = output[0]
            next_word = preferred_tuple[4]
            last_slope = slope
            last_vec = word_vec
            index += 1

        sentence += ' ' + next_word

        print('sentence: ', sentence)

        #((0: slope, 1: sum, 2: index, 3: float(index/max_length), 4: next_word,  5: last_word_vec, 6: last_slope))
        print('ask again? (y/n)')
        repeat_str = input()
        if repeat_str.lower() != 'y':
            ask_phase = False
    print('thanks for using me bot! Cya')


#todo
def word_vector(word, pref_freq, suff_freq, index, sentence_length):
    vec_len = 9
    max_traces = 12
    vec = []
    if word is None:
        for i in range(vec_len):
            vec.append(0)
        return vec
    #p_0 prefix val
    #p_1 suffix val
    #p_2 count of punctuation
    #p_3 sum of letters
    #p_4 index of max_pref_freq
    #p_5 index of max_suff_freq
    #p_6 length
    #p_7 index
    #p_8 relative index/percentage
    
    #collect all data points
    prefix_tuple = calc_pref(word.lower(), pref_freq)
    suffix_tuple = calc_suff(word.lower(), suff_freq)
    punc_count = count_punct(word)
    word_sum = sum_word(word)
    word_traces = gen_traces(word, max_traces)
    trace_tuple = process_traces(word_traces)
    #trace tuple contains: 
    """
    return (
    float(avg_sum/sum_terms),
    float(word_averages/count_of_traces),
    max_avg_poly_delta, min_avg_poly_delta, 
    max_root_avg_poly_delta, min_root_avg_poly_delta,
    max_avg_linear_delta, min_avg_linear_delta,
    max_root_avg_linear_delta, min_root_avg_linear_delta,
    )"""
    #add all to vector
    vec.append(prefix_tuple[1])
    vec.append(suffix_tuple[1])
    vec.append(punc_count)
    vec.append(word_sum)
    vec.append(len(prefix_tuple[0]))
    vec.append(len(suffix_tuple[0]))
    vec.append(len(word))
    vec.append(index)
    vec.append(index/sentence_length)
    
    return vec

def process_traces(traces):
    max_avg_poly_delta = -float('inf')
    min_avg_poly_delta = float('inf')
    max_avg_linear_delta = -float('inf')
    min_avg_linear_delta = float('inf')
    max_root_avg_poly_delta = -float('inf')
    min_root_avg_poly_delta = float('inf')
    max_root_avg_linear_delta = -float('inf')
    min_root_avg_linear_delta = float('inf')
    sum_terms = 0
    avg_sum = 0
    word_averages = 0
    count_of_traces = 0
    for trace in traces:
        trace_sum = 0
        linear_trace_deltas = []
        poly_trace_deltas = []
        last_letter_val = 0
        for w in trace:
            letter_val = ord(w)
            trace_sum += letter_val
            delta = letter_val - last_letter_val
            linear_trace_deltas.append(delta)
            poly_trace_deltas.append(delta**2)
            last_letter_val = letter_val
        word_averages += float(trace_sum/len(trace))
        count_of_traces += 1
        avg_sum += trace_sum
        sum_terms += len(trace)
        avg_lin_delta = sum(linear_trace_deltas)/len(linear_trace_deltas)
        avg_poly_delta = sum(poly_trace_deltas)/len(poly_trace_deltas)
        avg_root_lin_delta = avg_lin_delta**.5
        avg_root_poly_delta = avg_poly_delta**.5
        if avg_poly_delta > max_avg_poly_delta:
            max_avg_poly_delta = avg_poly_delta
        if avg_poly_delta < min_avg_poly_delta:
            min_avg_poly_delta = avg_poly_delta
        if avg_lin_delta > max_avg_linear_delta:
            max_avg_linear_delta = avg_lin_delta
        if avg_lin_delta > min_avg_linear_delta:
            min_avg_linear_delta = avg_lin_delta
        if avg_root_poly_delta > max_root_avg_poly_delta:
            max_root_avg_poly_delta = avg_root_poly_delta
        if avg_root_poly_delta < min_root_avg_poly_delta:
            min_root_avg_poly_delta = avg_root_poly_delta
        if avg_root_lin_delta > max_root_avg_linear_delta:
            max_root_avg_linear_delta = avg_root_lin_delta
        if avg_root_lin_delta > min_root_avg_linear_delta:
            min_root_avg_linear_delta = avg_root_lin_delta    
    

    return (
    float(avg_sum/sum_terms),
    float(word_averages/count_of_traces),
    max_avg_poly_delta, min_avg_poly_delta, 
    max_root_avg_poly_delta, min_root_avg_poly_delta,
    max_avg_linear_delta, min_avg_linear_delta,
    max_root_avg_linear_delta, min_root_avg_linear_delta,
    )

#set hard cap on num_traces
def calc_num_traces(word, max_traces):
    #function of length
    word_len = len(word)
    if word_len == 1  or word_len == 2:
        return word_len
    
    return max(int(word_len**1.195) + 2, max_traces)

def gen_traces(word, max_traces):
    #trace -> sum of k of n letters, and then average those letters
    num_traces = calc_num_traces(word, max_traces)
    excluded_indices = []
    max_tries = 5
    word_len = len(word)
    index_list = list(range(word_len))

    for i in range(num_traces):
        #select which indices to exclude by trace index?
        indices = sorted(random.sample(index_list, i % random.randint(1, word_len)))
        tries = 0
        while indices in excluded_indices and tries < max_tries:
            indices = sorted(random.sample(index_list, i % random.randint(1, word_len)))
            tries += 1
        if tries < max_tries:
            excluded_indices.append(indices)
        else:
            continue

    traces = []
    trace_count = 0
    for excluded in excluded_indices:
        traces.append("")
        for i in range(word_len):
            if i not in excluded:
                traces[trace_count] += word[i]
        trace_count += 1

    #gens substrings
    #print('traces for word: ', word, traces)
    return traces

def startsWithUpper(word):
    letter = word[0]
    ascii = ord(letter)
    if ascii >= 65 and ascii <= 90:
        return 1
    return 0

def sum_word(word):
    return sum([ord(c) for c in word])

def count_punct(word):
    punct_ascii = [33, 46, 63, 59]
    count = 0
    for c in word:
        ascii = ord(c)
        if ascii in punct_ascii:
            count += 1

    return count

def calc_pref(word, pref_freq):
    #return max prefix val, and index?
    word_len = len(word)
    middle = int(word_len/2) + 1 #1 letter past middle of word
    middle = min(middle, word_len)
    pref = ""
    max_pref_freq = 0
    max_pref = ""
    
    for i in range(middle):
        pref += word[i]
        freq = 0
        if pref in pref_freq.keys():
            freq = pref_freq[pref]
        if freq > max_pref_freq:
            max_pref_freq = freq
            max_pref = pref
    return (max_pref, max_pref_freq)

def calc_suff(word, suff_freq):
    #return max prefix val, and index?
    word_len = len(word)
    middle = int(word_len/2) + 1 #1 letter before middle of word
    suff = ""
    max_suff_freq = 0
    max_suff = ""
    
    for i in range(middle):
        suff += word[word_len - 1 - i]
        freq = 0
        if suff in suff_freq.keys():
            freq = suff_freq[suff]
        if freq > max_suff_freq:
            max_suff_freq = freq
            max_suff = suff
        
    return (max_suff, max_suff_freq)

    
    #todo
def calc_slope(word_vec, last_word_vec, index):
    #index delta is always one, should this get considered somehow????
    delta = []
    for i in range(len(word_vec)):
        index_delta = word_vec[i] - last_word_vec[i]
        delta.append(index_delta)
    return delta

def calc_vector_delta(word, last_word):
    error = 0
    other_error = 0
    #print('delta: ', word, ' ', last_word)
    for i in range(len(word)):
        error += (word[i] - last_word[i])**2
        other_error += (word[i] - last_word[i])**2/max(word[i]**2, last_word[i]**2, 1)
    
    return (error**.5, other_error**.5)

#todo - finish
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
        last_word_vec = word_vector(last_word, suff_freq, pref_freq, 0, 0)
        last_slope = last_word_vec
        sum = last_word_vec
        index = 1
        words = entry.split()
        max_length = len(words)
        for word in words:
            if word is None:
                continue
            word_vec = word_vector(word, pref_freq, suff_freq, index, max_length)
            #slope = 0
            slope = calc_slope(word_vec, last_word_vec, index) #add some modifier based on index/max_length?
            if last_word not in model.keys():
                model[last_word] = []
                #model[last_word].append((slope, sum, word))

            model[last_word].append((slope, sum, index, float(index/max_length), word, last_word_vec, last_slope))
            index += 1
            last_word = word
            last_word_vec = word_vec
            last_slope = slope
            val_index = 0
            for val in word_vec:
                sum[val_index] += val
                val_index += 1
            
            

    #training
    #last word = None
    #sum = 0 vector
    #for word in sentence:
    # vectorize last word, word
    #calc slope or delta word - last word

    #model[word] = [(slope_0, sum_0, index_0), ..., (slope_n, sum_n, index_n)]
    #for p in model[word]:
    #   calculate p with closest 


    return model

def gen_word(model, word_k, word_k_vec, word_slope, index):

    #locate the entry in model with data hashed to word_k with the slope and sum closest to out slope and sum
    possible = model[word_k]
    # print(""" tuple: \n
    # ((slope, sum, index, float(index/max_length), next_word, last_word_vec, last_slope))
    # \n slope, sum and word_vecs: \n
    # p_0 prefix val
    # p_1 suffix val
    # p_2 count of punctuation
    # p_3 sum of letters
    # p_4 index of max_pref_freq
    # p_5 index of max_suff_freq
    # p_6 length
    # p_7 index
    # p_8 relative index/percentage
    # """)
    best_tuple_0 = None
    min_tuple_dist_0 = float('inf')
    best_tuple_1 = None
    min_tuple_dist_1 = float('inf')
    for tuple in possible:
        #print('word: ', word_k , ' ', tuple)
        tuple_slope = tuple[0]
        tuple_sum = tuple[1]
        tuple_index = tuple[2]
        tuple_rel_index = tuple[3]
        tuple_next_word = tuple[4]
        tuple_word_vec = tuple[5]
        tuple_word_slope = tuple[6]
        #print('tuple:\n', tuple)
        #start with just comparing tuple_word_vec with word_k_vec
        delta = calc_vector_delta(word_k_vec, tuple_word_vec)
        if delta[0] < min_tuple_dist_0:
            min_tuple_dist_0 = delta[0]
            best_tuple_0 = tuple
        if delta[1] < min_tuple_dist_1:
            min_tuple_dist_1 = delta[1]
            best_tuple_1 = tuple

    return (best_tuple_0, min_tuple_dist_0 ,best_tuple_1, min_tuple_dist_1)

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
    
    middle = int(word_len/2) - 1 #1 letter before middle of word
    suff = ""
    
    for i in range(middle):
        suff += word[word_len - 1 - i]
        if suff in suffix_freq.keys():
            freq = suffix_freq[suff]
            suffix_freq[suff] = freq + 1
        else:
            suffix_freq[suff] = 1

    middle = min(int(word_len/2) + 1, word_len) #1 letter past middle of word
    pref = ""
    
    for i in range(middle):
        pref += word[i]
        if pref in prefix_freq.keys():
            freq = prefix_freq[pref]
            prefix_freq[pref] = freq + 1
        else:
            prefix_freq[pref] = 1


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