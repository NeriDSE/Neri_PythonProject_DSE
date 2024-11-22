# # The BoardGameGeek (BGG) (https://boardgamegeek.com/wiki/page/Guide_to_Database_Corrections#toc18) provides various data and statistics 
# on the enthusiastic board game hobby. 
# BGG users comment on games and optionally assign them a liking score between 0 and 10.

# The PURPOSE of the project is to produce a ranking of games in order of user liking.
 
# 1. Rank the dataset in a traditional sense
# 
# 
# 2. It should be noted that in order to obtain an adequate ranking it is necessary to consider not only the votes, 
# but also the fact that different games may be associated with very different numbers of comments and thus
# votes from individual users. 
# For a discussion of this point see, for example, How Not To Sort By Average Rating.

# 3. The project should propose its OWN strategy for sorting the games.
# also arguing its appropriateness in relation to the official BGG ranking, available online.

# 4. The project should also produce graphs comparing the proposed ranking with the ranking obtained 
# only through the average rating of each game, showing the different distribution of scores and the differences found.

import pandas as pd
import numpy as np
import csv
import streamlit as st

file_name = "2022-01-08.csv" 
dataset = pd.read_csv(file_name)






sum(dataset.duplicated())

# Cleaned data, took out the url and thumbnail columns

clean_data  = dataset.drop(["URL", "Thumbnail"], axis = 1) 
clean_data = clean_data.rename(columns = {"Unnamed: 0" : "Game Index", "Bayes average": "Bayes Average", "Users rated" : "Users Rated"})
clean_data

