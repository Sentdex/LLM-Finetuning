import os
import json
import pandas as pd
from tqdm import tqdm
import time
import pickle

# Set the directory

directories = ["2016_j", "2017_j", "2018_j"]

target_subreddits = ["wallstreetbets"]


'''target_subreddits = ["wallstreetbets",
                     "askreddit",
                     "showerthoughts",
                     "todayilearned",
                     "cleanjokes",
                     "murderedbywords",
                     "jokes",
                     "funny",
                     "roastme",
                     "dadjokes",
                     "madlads",
                     "cringe",
                     "wtf",
                     "memes",
                     "publicfreakout",
                     "insanepeoplefacebook",
                     "facepalm",
                     "holdmybeer",
                     "instant_regret",
                     "idiotsincars",
                     "nonononoyes",
                     "yesyesyesno",
                     "maliciouscompliance",]'''



for directory in directories:
    START = time.time()

    # Create an empty dataframe
    df = pd.DataFrame(columns=["author", "subreddit", "created_utc", "parent_id", "id", "body", "score"])

    # Iterate over the files in ascending order by filename, set number of files to process
    files = sorted([f for f in os.listdir(directory)])
    #files = files[:10]
    print(files)

    for file in tqdm(files):
        with open(f"{directory}/{file}", "r") as f:
            try:
                tmpdf = pd.DataFrame([json.loads(line) for line in f])
                # lowercase the subreddit column
                tmpdf["subreddit"] = tmpdf["subreddit"].str.lower()
                # filter out the rows that do not have the target subreddit
                tmpdf = tmpdf[tmpdf["subreddit"].isin(target_subreddits)]
                #print(tmpdf.head())
                # append the tmpdf columns: "subreddit", "author", "created_utc", "parent_id", "id", "body" to the main dataframe
                #df = df.append(tmpdf[["subreddit", "author", "created_utc", "parent_id", "id", "body"]])
                # use concat instead of append
                df = pd.concat([df, tmpdf[["author", "subreddit", "created_utc", "parent_id", "id", "body", "score"]]])
            except Exception as e:
                print(str(e))


    print(df.head())
    print('length:', len(df))
    df = df.sort_values(by="created_utc")
    print(df.head())

    #save the dataframe to a csv as directory and target subreddits
    fname = f"{directory}_wallstreetbets.pkl"

    with open(fname, "wb") as f:
        pickle.dump(df, f)
        print(f"Saved to {directory}_{'_'.join(target_subreddits)}.pkl")

    print(f"Time taken: {(time.time() - START)/60} minutes")
