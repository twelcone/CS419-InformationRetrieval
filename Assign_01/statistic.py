from asyncore import file_dispatcher
import os
import re
import time
import math
import io
import pandas as pd

total_count = 0
word_list = []
word_map = {}

def add_map(data):
    global total_count, a
    token = re.split("[^a-zA-Z0-9]", data)
    for word in token :
        word = word.lower()
        if len(word) >0:
            if word in word_map:
                val = word_map[word]
                word_map[word] = val +1
                total_count = total_count + 1
            else:
                word_map[word] = 1
                total_count = total_count + 1

def convert(list):
    result = {}
    for i in list:
        result[i[0]] = i[1]
    return result 
             
def progress():
    files = os.listdir('Cranfield')
    for file in files:
        file = 'Cranfield/' + file
        data=open(file,'r').read().replace('\n', ' ')
        start_pos = data.find("<TEXT>") + 6
        end_pos = data.find("</TEXT>")
        data = data[start_pos : end_pos]
        add_map(data)

def create_df(df):
    df2 = pd.DataFrame({'Document': []})
    for i in word_map.keys():
        dummy = []
        for file in os.listdir('Cranfield'):
            file_path = 'Cranfield/' + file
            data=open(file_path,'r').read().replace('\n', ' ')
            if i in data: 
                dummy.append(file)
        df2.append(dummy, ignore_index=True)
                        
    df_result = df.join(df2)
    df_result.to_csv("posting_list.csv")

if __name__ == "__main__":
    progress()        
    word_list = sorted(word_map.items(), key=lambda x: x[1], reverse=True)
    word_map = convert(word_list)
    
    print(word_map)
    print("Total words in Cranfield dataset:", sum(word_map.values()))
    print("Num of terms:", len(word_map))
    
    # df1 = pd.DataFrame.from_dict(word_map, orient='index', columns=["Term, Count"])
    df1 = pd.DataFrame({"Terms": word_map.keys(),
                        "Count": word_map.values()})
    print(df1.head())

    # df_test = pd.DataFrame.from_dict({"Documents": [['t', 'k']]})
    # df_test2 = pd.DataFrame.from_dict({"Index": [0]})
    # df_test3 = pd.concat([df_test, df_test2], axis=1, ignore_index=True)
    # df_test3 = df_test2.join(df_test)
    # print(df_test3.head())
    # create_df(df1)