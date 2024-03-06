'''
Silly-man's multiprocessing :)

Run multiple instances of this script or make it better.
'''

import sqlite3
import pickle
import pandas as pd
import sqlite3
import colorama

# create table with unique id column and a text column, called walls1337bot

conn = sqlite3.connect('walls1337bot.db')
c = conn.cursor()
# create table if it doesnt exist:
c.execute('''CREATE TABLE IF NOT EXISTS walls1337bot
             (id TEXT PRIMARY KEY, train_text TEXT, score INT, length INT)''')
conn.commit()
#conn.close()


files = ["2016_j_wallstreetbets.pkl", "2017_j_wallstreetbets.pkl", "2018_j_wallstreetbets.pkl"]

df = pd.DataFrame()

conn = sqlite3.connect('walls1337bot.db')
c = conn.cursor()

for file in files:
    with open(file, 'rb') as f:
        data = pickle.load(f)
        df = df.append(data)
# remove first 3 characters in all rows of the "parent_id" column
df['parent_id'] = df['parent_id'].str[3:]

# or for the full combined: 
#df = pd.read_csv('combined_df-with-removeds', index_col=0)

print("df head:")
print(df.head())
print("df length:", len(df))


def build_convo_chain_by_id(df, id):
    HAS_PARENT = True
    convo_chain = []
    while HAS_PARENT:
        try:
            # get just the author, body, and score. 
            row = df[df['id'] == id]
            
            convo_chain.append(row[['author', 'body', 'score']].values[0].tolist())
            #print(row['body'].values)
            if row['parent_id'].isna().values[0]:
                HAS_PARENT = False
            else:
                id = row['parent_id'].values[0]
                #print(id)
        except IndexError:
            #print("ID not found")
            break

    # reverse the convo_chain:
    convo_chain = convo_chain[::-1]
    return convo_chain


# get a list of each unique id column
ids = df['id'].unique()


import random
import colorama

# shuffle ids
random.shuffle(ids)

MIN_LEN = 2
MIN_SCORE = 3

BOT_NAME = "Walls1337bot"

hm_samples = 1000000
sample_count = 0

samples = []

for idx in ids:
    chain = (build_convo_chain_by_id(df, idx))
    reply_score = int(chain[-1][-1])

    if len(chain) >= MIN_LEN and reply_score >= MIN_SCORE:
        print("ID: ", idx)
        print("Score: ", reply_score)

        final_reply_author = chain[-1][0]
        author_ids = {final_reply_author: BOT_NAME}
        start_id = 0
        in_str = "### BEGIN CONVERSATION ###\n\n"
        for i in chain[:-1]:
            author = i[0]
            if author not in author_ids:
                author_ids[author] = "Speaker_" + str(start_id)
                start_id += 1
            in_str += "## "+author_ids[author] + ": ##\n" + i[1] + "\n\n"

        in_str += "## " + author_ids[final_reply_author] + ": ##\n"
        out_str = chain[-1][1] + "\n\n### END CONVERSATION ###"

        train_string = in_str + out_str
        
        # if idx not in database, add the idx and train_string
        c.execute("SELECT * FROM walls1337bot WHERE id=?", (idx,))
        if c.fetchone() is None:
            c.execute("INSERT INTO walls1337bot (id, train_text, score, length) VALUES (?, ?, ?, ?)", (idx, train_string, reply_score, len(chain)))
            conn.commit()
            # print added to database in green:
            print(colorama.Fore.GREEN + "Added to database" + colorama.Style.RESET_ALL)
            sample_count += 1
        else:
            # print already in database in red!
            print(colorama.Fore.RED + "Already in database" + colorama.Style.RESET_ALL)

    if sample_count >= hm_samples:
        break


