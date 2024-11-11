import pandas as pd
import numpy as np
import matplotlib as mpl
import csv
import streamlit as st

file_rank = "2022-01-08.csv" 
dataset_ranks = pd.read_csv(file_rank)
file_reviews = "bgg-19m-reviews.csv"
dataset_reviews = pd.read_csv(file_reviews)



# Cleaned data, took out the URL and thumbnail columns

# Dataset with the ranks first
clean_dataset_rank  = dataset_ranks.drop(["URL", "Thumbnail"], axis = 1) 
clean_dataset_rank = clean_dataset_rank.rename(columns = {"Unnamed: 0" : "Game Index", "Bayes average": "Bayes Average", "Users rated" : "Users Rated"})
clean_dataset_rank

# Then the dataset with the reviews second
clean_review_data = dataset_reviews.drop(["Unnamed: 0", "comment"], axis = 1)
clean_review_data = clean_review_data.rename(columns = {"user":"User", "rating":"Rating", "name" : "Name_of_Game"})
clean_review_data

# Data with the ranks sorted by the average score
# Not the best way, the amount of reviews per game varies from 30 to 70k reviews. 
# yet to be graphed idk when I want to show it.
data_by_average = clean_dataset_rank.sort_values("Average", ascending= False)
data_by_average

# Data sorted by the rank, same as sorting by the Bayes Average
data_by_rank = clean_dataset_rank.sort_values("Rank")
data_by_rank
data_sorted_by_bayes = clean_dataset_rank.sort_values("Bayes Average", ascending = False)
data_sorted_by_bayes

# Code for the Wilson function:

# total number of positive reviews per game, you input the dataframe and the ID of a game 
# and it gives you the total number of positive reviews for that game
# useless I have a column in the first part that does exactly this ahahahhahah

def count_positive_reviews_per_game(dataset, ID):
    
    df_positive_reviews = dataset.loc[(dataset["ID"] == 1752) & (dataset['Rating'] >= 6.0)]
    positive_reviews_count = df_positive_reviews['Rating'].count() 

    return int(positive_reviews_count)

# Total reviews, is this the most efficient way? ask someone you know tomorrow
def total_reviews(dataset):
    for game in dataset:
        total_reviews = dataset['Number_of_Ratings']
    
    return total_reviews

# I need a better way to say that. 
# the following is the trial
index = 0
for index in range(21830):
    int(total_reviews(dataset_ranks)[index])

# I could make a function with the share of positive reviews, or 3 different functions,
# I imagine a single one with all the other ones is better.

def share_of_positive_reviews_per_game(ID):
    count_positive_reviews_per_game(dataset_reviews, ID) / total_reviews(dataset_ranks)

for id in clean_dataset_rank['ID']:
    share_of_positive_reviews_per_game(id)
        
        

# part of the code for the greater Wilson function
# which has to be a column in the end.







# take all the positive rankings associated to that id. (above 6, according to the score)
        
# return me the wilson score, i'd say.
        
# then I can start graphing shit and other stuff
# count the number of positive ratings in the review table, what's the best way to do this? can I do this through SQL?

# my biggest question is, if there was a more
# efficient way to do things will you take points away?
# or is it just about fulfilling the criteria and
# being able to explain everything?