import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as mpl


# My algorithm class:
class ranking_algorithm():
    
    # Attributes: a name and the input datasets

    def __init__(self, name = None, dataset_ranks, dataset_reviews):
        self.name = name
        self.dataset_ranks = None
        self.dataset_reviews = None
        

    # These are my methods:
    
    # Calculating the Total reviews:
    def total_reviews(self, dataset, ID):
        total_reviews = dataset['Number_of_Ratings']
        total_reviews_ID = total_reviews.loc[(dataset['ID']== ID)]
        return int(total_reviews_ID.iloc[0])

    # Function to calculate any confidence level
    def confidence_level(self, confidence):
        cl = norm.ppf(1- (1 - confidence)/2)
        return cl

# Presentation of data functions: 

    # Adding a column to a dataset
    def add_new_column_to_dataset(self, dataset_input, dataset_output, function, title_of_column = 'New Column'):
        # create an empty list (our future column)
        New_column = []
        # for each row in a dataset I have to find its ID and apply a the funciton over it
        for id in dataset_input['ID'].unique():
            New_column.append(function(id))
            
        dataset_output.insert(0, title_of_column, New_column)
        
        return dataset_output

    # A function that filters a rank database based on the number of reviews it's had (many, very few, somewhere in the middle)

    def clean_review_data_x_reviewed(self, rank_database, operator, reviews, reviews_2 = None):
        if operator == 'equal':
            x_reviewed_database = rank_database[rank_database['Number_of_Ratings'] == reviews]
        elif operator == 'greater':
            x_reviewed_database = rank_database[rank_database['Number_of_Ratings'] > reviews]
        elif operator == 'between':
            x_reviewed_database = rank_database[rank_database['Number_of_Ratings'].between(reviews, reviews_2)]
        else:
            x_reviewed_database = rank_database[rank_database['Number_of_Ratings'] < reviews]
        return x_reviewed_database
    
    # A function that filters the review database based on the rank database (so to get the individual scores for each game that I can then use for the bayesian method)
    def filtered_data_by_review(self, rank_by_review_data, reviews_database):    
        desired_ids = rank_by_review_data['ID']
        
        clean_review_data_x_reviewed =  reviews_database[ reviews_database['ID'].isin(desired_ids)]
        return clean_review_data_x_reviewed
    

class Wilson_Function(ranking_algorithm):
    
    def count_positive_reviews_per_game(self, dataset, ID):
        
        df_positive_reviews = dataset.loc[(dataset["ID"] == ID) & (dataset['Rating'] >= 6.0)] 
        # Loc Accesses a group of columns by labels and makes a new df
        positive_reviews_count = df_positive_reviews['Rating'].count() 
        # the variable counts every element in the df, so all the positive reviews
        
        return int(positive_reviews_count)

    # Ratio of positive review per total reviews
    def share_of_positive_reviews_per_game(self, ID, dataset):
        share_of_pos_reviews_per_game = float(self.count_positive_reviews_per_game(dataset, ID) / self.total_reviews(dataset, ID))
        return round(share_of_pos_reviews_per_game, 4)

    # Calculating the ratio for every game (Is this necessary?)
    def ratio_posreviews_allgames(self, dataset):
        for id in dataset['ID']:
            self.share_of_positive_reviews_per_game(id)
    
    # Wilson Function
    def Wilson_Function(self, ID, dataset, confidence = .95):
        z = self.confidence_level(confidence)
        n = self.total_reviews(dataset, ID)
        p_hat = 1 * self.share_of_positive_reviews_per_game(ID) #/ total_reviews(clean_data, ID)
        
        wilson_score = round(float((p_hat + z**2/(2*n) - z*np.sqrt((p_hat*(1 - p_hat) + z**2/(4*n))/n)) / (1 + (z**2)/n)), 2)
        
        return wilson_score

class Bayesian_Average(ranking_algorithm):

# For Bayesian Lower Bound:

    # Array Scores, returns the number of times a game received a certainscore (how many 1/10s, how many 2/10s...)
    def array_scores(self, dataset, ID):
        list_of_scores = []
        for i in range(1,11):
            how_many_i_reviews = dataset.loc[(dataset['ID'] == ID) & (dataset['Rating'].between(i, i + 1, inclusive='left'))]
            this_many_i_reviews =how_many_i_reviews['Rating'].count()
            
            list_of_scores.append(int(this_many_i_reviews))
            
        return list_of_scores

    # Bayesian lower bound function
    def Bayesian_Average(self, ID, dataset, confidence = .95):
        z = self.confidence_level(confidence)
        n = self.array_scores(dataset, ID)
        N = sum(n)
        first_part = 0
        second_part = 0
        for k, n_k in enumerate(n):
            first_part += (k+1)*(n[k]+1)/(N + 10)
            second_part += (k+1)*(k+1)*(n[k]+1)/(N+10)
        score = first_part - z*np.sqrt((second_part - first_part*first_part)/(N+11))
        
        return round(float(score), 2)    





# graphing object, these are both possibilities.


class graph():
    def __init__(self, name) # do I put the same shit as the stuff below??

    # Plotting the New_Bayesian_Average vs the common average for the top rated games (explain it better, idk what tf this means)
    
    def horizontal_bar_graph(dataset, sortby_variable, graph_title, y_labels = 'Name', top_color = 'red' ):
    # data
        sorted_reviews = dataset.sort_values(sortby_variable, ascending = False)
        sorting_by_variable = sorted_reviews[sortby_variable].iloc[0:10]
        displayed_titles = sorted_reviews[y_labels].iloc[0:10]
        
        colors = [top_color,'blue','blue','blue','blue','blue','blue','blue','blue','blue' ]
        pos = np.arange(len(displayed_titles))
        
        plt.style.use('_mpl-gallery')
        # plot
        fig, ax = plt.subplots() 

        ax.barh(pos, sorting_by_variable, align = 'center', edgecolor = 'black', color = colors )
        ax.set_yticks(pos, labels = displayed_titles)
        ax.invert_yaxis()
        ax.set_xlabel(sortby_variable)
        ax.set_title(graph_title)
        
        return plt.show()

