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

"""
Load dataframe first (not doing anything with this yet...)
"""

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

"""
Load "all-text" file next (contains every sentence, concatenated into one string)
"""

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
Scan through All-Text string, getting rid of punctuation and saving all individual sentences to a list of strings
"""

# Initialize list
bible_all_sentences_list = []

# Initialize first sentence
sentence = ""

# Progress bar
bar = IncrementalBar('Countdown', max = bible_all_text_len)

# Main loop: get rid of punctuation, store sentences in a list
for char_idx, char in enumerate(bible_all_text_str):

    # Keep it if its alphanumeric or a space (i.e. not a punctuation mark)
    if char.isalnum() is True or char == " ":
        sentence = sentence + char
    # If character is a period, store preceding text (the sentence), add that to the list
    elif char == ".":
        #Take out the single space at the beginning of each sentence (not needed for analysis)
        sentence = sentence[1:]
        # Add trimmed sentence to the list
        bible_all_sentences_list.append(sentence)
        # Reset the sentence string
        sentence = ""

    bar.next()

bar.finish()

# If you need to turn the list of sentences into a real array
# bible_all_sentences_arr = np.array(bible_all_sentences_list)

# Pickle the numpy array containing each separate sentence as a string
out_list_name = f"{bible_version}_sentences.list"

with open(out_list_name, 'wb') as outfile:

    pickle.dump(bible_all_sentences_list, outfile)
print(f"Pickle of {out_list_name} complete.")
