
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



if __name__ == "__main__":
    main()