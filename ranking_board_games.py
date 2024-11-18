import pandas as pd
import numpy as np
import scipy.stats as sps
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

# Total number of positive reviews per game


def count_positive_reviews_per_game(dataset, ID):
    
    df_positive_reviews = dataset.loc[(dataset["ID"] == ID) & (dataset['Rating'] >= 6.0)]
    positive_reviews_count = df_positive_reviews['Rating'].count() 

    return int(positive_reviews_count)

# Total reviews:
def total_reviews(dataset, ID):
    total_reviews = dataset['Number_of_Ratings']
    total_reviews_ID = total_reviews.loc[(dataset['ID']== ID)]
    return int(total_reviews_ID.iloc[0])

# Ratio of positive review per total reviews
def share_of_positive_reviews_per_game(ID):
    share_of_pos_reviews_per_game = float(count_positive_reviews_per_game(clean_review_data, ID) / total_reviews(clean_dataset_rank, ID))
    return round(share_of_pos_reviews_per_game, 4)

# Calculating the ratio for every game (there is probably a better and faster implementation for this than a for loop)
for id in clean_dataset_rank['ID']:
    share_of_positive_reviews_per_game(id)

# find the confidence level z_alpha/2

def confidence_level(confidence):
    cl = sps.norm.ppf(confidence)
    return cl

# who decides the confidence in the end? 
# you can ask for a confidence level
# i'll set it but it' be cool if in the streamlit you could slide it and the 
# distribution changes accordingly.
# confidence = float(input("Please input a confidence level"))

# Wilson function, otherwise known as the lower bound
# on the propoertion f positive ratings
def Wilson_Function(ID, confidence = .95):
    
    z = confidence_level(confidence)
    p_hat = share_of_positive_reviews_per_game(ID)
    n = total_reviews(clean_dataset_rank, ID)
    
    Wilson_Score = round(float((p_hat + z**2/(2*n) - z*np.sqrt((p_hat*(1 - p_hat) + z**2/(4*n))/n)) / (1 + (z**2)/n)), 2)
    
    return Wilson_Score

def array_scores(dataset, ID):
    list_scores = []
    i = 1
    for i in range(1,11):
        df_i_reviews = dataset.loc[(dataset['ID'] == ID) & (dataset['Rating'].between(i, i + 1, inclusive='left'))]
        i_reviews = df_i_reviews['Rating'].count()
        list_scores.append(int(i_reviews))
        i =+ 1
    
    return list_scores
        

def Bayesian_Average(ID, confidence = .95):
    z = confidence_level(confidence)
    n = array_scores(clean_review_data, ID)
    N = sum(n)
    first_part = 0
    second_part = 0
    for k, n_k in enumerate(n):
        first_part += (k+1)*(n[k]+1)/(N + 10)
        second_part += (k+1)*(k+1)*(n[k]+1)/(N+10)
    score = first_part - z*np.sqrt((second_part - first_part*first_part)/(N+11))
    
    return score

# now that I have my wilson score I can compare it to the other ones. I think I have to make a new column add it to the og dataframe and 
# rank them by Wilson Score, and I have to graph them.

# Possibly the same thing with the Bayesian score, tomorrow just graph them


# What types of objects/class could I run here? the class' purpose is a template of objects that you create a new instance of every time.
# the class of a game would make sense, the class of dataset with games? the class of the variables and the function? 
# They'd be methods of a larger class what kind of object would need that kind of class? idk, we'll see


# Find a way to rank the games:



# I could count the number of comments. Find certain amounts of words.
# I could count the year or the playing time/cost but I would have to download new datasets and merge them with the old ones
# keeping count of when these datasets were assembled.

# I made the bayesian thing
