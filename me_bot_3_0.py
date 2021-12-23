
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
traces_model = {}

conn = sqlite3.connect('chat.db')

def main():
    #cur = conn.cursor()
    #cur.execute("select name from sqlite_master where type = 'table' ")
    # for n in cur.fetchall():
    #     print('TABLE: ', n)
    #count = pd.read_sql_query("select Count(*) from message where is_from_me = 1", conn)
    #print(count)#57722 messages from me
    messages = pd.read_sql_query("select * from message where is_from_me = 1 limit 3000", conn)
    handles = pd.read_sql_query("select * from handle", conn)
    messages.rename(columns={'ROWID' : 'message_id'}, inplace = True)
    handles.rename(columns={'id' : 'phone_number', 'ROWID': 'handle_id'}, inplace = True)
    merge_level_1 = temp = pd.merge(messages[['text', 'handle_id', 'date','is_sent', 'message_id', 'is_from_me']],  handles[['handle_id', 'phone_number']], on ='handle_id', how='left')
    training_data = merge_level_1.sample(frac=.7)
    remaining = merge_level_1.drop(training_data.index)
    testing = remaining.sample(frac=.66)
    hold_out = remaining.drop(testing.index)
    
    
    texts = []
    for msg in training_data['text']:
        if msg is not None:
            texts.append(msg)

        
    words = {}
    traces = {}
    word_count = {}
    trace_count = {}
    word_radius = 0

    for t in texts:
        words, traces = process_texts(words, traces, t, word_count, trace_count)
        word_radius = calc_radius(words, traces, word_count, trace_count)

def process_texts(word_dict, trace_dict, word_count, trace_count, curr_text):
    words = curr_text.split(' ')
    words_lower = curr_text.lower().split(' ')

    prev_prev_word = None
    prev_word = None
    curr_word = None
    curr_word_vec = []
    prev_word_vec = []
    prev_prev_word_vec = []
    next_word = None
    outer_context = []

    sentence_length = len(words)
    
    #what if we have a param for max_trace_length

    #becomes light, then we get 


    for w in range(sentence_length):
        curr_word = words[w]
        curr_word_lower = words_lower[w]
        traces = gen_traces(curr_word, curr_word_lower)
        traces_dict, traces_count = add_all_traces(traces_dict, traces_count, traces, curr_word)
        curr_word_vec = vectorize_word(curr_word, w, traces)

        heavy_inner_context = [] #next + word + prev
        light_inner_context = [] #next + word + prev
        prev_prev_word = prev_word
        prev_word = curr_word
        heavy_inner_context = light_inner_context
    #gen sentence trace? or use a proximity of 2???
    #like local radius, then slightly more broad, then broadest

    
    return 1, 1

def gen_traces(curr_word, curr_word_lower):
    return []

def add_all_traces(trace_dict, trace_count, traces, word):
    #add trace to dictionary if needed
        #trace dict maps trace to word
    #count trace occurrences
    #go through this list, separating out those that only occur once or twice
    #those separated out will get added to a new "corrections" dict
    #corrections maps shitty trace for an old word to a newer better word
    #extremely common traces are most likely words, and will be treated as such
    for i in range(len(traces)):
        t = traces[i]
        if t in trace_dict.keys():
            if word not in trace_dict[t]:
                trace_dict[t].append(word) #all words the trace could go to
            trace_count[t] += 1
        else:
            trace_dict[t] = [word]
            trace_count[t] = 1
    
    return trace_dict, trace_count

def vectorize_word(curr, word_index, traces):
    return []

def calc_radius(word_dict, trace_dict):
    #calc some median, or avg radius based on trace distance
    return 1

    print('thanks for using me bot! Cya')

if __name__ == "__main__":
    main()