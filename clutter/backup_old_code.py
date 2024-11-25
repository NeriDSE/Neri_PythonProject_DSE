import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib as plt
import os
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


# who decides the confidence in the end? 
# you can ask for a confidence level
# i'll set it but it' be cool if in the streamlit you could slide it and the 
# distribution changes accordingly.
# confidence = float(input("Please input a confidence level"))

# Wilson function, otherwise known as the lower bound
# on the proportion of positive ratings
def confidence_level(confidence):
    cl = norm.ppf(1- (1 - confidence)/2)
    return cl

# with the list here you could use np.array to calculate all your total review stuff.
def Wilson_Function(ID, dataset = clean_dataset_rank, confidence = .95):
    z = confidence_level(confidence)
    n = total_reviews(dataset, ID)
    p_hat = 1 * share_of_positive_reviews_per_game(ID) #/ total_reviews(clean_data, ID)
    
    wilson_score = round(float((p_hat + z**2/(2*n) - z*np.sqrt((p_hat*(1 - p_hat) + z**2/(4*n))/n)) / (1 + (z**2)/n)), 2)
    


    return wilson_score

def array_scores(dataset, ID):
    list_scores = []
    for i in range(1,11):
        df_i_reviews = dataset.loc[(dataset['ID'] == ID) & (dataset['Rating'].between(i, i + 1, inclusive='left'))]
        i_reviews = df_i_reviews['Rating'].count()
        
        list_scores.append(int(i_reviews))
        
    return list_scores
        

def Bayesian_Average(ID, dataset = clean_review_data, confidence = .95):
    z = confidence_level(confidence)
    n = array_scores(dataset, ID)
    N = sum(n)
    first_part = 0
    second_part = 0
    for k, n_k in enumerate(n):
        first_part += (k+1)*(n[k]+1)/(N + 10)
        second_part += (k+1)*(k+1)*(n[k]+1)/(N+10)
    score = first_part - z*np.sqrt((second_part - first_part*first_part)/(N+11))
    
    return round(float(score), 2)

def New_Column(dataset, function):
    # create an empty list (our future column)
    New_column = []
    # for each row in a dataset I have to find its ID and apply a the funciton over it
    for id in dataset['ID']:
        New_column.append(function(id))
    
    return New_column

clean_dataset_rank.insert(-1, 'Bayesian Average', New_Column(clean_dataset_rank, Bayesian_Average))
clean_dataset_rank.insert(-1, 'Wilson_Score', New_Column(clean_dataset_rank, Wilson_Function))

clean_data2 = clean_dataset_rank[clean_dataset_rank['Number_of_Ratings'] > 80000]
clean_data2
len(clean_data2)

Bayesian_column = New_Column(clean_data2, Bayesian_Average)


clean_data2.insert(-1, 'Bayesian_Average', Bayesian_column )

# if you forget how to run shit:  
filtered_dataset_by_wilson = rb.dataset_by_review_bracket('most_reviewed', clean_rank_data, clean_review_data, ra.wilson_function, 'greater', 80000)
most_reviewed_games_by_wilson = filtered_dataset_by_wilson.add_column_to_df_filtered_by_reviews('Wilson function')
graph1 = gr.graph('most reviewed by wilson', most_reviewed_games_by_wilson, 'Wilson function', 'n')

filtered_dataset_by_bayes = rb.dataset_by_review_bracket('in between reviewed', clean_rank_data, clean_review_data, ra.bayesian_average, 'between', 3900)
mid_reviewed_games_by_bayes = filtered_dataset_by_bayes.add_column_to_df_filtered_by_reviews('New Bayesian Average', 4000)
mid_reviewed_games_by_bayes.sort_values('New Bayesian Average', ascending = False)

# I could count the number of comments. Find certain amounts of words. mix the comments with the votes for example... 
# the top voters, rank them. the experienced guard.

# a new hotness rank. cool too. definetely possible, I want to finish on my OGs tomorrow with the graphs
# maybe easier functions this time around.
# Let's see, number of comments and votes
# percentage of comments per positive votes? 

# the people who've ranked the most. fair let's try it.
