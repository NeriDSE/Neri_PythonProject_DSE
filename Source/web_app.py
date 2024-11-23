import streamlit as st
import pandas as pd
import duckdb
import os
import functions as f


data_path = os.path.join(os.getcwd(), 'Source\data')
image = 'boardgame.jpg'
st.image(f'{data_path}\{image}')
st.title("Welcome to the Ranking Board App! 🎲")
st.markdown("Discover ways to compare the rankings of your favorite board games")

# importing and cleaning data:
rank_file = "2022-01-08.csv" 
dataset = pd.read_csv(f'{data_path}\{rank_file}')
clean_rank_data  = dataset.drop(["URL", "Thumbnail", "Unnamed: 0", "Bayes average", 'Year'], axis = 1) 
clean_rank_data = clean_rank_data.rename(columns = {"Users rated" : "Number of Ratings"})

file_reviews = "bgg-19m-reviews.csv" # second dataset
dataset_reviews = pd.read_csv(f'{data_path}/{file_reviews}')
clean_review_data = dataset_reviews.drop(["Unnamed: 0", "comment"], axis = 1)
clean_review_data = clean_review_data.rename(columns = {"user":"User", "rating":"Rating", "name" : "Name_of_Game"})


# most_reviewed_games.sort_values('New_Bayesian_Average', ascending = False)


list_reviewed = ['Most reviewed (25k+)', 'Least reviewed (50 reviews)', 'In between (3500-4000)']
selectbox = st.selectbox('How many reviews do you want your games to have', list_reviewed )

# for i in list_reviewed:
#     if i == selectbox:
#         x_reviewed_games = f.clean_review_data_x_reviewed(clean_rank_data, 'greater', 25000)
#         f.add_new_column_to_dataset(f.filtered_data_by_review(clean_rank_data, clean_review_data),  x_reviewed_games, f.Bayesian_Average, 'New_Bayesian_Average')
#     elif:
    
#     else:
        
        # This should display the dataset of the games. So I guess I have to put them in here.
        
# then I figure out how to put all the graphs in the right place.

# I want it to display the different graphs 
#  also the different rankings

# I think I can just pass my program in a straightforward way
# rank it, show the top 10, show the graph, 
# maybe a comparison and the picture of the winner.

# I can do this in different pages although I'm not sure as to why.
