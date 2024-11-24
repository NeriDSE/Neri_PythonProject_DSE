import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib as plt
import streamlit as st # should I keep this here?
import os
import dataset_by_review_bracket as rb
import ranking_algorithms as ra
import graph
from data_cleaning import clean_rank_data, clean_review_data


# filtering the dataframes and creating a new column with a desired ranking algorithm.

filtered_dataset_by_wilson = rb.dataset_by_review_bracket('most_reviewed', clean_rank_data, clean_review_data, ra.wilson_function, 'greater', 80000)
most_reviewed_games_by_wilson = filtered_dataset_by_wilson.add_column_to_df_filtered_by_reviews('Wilson function')
most_reviewed_games_by_wilson.sort_values('Wilson function', ascending = False)

filtered_dataset_by_bayes = rb.dataset_by_review_bracket('in between reviewed', clean_rank_data, clean_review_data, ra.bayesian_average, 'between', 3900)
mid_reviewed_games_by_bayes = filtered_dataset_by_bayes.add_column_to_df_filtered_by_reviews('New Bayesian Average', 4000)
mid_reviewed_games_by_bayes.sort_values('New Bayesian Average', ascending = False)
# graphs here