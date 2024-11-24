import pandas as pd
import os

''' Importing and Cleaning data'''

data_path = os.path.join(os.getcwd(), 'data')
print(data_path)

rank_file = "2022-01-08.csv" 
dataset_ranks = pd.read_csv(f'{data_path}\{rank_file}')
clean_rank_data  = dataset_ranks.drop(["URL", "Thumbnail", "Unnamed: 0", "Bayes average", 'Year'], axis = 1) 
clean_rank_data = clean_rank_data.rename(columns = {"Users rated" : "Number of Ratings"})

file_reviews = "bgg-19m-reviews.csv" # second dataset
dataset_reviews = pd.read_csv(f'{data_path}\{file_reviews}')
clean_review_data = dataset_reviews.drop(["Unnamed: 0", "comment"], axis = 1)
clean_review_data = clean_review_data.rename(columns = {"user":"User", "rating":"Rating", "name" : "Name_of_Game"})