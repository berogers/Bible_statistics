import pickle
import pandas as pd
import sys
import re
import numpy as np
from progress.bar import IncrementalBar

"""
Take a Bible version, load its DF, and load its All-Text string file for statistical operations
"""

# Set Bible version
bible_version = "KJV"
# bible_version = "ESV"
# bible_version = "LSB"
# bible_version = "NASB_95"
# bible_version = "NIV"

# Set general fetch path
bible_path = "./" + bible_version

# Path for DF
bible_df_path = bible_path + ".df"

# Open Bible df file
with open(bible_df_path, 'rb') as infile:

    # Read in whole-Bible df
    df_bible = pickle.load(infile)

# Sanity Checks for DF
print(f"Bible DF File {bible_df_path} imported; shape: {df_bible.shape}\n")
# print(df_bible.head())
# print(df_bible.tail())
# print(df_bible.describe())
print('Bible DF First row:')
print(df_bible.iloc[0])
print('\n')
# print(df_bible.iloc[8000])
print('Bible DF Last row:')
print(df_bible.iloc[df_bible.shape[0]-1])
print('\n')

# Path for all-text string
bible_all_text_path = bible_path + "_all_concat.str"

# Open Bible all-text string
with open(bible_all_text_path, 'rb') as infile:

    # Read in whole-Bible string
    bible_all_text_str = pickle.load(infile)

# Might need length for something later.
bible_all_text_len = len(bible_all_text_str)

# Sanity checks for all-text string
print(f"Bible All-text string {bible_all_text_path} imported.\nLength (num characters): {bible_all_text_len}\n")
print(f"Bible All-text string First 100 characters (w/in ''):\n'{bible_all_text_str[:100]}'\n")
print(f"Bible All-text string Last 100 characters (w/in ''):\n'{bible_all_text_str[-100:]}'\n")

# Remove Gen 1:1

"""
Scan through All-Text string, getting rid of punctuation and saving all individual sentences to a list (then array) of strings
"""

# Initialize list
bible_all_sentences_arr = []

# Initialize first sentence
sentence = ""

percent_readout_divisors = [5,4,3,2,1]
percent_readout_list = [bible_all_text_len/i for i in percent_readout_divisors]

# print(percent_readout_list)

# Progress bar
bar = IncrementalBar('Countdown', max = bible_all_text_len)

percent = 0
for char_idx, char in enumerate(bible_all_text_str):
    # if char_idx/bible_all_text_len in percent_readout_list:
    #     percent += 20
    #     print(f"{percent} completed")

    bar.next()

    if char.isalnum() is True or char == " ":
        sentence = sentence + char
    elif char == ".":
        bible_all_sentences_arr.append(sentence)
        sentence = ""

bar.finish()

# Turn the list of sentences into a real array
bible_all_sentences_arr = np.array(bible_all_sentences_arr)

# Pickle the numpy array containing each separate sentence as a string
out_arr_name = f"{bible_version}_sentences.arr"

with open(out_arr_name, 'wb') as outfile:

    pickle.dump(bible_all_sentences_arr, outfile)
print(f"Pickle of {out_arr_name} complete.")
