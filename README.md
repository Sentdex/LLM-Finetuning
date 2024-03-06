# LLM-Fine-Tune-Dataset-Create
Some helpers and examples for creating an LLM fine-tuning dataset

Based on the tutorial video here: https://www.youtube.com/watch?v=pCX_3p40Efc

- 1.Decompress-Bigquery.py: Decompresses the gzip json files from the bigquery export of reddit data comments.
- 2.load_subreddits.py: This script builds large pickle files consisting of the comments from the subreddits you target.
- 3.Build_training_data.py: This script loads those dataframes from 2. and builds chains of conversations. Run as many instances of this simultaneously as you want to make this process go faster and/or fix it to be a proper multi-processed script.
- 4.make_train_json.py: Creates the actual json file that you can upload straight to huggingface as a dataset to then fine-tune.

  


The fine-tuning script I used was modified: https://colab.research.google.com/drive/1PEQyJO1-f6j0S_XJ8DV50NkpzasXkrzd?usp=sharing#scrollTo=x-xPb-_qB0dz
