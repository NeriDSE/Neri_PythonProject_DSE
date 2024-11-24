import streamlit as st
import pandas as pd
import os
import ranking_algorithms as ra
import dataset_by_review_bracket as rb
import graph as gr
# from data_processing import clean_rank_data, clean_review_data



data_path = os.path.join(os.getcwd(), 'Source\data')

rank_file = "2022-01-08.csv" 
dataset_ranks = pd.read_csv(f'{data_path}\{rank_file}')
clean_rank_data  = dataset_ranks.drop(["URL", "Thumbnail", "Unnamed: 0", "Bayes average", 'Year'], axis = 1) 
clean_rank_data = clean_rank_data.rename(columns = {"Users rated" : "Number of Ratings"})

file_reviews = "bgg-19m-reviews.csv" # second dataset
dataset_reviews = pd.read_csv(f'{data_path}\{file_reviews}')
clean_review_data = dataset_reviews.drop(["Unnamed: 0", "comment"], axis = 1)
clean_review_data = clean_review_data.rename(columns = {"user":"User", "rating":"Rating", "name" : "Name_of_Game"})

image = 'boardgame.jpg' 
st.image(f'{data_path}\{image}')
st.title("Welcome to the Ranking Board App! 🎲")
st.markdown("Discover ways to compare the rankings of your favorite board games")


# display all of my cleaned datasets
st.markdown("*The datasets:*")
st.write('First of all, a glimpse into the Rank dataset')
st.write(clean_rank_data.head(5))

st.write(' Then, a glimpse into the Reviews dataset')

st.write(clean_review_data.head(5))

st.markdown("*The algorithms:*")
algorithms = ['Wilson Function', 'New Bayesian Average', 'Arithmetic Mean']
selectbox_algorithms = st.selectbox('Choose between one of the algorithms', algorithms)
games = clean_rank_data['Name']
selectbox_name = st.selectbox('Choose a game', games)

def name_to_x(name, column_to_match):
        name_to_x_index = clean_rank_data.loc[clean_rank_data['Name'] == name, column_to_match]
        name_to_x = int(name_to_x_index.iloc[0])
        return name_to_x



if selectbox_algorithms =='Wilson Function':
        st.write(f'The Wilson Score of {selectbox_name} is:', ra.wilson_function(name_to_x(selectbox_name, 'ID'), clean_rank_data, clean_review_data))
elif selectbox_algorithms == 'New Bayesian Average':
        st.write(f'The New Bayesian Score of {selectbox_name} is:', ra.bayesian_average(name_to_x(selectbox_name, 'ID'), clean_rank_data, clean_review_data))
elif selectbox_algorithms == 'Arithmetic Mean':
        st.write(f'The Arithmetic Mean of {selectbox_name} is:', name_to_x(selectbox_name, 'ID'))
else:
        st.write('Please enter a valid ranking algorithm and or a valid game')
        
        
st.write("You can filter the rank dataset based on how the previously chosen algorithm and the number of reviews each game's received ")

list_reviewed = ['Most reviewed', 'Least reviewed', 'a Middle ground']
selectbox_filtered = st.selectbox('How many reviews would you like your game to have?', list_reviewed )

filtered_by_wilson = rb.dataset_by_review_bracket('most_reviewed', clean_rank_data, clean_review_data, ra.wilson_function, 'greater', 50000)
most_by_wilson = filtered_by_wilson.add_column_to_df_filtered_by_reviews('Wilson function')
graph1 = gr.graph('Most reviewed by wilson', most_by_wilson, 'Wilson function', 'n') 
    
filtered_by_wilson = rb.dataset_by_review_bracket('least_reviewed', clean_rank_data, clean_review_data, ra.wilson_function, 'equal', 50)
least_by_wilson = filtered_by_wilson.add_column_to_df_filtered_by_reviews('Wilson function')
graph2 = gr.graph('Least reviewed by wilson', least_by_wilson, 'Wilson function', 'n')

         
filtered_by_wilson = rb.dataset_by_review_bracket('mid_reviewed', clean_rank_data, clean_review_data, ra.wilson_function, 'between', 3700)
middle_by_wilson = filtered_by_wilson.add_column_to_df_filtered_by_reviews('Wilson function', 4000)
graph3 = gr.graph('Middle reviewed by wilson', middle_by_wilson, 'Wilson function', 'n')

filtered_by_bayes = rb.dataset_by_review_bracket('most_reviewed', clean_rank_data, clean_review_data, ra.wilson_function, 'greater', 50000)
most_by_bayes = filtered_by_bayes.add_column_to_df_filtered_by_reviews('New Bayesian Average')
graph4 = gr.graph('Most reviewed by Bayes', most_by_bayes, 'New Bayesian Average', 'n')

filtered_by_bayes = rb.dataset_by_review_bracket('least_reviewed', clean_rank_data, clean_review_data, ra.wilson_function, 'equal', 50)
least_by_bayes = filtered_by_bayes.add_column_to_df_filtered_by_reviews('New Bayesian Average')
graph5 = gr.graph('Least reviewed by Bayes', least_by_bayes, 'New Bayesian Average', 'n')

filtered_by_bayes = rb.dataset_by_review_bracket('mid_reviewed', clean_rank_data, clean_review_data, ra.wilson_function, 'between', 3700)
middle_by_bayes = filtered_by_bayes.add_column_to_df_filtered_by_reviews('New Bayesian Average', 4000)
graph6 = gr.graph('Mid reviewed by Bayes', middle_by_bayes, 'New Bayesian Average', 'n')

filtered_by_mean = rb.dataset_by_review_bracket('most_reviewed', clean_rank_data, clean_review_data, ra.wilson_function, 'greater', 50000)
graph7 = gr.graph('Most reviewed by Mean', filtered_by_mean, 'Average', 'n')

filtered_by_mean = rb.dataset_by_review_bracket('least_reviewed', clean_rank_data, clean_review_data, ra.wilson_function, 'equal', 50)
graph8 = gr.graph('Least reviewed by Mean', filtered_by_mean, 'Average', 'n')

filtered_by_mean = rb.dataset_by_review_bracket('mid_reviewed', clean_rank_data, clean_review_data, ra.wilson_function, 'between', 3700)
graph9 = gr.graph('Mid reviewed by Mean', filtered_by_mean, 'Average', 'n')

if selectbox_algorithms == 'Wilson Function':
        if selectbox_filtered == 'Most reviewed':
                
                st.write('Here is your filtered dataframe')
                st.write(most_by_wilson.sort_values('Wilson function', ascending = False))
                st.pyplot(graph1.horizontal_bar_graph('Wilson based ranking, 50k+ reviews'))
                
        elif selectbox_filtered == 'Least reviewed':
                st.write('Here is your filtered dataframe', least_by_wilson.sort_values('Wilson function', ascending = False))
                st.pyplot(graph2.horizontal_bar_graph('Wilson based ranking, 50 reviews'))
        elif selectbox_filtered == 'a Middle ground':
                st.write('Here is your filtered dataframe', middle_by_wilson.sort_values('Wilson function', ascending = False))
                st.pyplot(graph3.horizontal_bar_graph('Wilson based ranking, between 3700 and 4000 reviews'))
        else:
                st.write('An error occurred, please select a valid option')
                
elif selectbox_algorithms == 'New Bayesian Average':
        if selectbox_filtered == 'Most reviewed':
                st.write('Here is your filtered dataframe', most_by_bayes.sort_values('New Bayesian Average', ascending = False))
                st.pyplot(graph4.horizontal_bar_graph('Bayes based ranking, 50k+ reviews'))
        elif selectbox_filtered == 'Least reviewed':
                
                st.write('Here is your filtered dataframe', least_by_bayes.sort_values('New Bayesian Average', ascending = False))
                st.pyplot(graph5.horizontal_bar_graph('Bayes based ranking, 50 reviews'))
        elif selectbox_filtered == 'a Middle ground':
                st.write('Here is your filtered dataframe', middle_by_bayes.sort_values('New Bayesian Average', ascending = False))
                st.pyplot(graph6.horizontal_bar_graph('Bayes based ranking between 3700 and 4000 reviews'))      
        else:
                st.write('An error occurred, please select a valid option')
elif selectbox_algorithms == 'Arithmetic Mean':
        if selectbox_filtered == 'Most reviewed':
                st.write('Here is your filtered dataframe', filtered_by_mean.sort_values('Mean', ascending = False))
                st.pyplot(graph7.horizontal_bar_graph('Mean based ranking, 50k+ reviews'))        
        elif selectbox_filtered == 'Least reviewed':
                st.write('Here is your filtered dataframe', filtered_by_mean.sort_values('Mean', ascending = False))
                st.pyplot(graph8.horizontal_bar_graph('Mean based ranking, 50 reviews'))        
        elif selectbox_filtered == 'a Middle ground':
                
                st.write('Here is your filtered dataframe', filtered_by_mean.sort_values('Mean', ascending = False))       
                st.pyplot(graph9.horizontal_bar_graph('Mean based ranking, between 3700 and 4000 reviews'))                     # these have to be properly segmented jesus lord christ superstar.
                          
        
