import sqlite3
import pandas as pd
import sqlite3
import json


# create table with unique id column and a text column, called walls1337bot

conn = sqlite3.connect('walls1337bot.db')
c = conn.cursor()
# create table if it doesnt exist:
c.execute('''CREATE TABLE IF NOT EXISTS walls1337bot
             (id TEXT PRIMARY KEY, train_text TEXT, score INT, length INT)''')
conn.commit()
# save the train_text column of the database to json formatted like {"sample": "text"}

MIN_SCORE = 7
MIN_LEN = 5
MAX_CHARS = 7500
c.execute("SELECT train_text FROM walls1337bot WHERE score >= ? AND length >= ?", (MIN_SCORE, MIN_LEN))
rows = c.fetchall()
print('Number of samples with these settings:',len(rows))
# save each row of train_text to json file such that it looks like
# {"sample": "text"} per line


bad_contents = ["[deleted]", 
                "[removed]", 
                "I am a bot, and this action was performed automatically. Please contact the moderators of this subreddit if you have any questions or concerns.",
                ".jpg",".png",".jpeg",".gif",
                ]

with open(f'WSB-min_score-{MIN_SCORE}-min_len-{MIN_LEN}-002.json', 'w') as f:
    for row in rows:
        if len(row[0]) < MAX_CHARS:
            if not any(bad in row[0] for bad in bad_contents):
                f.write(json.dumps({"sample": row[0]}) + "\n")
            else:
                print('bad content found')

conn.close()
