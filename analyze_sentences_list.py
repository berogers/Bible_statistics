import pickle
import pandas as pd
import sys
import re
import numpy as np
from progress.bar import IncrementalBar
from matplotlib import pyplot as plt

"""
Take a list of all sentences in the Bible, and learn things from it
"""

# Set Bible version
bible_version = "KJV"
# bible_version = "ESV"
# bible_version = "LSB"
# bible_version = "NASB_95"
# bible_version = "NIV"

# Set general fetch path
bible_path = "./" + bible_version

# Path for sentences array
bible_list_path = bible_path + "_sentences.list"

# Open Bible sentences list file
with open(bible_list_path, 'rb') as infile:

    # Read in whole-Bible df
    bible_all_sentences_list = pickle.load(infile)
    
bible_tot_num_sentences = len(bible_all_sentences_list)

# Some descriptive stats:
print(f"Bible All-Sentences list {bible_list_path} imported; length (= how many sentences): {bible_tot_num_sentences}\n")

# Sanity checks:
print(f"Bible All-Sentences list first sentence:\n{bible_all_sentences_list[0]}\nLength: {len(bible_all_sentences_list[0])}\n")
print(f"Bible All-Sentences list penultimate sentence: '{bible_all_sentences_list[bible_tot_num_sentences-2]}'\n")
print(f"Bible All-Sentences list last sentence: '{bible_all_sentences_list[bible_tot_num_sentences-1]}'\n")

"""
Get average number of words per sentence in Bible
"""

# Number of words in a sentence string = number of spaces + 1

# Init storage list of number of words in each sentence
bible_n_words_per_sentence = []

# Progress bar
bar = IncrementalBar('Countdown', max = bible_tot_num_sentences)

# For each sentence...
for sentence in bible_all_sentences_list:

    # Min num words is one
    num_words = 1
    # Scan sentence string anyway
    for char in sentence:

        # If a space is encountered, there is at least one more word in the sentence, so add one word to the counter
        if char == " ":

            num_words += 1
    # Append sentence length "words-per-sentence" list
    bible_n_words_per_sentence.append(num_words)
    # Advance progress bar
    bar.next()

# Close progress bar
bar.finish()

# Calculate grand average (2 decimal places)
bible_avg_n_words_per_sentence = round((sum(bible_n_words_per_sentence) / len(bible_n_words_per_sentence)), 2)

print(f"Average number of words per sentence in the {bible_version} Bible is: {bible_avg_n_words_per_sentence:.2f}")

# Plot distribution of sentence lengths!
plt.hist(bible_n_words_per_sentence, 450)
plt.xlabel("Number of words per sentence")
plt.ylabel("Number of sentences w/ given num. words")
plt.title(f"Distribution of sentence length in {bible_version} Bible")
xlim_hi = 200
annotation_coords = (xlim_hi*.8,1250)
plt.annotate(f"Avg = {bible_avg_n_words_per_sentence:.2f}", xy=annotation_coords)
plt.xlim([0,xlim_hi])
plt.show()


"""
BR Note:

KJV Average number of words per Sentence = 30.14!

This checks out with https://www.thelastdialogue.org/article/bible-statistics-and-facts/
which says that the average num words per Verse = 25.2
(OT 27.6, NT 22.2)

Since sentences can and often do span multiple verses, verses should on average consist of a smaller number of number of words
than sentences do (BR's educated guess). Thus, the average number of words per Sentence of 30.14 checks out.
"""


"""
Main loop

For each sentence:
1) Parse it into n = avg number of words per sentence (i.e. 30) word-locations
2) Put the closest word to each word-location in a list of n (i.e. 30) lists,
    where each list will contain tot_num_sentences (i.e. 26,200) words
    
"""

# Progress bar
bar = IncrementalBar('Countdown', max = bible_tot_num_sentences)



for sentence in bible_all_sentences_list:
    
    

    # Advance progress bar
    bar.next()

# Close progress bar
bar.finish()