import pandas as pd
import numpy as np
from scipy.stats import norm


# I could probably get rid of the ID thing I need it for the whole dataset.
# freed reviews:

def total_reviews(dataset_ranks, id):
        total_reviews = dataset_ranks['Number of Ratings']
        total_reviews_ID = total_reviews.loc[(dataset_ranks['ID']== id)]
        return int(total_reviews_ID.iloc[0])

def count_positive_reviews_per_game(dataset_reviews, id):
        
        df_positive_reviews = dataset_reviews.loc[(dataset_reviews["ID"] == id) & (dataset_reviews['Rating'] >= 6.0)] 
        # Loc Accesses a group of columns by labels and makes a new df
        positive_reviews_count = df_positive_reviews['Rating'].count() 
        # the variable counts every element in the df, so all the positive reviews
        
        return int(positive_reviews_count)

    # Ratio of positive review per total reviews
def share_of_positive_reviews_per_game(dataset_ranks, dataset_reviews, id):
        share_of_pos_reviews_per_game = float(count_positive_reviews_per_game(dataset_reviews, id) / total_reviews(dataset_ranks, id))
        return round(share_of_pos_reviews_per_game, 4)

    # Function to calculate any confidence level
def confidence_level(confidence):
    cl = norm.ppf(1- (1 - confidence)/2)
    return cl
    
    # Wilson Function
def wilson_function(id, dataset_ranks, dataset_reviews, confidence = .95):
        z = confidence_level(confidence)
        n = total_reviews(dataset_ranks, id)
        p_hat = 1 * share_of_positive_reviews_per_game(dataset_ranks, dataset_reviews, id) 
        
        wilson_score = round(float((p_hat + z**2/(2*n) - z*np.sqrt((p_hat*(1 - p_hat) + z**2/(4*n))/n)) / (1 + (z**2)/n)), 2)
        
        return wilson_score
    
    
    
# For Bayesian Lower Bound:

# Array Scores, returns the number of times a game received a certainscore (how many 1/10s, how many 2/10s...)
def array_scores(id, dataset_reviews):
        list_of_scores = []
        for i in range(1,11):
            how_many_i_reviews = dataset_reviews.loc[(dataset_reviews['ID'] == id) & (dataset_reviews['Rating'].between(i, i + 1, inclusive='left'))]
            this_many_i_reviews = how_many_i_reviews['Rating'].count()
            
            list_of_scores.append(int(this_many_i_reviews))
            
        return list_of_scores

# Bayesian lower bound function
def bayesian_average(id, dataset_ranks, dataset_reviews, confidence = .95):
        z = confidence_level(confidence)
        n = array_scores(id, dataset_reviews)
        N = sum(n)
        first_part = 0
        second_part = 0
        for k, n_k in enumerate(n):
            first_part += (k+1)*(n[k]+1)/(N + 10)
            second_part += (k+1)*(k+1)*(n[k]+1)/(N+10)
        score = first_part - z*np.sqrt((second_part - first_part * first_part)/(N+11))
        
        return round(float(score), 2)    


'''Old code: '''
# Calculating the ratio for every game 
# def ratio_posreviews_allgames(dataset_ranks, dataset_reviews):
#         for id in dataset_ranks['ID']:
#             share_of_positive_reviews_per_game(dataset_ranks, dataset_reviews, id)

# My algorithm class:
# class ranking_algorithm():
    
#     # Attributes: a name and the input datasets

#     def __init__(self, name , dataset_ranks, dataset_reviews):
#         self.name = name
#         self.dataset_ranks = dataset_ranks
#         self.dataset_reviews = dataset_reviews
        

#     # These are my methods:
#     # this has dataset as its second argument
#     # Calculating the Total reviews:
#     def total_reviews(self, ID):
#         total_reviews = self.dataset_ranks['Number of Ratings']
#         total_reviews_ID = total_reviews.loc[(self.dataset_ranks['ID']== ID)]
#         return int(total_reviews_ID.iloc[0])

#     # Function to calculate any confidence level
#     def confidence_level(self, confidence):
#         cl = norm.ppf(1- (1 - confidence)/2)
#         return cl

# class Wilson_Function(ranking_algorithm):
    
#     def count_positive_reviews_per_game(self, ID):
        
#         df_positive_reviews = self.dataset_reviews.loc[(self.dataset_reviews["ID"] == ID) & (self.dataset_reviews['Rating'] >= 6.0)] 
#         # Loc Accesses a group of columns by labels and makes a new df
#         positive_reviews_count = df_positive_reviews['Rating'].count() 
#         # the variable counts every element in the df, so all the positive reviews
        
#         return int(positive_reviews_count)

#     # Ratio of positive review per total reviews
#     def share_of_positive_reviews_per_game(self, ID):
#         share_of_pos_reviews_per_game = float(self.count_positive_reviews_per_game(ID) / self.total_reviews(ID))
#         return round(share_of_pos_reviews_per_game, 4)

#     # Calculating the ratio for every game (Is this necessary?)
#     def ratio_posreviews_allgames(self):
#         for id in self.dataset_ranks['ID']:
#             self.share_of_positive_reviews_per_game(id)
    
#     # Wilson Function
#     def Wilson_Function(self, ID, confidence = .95):
#         z = self.confidence_level(confidence)
#         n = self.total_reviews(ID)
#         p_hat = 1 * self.share_of_positive_reviews_per_game(ID) #/ self.total_reviews(ID)
        
#         wilson_score = round(float((p_hat + z**2/(2*n) - z*np.sqrt((p_hat*(1 - p_hat) + z**2/(4*n))/n)) / (1 + (z**2)/n)), 2)
        
#         return wilson_score

# class Bayesian_Average(ranking_algorithm):

# # For Bayesian Lower Bound:

#     # Array Scores, returns the number of times a game received a certainscore (how many 1/10s, how many 2/10s...)
#     def array_scores(self, ID):
#         list_of_scores = []
#         for i in range(1,11):
#             how_many_i_reviews = self.dataset_reviews.loc[(self.dataset_reviews['ID'] == ID) & (self.dataset_reviews['Rating'].between(i, i + 1, inclusive='left'))]
#             this_many_i_reviews = how_many_i_reviews['Rating'].count()
            
#             list_of_scores.append(int(this_many_i_reviews))
            
#         return list_of_scores

#     # Bayesian lower bound function
#     def Bayesian_Average(self, ID, confidence = .95):
#         z = self.confidence_level(confidence)
#         n = self.array_scores(ID)
#         N = sum(n)
#         first_part = 0
#         second_part = 0
#         for k, n_k in enumerate(n):
#             first_part += (k+1)*(n[k]+1)/(N + 10)
#             second_part += (k+1)*(k+1)*(n[k]+1)/(N+10)
#         score = first_part - z*np.sqrt((second_part - first_part * first_part)/(N+11))
        
#         return round(float(score), 2)    

