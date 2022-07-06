import pandas as pd
import sys
import re
import pickle

"""
Import a local Bible.txt file for parsing into (and saving):

i) Book
ii) Chapter
iii) Verse
iv) Verse Text

"""

# NOTE: At first, this script will only work with the KJV.txt "book (space) chapter:verse (space) text" format

# Set Bible version
bible_version = "KJV"
# bible_version = "ESV"
# bible_version = "LSB"
# bible_version = "NASB_95"
# bible_version = "NIV"

# Set fetch path
bible_path = "./" + bible_version + ".txt"

# Open Bible.txt file
with open(bible_path, 'r') as bible_file:

    # Read in whole Bible.txt as a string
    bible_text_raw = bible_file.read()

# print(f"type(bible_text_raw) is {type(bible_text_raw)}")

# for i in range(300):
#     char_i = bible_text_raw[i]
#     print(f"bible_text_raw[{i}] is {char_i}")

# print(f"aaaa{bible_text_raw[221]}aaaa")

if bible_version == "KJV":
    column_names = []
    pass

df_bible_text_raw = pd.read_table(bible_path, delimiter = '\n', header=None, names=["raw_line", "book", "chapter", "verse_num", "verse_text"])

# may need later
# df_bible_text_raw.insert(loc=len(df_bible_text_raw.columns), column="book", value='na')

df_bible_text_raw["book"] = 'na'
df_bible_text_raw["chapter"] = 'na'
df_bible_text_raw["verse_num"] = 'na'
df_bible_text_raw["verse_text"] = 'na'

print(df_bible_text_raw.head())
# print(df_bible_text_raw.tail())
# print(df_bible_text_raw.describe())
# print(df_bible_text_raw.shape)

# print(df_bible_text_raw.iloc[8000])

# Initiate the "all-text" string (will concatenate every verse into one string in loop)
bible_all_text_concat_str = ""

for row in df_bible_text_raw.iterrows():

    # Example row in DF:
    # 0  "Genesis 1:1\tIn the beginning God created the..."
    # Parse accordingly

    # Grab raw line (pandas) index, print for tracking progress
    raw_line_idx = row[0]
    # print(f"row {raw_line_idx}")
    # Grab raw line (row idx 1) as a one-item series (pandas default), then pull out the string
    raw_line_str = row[1][0]

    # Split raw line string (at the "\t" tab) the "Book Chap#:Verse#"-format string (elem index 0) from Verse Text string (elem index 1)
    # E.g., split into:
    # ["Genesis 1:1", "In the beginning God created the..."]
    split_line = raw_line_str.split("\t")
    # Grab "Book Chap#:Verse#"-format string
    book_chap_versenum = split_line[0]
    # Grab Verse Text proper
    verse_text = split_line[1]

    # Add isolated Verse Text proper into DF
    df_bible_text_raw.at[raw_line_idx, "verse_text"] = verse_text
    # Add isolated Verse Text to "all-Bible-text" string
    bible_all_text_concat_str = bible_all_text_concat_str + " " + verse_text


    # Split "Verse#" str from "Book Chap#" str, store in variables
    split_book_chap_from_versenum = book_chap_versenum.split(":")

    # print('split_book_chap_from_versenum')
    # print(split_book_chap_from_versenum)

    # Grab "Book Chap#" str
    book_chap = split_book_chap_from_versenum[0]

    # print('book_chap')
    # print(book_chap)

    # Split "Verse#" str
    verse_num = split_book_chap_from_versenum[1]

    # print('verse_num')
    # print(verse_num)

    # Add isolated Verse Number into DF
    df_bible_text_raw.at[raw_line_idx, "verse_num"] = verse_num

    # Parse "Book Chap#" into Book and Chap#
    # NOTE: A little tricky, because some books are named with an index number at the beginning (e.g. 1 Samuel, 2 Samuel)
    # Strategy--
    # Chapter #:
    # i) Take last 2 characters of "Book Chap#" string: will list a chapter number either as " #" or "##"
    # ii) Strip the space from it
    # iii) Turn it into integer after insertion into DF
    # Book Name:
    # i) Take remaining (first) n-2 characters from "Book Chap#" string (will be in "Book" or "Book " format)
    # ii) Strip the spaces from it (final Book Name format that will remain in the DF: e.g. "1Samuel")

    ## Chapter #
    # Grab last 2 characters from "Book Chap#" string
    # Result: chapter number in " #" or "##" format
    chap_num_w_spaces = book_chap[-2:]
    ## Book Name
    # Grab first n-2 characters from "Book Chap#"
    book_name_w_spaces = book_chap[:-2]

    # Add Book Name (w Spaces) to DF
    df_bible_text_raw.at[raw_line_idx, "book"] = book_name_w_spaces
    # Add Chapter # (w Spaces) to DF
    df_bible_text_raw.at[raw_line_idx, "chapter"] = chap_num_w_spaces

# Strip any spaces from Book Name or Chapter Number columns
df_bible_text_raw['book'] = df_bible_text_raw['book'].str.strip()
df_bible_text_raw['chapter'] = df_bible_text_raw['chapter'].str.strip()

# print(f"Bible All-text file First 100 characters: {bible_all_text_concat_str[:100]}")
# print(f"Bible All-text file Last 100 characters: {bible_all_text_concat_str[-100:]}")

# sys.exit()

# # Sanity checks
# print(df_bible_text_raw.iloc[0])
# print(df_bible_text_raw.iloc[8000])

# print('df at 0, chapter')
# a = df_bible_text_raw.at[0, 'chapter']
# print(f"'{a}'")
# print('df at 0, book')
# b = df_bible_text_raw.at[0, 'book']
# print(f"'{b}'")

# print('df at 8000, chapter')
# a = df_bible_text_raw.at[8000, 'chapter']
# print(f"'{a}'")
# print('df at 8000, book')
# b = df_bible_text_raw.at[8000, 'book']
# print(f"'{b}'")

# print(df_bible_text_raw.head())
# print(df_bible_text_raw.tail())

# Pickle the conglomerate all-Bible-text string for analysis in "bible_sentence_stats.py"
out_str_name = f"{bible_version}_all_concat.str"

with open(out_str_name, 'wb') as outfile:

    pickle.dump(bible_all_text_concat_str, outfile)
print(f"Pickle of {out_str_name} complete.")

# # Pickle the parsed Bible DF for analysis (e.g. in "bible_sentence_stats.py" script)
# out_df_name = f"{bible_version}.df"

# with open(out_df_name, 'wb') as outfile:

#     pickle.dump(df_bible_text_raw, outfile)
# print(f"Pickle of {out_df_name} complete.")

# # Pickle the Bible DF as a CSV
# df_bible_text_raw.to_csv(f"{bible_version}.csv")
# print(f"CSV of {bible_version} complete.")
