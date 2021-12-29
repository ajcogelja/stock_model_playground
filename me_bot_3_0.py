
from os import replace
import random
from sqlite3.dbapi2 import connect
from typing import cast
import numpy as np
import pandas as pd
from numpy.random import default_rng
import math
import matplotlib.pyplot as plt
import sqlite3
"""
Comment philosophy:
 # = inline standard code comment
 ## = sub section header
 ### = section header
"""

#open connection
conn = sqlite3.connect('chat.db')
rand_gen = default_rng()

def main():

    ### Read and Preprocess Data

    #count = pd.read_sql_query("select Count(*) from message where is_from_me = 1", conn)
    #print(count)#57722 messages from me
    msg_count = 3000
    messages = pd.read_sql_query('select * from message where is_from_me = 1 limit {}'.format(msg_count), conn)
    handles = pd.read_sql_query("select * from handle", conn)
    messages.rename(columns={'ROWID' : 'message_id'}, inplace = True)
    handles.rename(columns={'id' : 'phone_number', 'ROWID': 'handle_id'}, inplace = True)
    merge_level_1 = temp = pd.merge(messages[['text', 'handle_id', 'date','is_sent', 'message_id', 'is_from_me']],  handles[['handle_id', 'phone_number']], on ='handle_id', how='left')
    training_data = merge_level_1.sample(frac=.7)
    remaining = merge_level_1.drop(training_data.index)
    testing = remaining.sample(frac=.66)
    hold_out = remaining.drop(testing.index)
    
    ## Gather into nice and friendly list
    
    texts = []
    for msg in training_data['text']:
        if msg is not None:
            texts.append(msg)

    ### Create/Train model
        
    #Data structures for model
    word_graph = {}
    next_word = {}
    trace_map = {}
    next_word_count = {}

    for t in texts:
        process_texts(word_graph, next_word, next_word_count, trace_map, t, max_length=60)
    # input('see next_word')
    # print('next_word_count: ', next_word_count)
    # input('see trace_map')
    # print('trace_map: ', trace_map)
    # input('see word graph')
    # print('word graph: ', word_graph)
    model = (word_graph, next_word_count, trace_map)
    model = normalize_model(model, trace_prune_threshold=.84)
    while True:
        run = input('Run program?')
        if run.lower() == 'y':
            print('sentence: ', gen_raw_sentence(model))
        else:
            break

def gen_raw_sentence(model):
    word_graph, next_word_count, trace_map = model
    prev = None
    sentence = ''
    gen = True
    length = 0
    while gen:
        if prev not in next_word_count.keys():
            #try stripping of punctuation
            no_punc = remove_punct(prev)
            if no_punc in next_word_count.keys():
                prev = no_punc
            else:
                return sentence
        next_word_list = next_word_count[prev].keys()
        #print('word: ', prev, 'word graph: ', word_graph[prev])
        word_dict = word_graph[prev][1]
        word_graph_keys = list(word_dict.keys())
        word_graph_probs = list(word_dict.values())
        #print('word_graph_probs: ', word_graph_probs)
        for w in next_word_list:
            if w in word_dict.keys():
                prob = word_dict[w]
                index = word_graph_keys.index(w)
                #want to redo weight function
                word_graph_probs[index] += (6*prob) #weight this more heavily
            else:
                word_graph_probs.append(6*prob)
                word_graph_keys.append(w)

        
        next_word = rand_gen.choice(word_graph_keys, p = [prob/sum(word_graph_probs) for prob in word_graph_probs] )
        sentence += next_word + ' '
        #print('next word: ', next_word)
        prev = next_word
        length += 1
        #again_probs = [length+8, length*1.2]
        #again_probs_sum = again_probs[0] + again_probs[1]
        #again_probs[0] /= again_probs_sum
        #again_probs[1] /= again_probs_sum
        #probs should reflect a few things: 
        #gen = rand_gen.choice([True, False], p = again_probs)
    return sentence

    
def normalize_model(model, trace_prune_threshold):
    word_graph, next_word_count, trace_map = model
    power = .8
    word_occ_count = sum([word_graph[word][0]**power for word in word_graph.keys()])
    for word in word_graph.keys():
        #print('word:', word_graph[word])
        word_graph[word][0] = (word_graph[word][0]**power)/word_occ_count
        word_graph_sum = sum([word_graph[word][1][w]**power for w in word_graph[word][1].keys() ])
        for entry in word_graph[word][1].keys():
            word_graph[word][1][entry] = (word_graph[word][1][entry]**power / word_graph_sum)
        #print('after word:', word_graph[word])

    #print('trace_map: ', trace_map)
    counts = {}
    #prune the trace map with rarely occuring ones
    len_power = .3
    for t in trace_map.keys():
        for val in trace_map[t].keys():
            v = trace_map[t][val]*math.ceil(len(t)**len_power)
            if v in counts.keys():
                counts[v] += 1 #statistically shorter traces appear more often, even trying to reduce this is a better approach imo
            else:
                counts[v] = 1

    normalized_counts = {}
    for c in sorted(counts.keys()):
        normalized_counts[c] = counts[c]/sum(counts.values())            

    cdf = 0
    prune_val = 0
    for c in (normalized_counts.keys()):
        cdf += normalized_counts[c]
        if prune_val == 0 and cdf > trace_prune_threshold:
            prune_val = c
        #print('sum up to: ', c, 'is: ', cdf)
    
    new_trace_map = {}

    for t in trace_map.keys():
        for val in trace_map[t].keys():
            if trace_map[t][val]*math.ceil(len(t)**len_power) > prune_val:
                if t not in new_trace_map.keys():
                    new_trace_map[t] = {val: trace_map[t][val]}
                else:
                    if val not in new_trace_map[t].keys():
                        new_trace_map[t][val] = trace_map[t][val]
                    else:
                        print('this condition shouldnt execute')

    #now do we normalize it???
    for t in new_trace_map.keys():
        map_sum = sum([new_trace_map[t][w] for w in new_trace_map[t].keys()])
        for val in new_trace_map[t].keys():
            new_trace_map[t][val] = new_trace_map[t][val]/map_sum

    for w in next_word_count.keys():
        sum_counts = sum([ next_word_count[w][n] for n in next_word_count[w].keys() ])
        for next in next_word_count[w].keys():
            next_word_count[w][next] = next_word_count[w][next]/sum_counts
            #print(word, '- word, next: ', next, next_word_count[w][next])


    return (word_graph, next_word_count, new_trace_map)

#insert connections indicating one word follows another in a sentence
def insert_word_into_mem(graph, word, follower):
    default_occurences = 1
    #what if we wanted to track follower distance? a more challenging task i think, messy data structures
    if word not in graph.keys():
        graph[word] = [default_occurences, {follower : 1}] #list goes: occurences, follower_dict, cant use tuple and dont want to copy and move
    else:
        graph[word][0] += 1 #increment occurences
        if follower in graph[word][1].keys():
            #print('increment edge weight: ', follower, word)
            graph[word][1][follower] += 1 #increment edge weight
        else:
            graph[word][1][follower] = 1 #set count

#helper function, check for ascii punctuation values
def has_punct(word):
    punctuation = ["'", '"', '.', '!', '?', '`', ';', ',']
    for p in punctuation:
        if p in word:
            return True

    return False

def remove_punct(word):
    punctuation = ["'", '"', '.', '!', '?', '`', ';', ',']
    for p in punctuation:
        word = word.replace(p, '')
    return word

def trace_to_word(trace, word):
    new_word = ''
    for c in trace:
            new_word += word[c]
    return new_word

#function to create all a words traces
def gen_traces(word):
    traces = []
    traces_index = []
    word_len = len(word)
    if has_punct(word):
        for t in gen_traces(remove_punct(word)):
            traces.append(t)
    if word_len < 2:
        return traces
    num_traces = int(math.exp(-(word_len >> 7)) * word_len**1.08) #cant use bit shift here, because its a float. I have to multiply 
    numbers = list(range(0, word_len))
    prob = []
    k = .496
    k *= 2
    half = word_len >> 1
    for i in range(word_len):
        prob.append((half**k - abs(half - i)**k)*(i**.5))
    probs = [p/sum(prob) for p in prob]
    max_retries = 10
    for i in range(num_traces):
        retries = 0
        trace_len = rand_gen.choice(word_len, p=probs)
        t = np.sort(rand_gen.choice(numbers, trace_len, replace=False, shuffle=False))
        while list(t) in traces_index and retries < max_retries:
            retries += 1
            trace_len = rand_gen.choice(word_len, p=probs)
            t = np.sort(rand_gen.choice(numbers, trace_len, replace=False, shuffle=False))
        trace = trace_to_word(t, word)
        traces_index.append(list(t))
        traces.append(trace)

    return traces

#create and insert all traces with counts for words
def map_traces(trace_map, word):
    traces = gen_traces(word)
    for trace in traces:
        if trace in trace_map.keys():
            if word in trace_map[trace].keys():
                trace_map[trace][word] += 1
            else:
                trace_map[trace][word] = 1
        else:
            trace_map[trace] = {word: 1}

def insert_word(prev_word, word, next_words, next_word_count):
    if prev_word in next_words.keys(): 
        if word not in next_words[prev_word]:
            next_words[prev_word].append(word)
            next_word_count[prev_word][word] = 1
        else:
            next_word_count[prev_word][word] += 1

    else:
        next_words[prev_word] = [word] #next_word_holds a list of possible follower words
        next_word_count[prev_word] = {word: 1}

def process_texts(word_graph, next_word, next_word_count, trace_map, text, max_length):
    words = text.lower().split(' ')
    length = len(words)
    if length == 0:
        return
    
    prev_word = None
    first_insert = False
    for w in range(length):
        if len(words[w]) == 0 or len(words[w]) > max_length:
            continue
        if not first_insert:
            insert_word_into_mem(graph=word_graph, word = prev_word, follower=words[w])
            if has_punct(words[w]):
                insert_word_into_mem(graph=word_graph, word = prev_word, follower = remove_punct(words[w]))
            first_insert = True
        map_traces(trace_map, words[w])
        for i in range(w + 1, length):
            #loop from current word to end of sentence, adding links into graph
            insert_word_into_mem(graph=word_graph, word = words[w], follower=words[i])
            if has_punct(words[w]):
                insert_word_into_mem(graph=word_graph, word = remove_punct(words[w]), follower=words[i])
                if has_punct(words[i]):
                    insert_word_into_mem(graph=word_graph, word = remove_punct(words[w]), follower=remove_punct(words[i]))
            else:
                if has_punct(words[i]):
                    insert_word_into_mem(graph=word_graph, word = words[w], follower=remove_punct(words[i]))
            

        insert_word(prev_word, words[w], next_word, next_word_count)
        prev_word = words[w]
        

if __name__ == "__main__":
    main()