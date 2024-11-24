import dataset_by_review_bracket as rb
import ranking_algorithms as ra
import graph as gr
from Source.data_processing import clean_rank_data, clean_review_data




# presentation should be something I zoom through... first thing tomorrow

# round1 of explanations

# more data cleaning shit...
# name of df kind of useless... I'm taking it out tomorrow

# streamlit fix, actually way simpler with this function... I just run this shit.. saves me FOREVER... literally. so close to being done...

    
def ranking_algorithm_by_reviews(ranking_algorithm, name_df, operator, num_of_reviews1, title_graph):
    '''Filters datasets by number of reviews and adds a new column to them with a specified new value, sorting by that value or not that value'''
    
    if ranking_algorithm == 'Wilson Score'.lower():
        name_df1 = rb.dataset_by_review_bracket(name_df, clean_rank_data, clean_review_data, ra.wilson_function, operator, num_of_reviews1)    
        name_df2 = name_df1.add_column_to_df_filtered_by_reviews('Wilson function')
        name_df2 = name_df2.sort_values('Wilson function', ascending = False)
        graph_setup = gr.graph(name_df, name_df2, 'Wilson function', 'n')
        graph_of_alg = graph_setup.horizontal_bar_graph(title_graph)
        
    elif ranking_algorithm =='Bayesian'.lower():
        name_df1 = rb.dataset_by_review_bracket(name_df, clean_rank_data, clean_review_data, ra.bayesian_average, operator, num_of_reviews1)    
        name_df2 = name_df1.add_column_to_df_filtered_by_reviews('New Bayesian Average')
        name_df2 = name_df2.sort_values('New Bayesian Average', ascending = False)
        graph_setup = gr.graph(name_df, name_df2, 'New Bayesian Average', 'n')
        graph_of_alg = graph_setup.horizontal_bar_graph(title_graph)
        
    elif ranking_algorithm == 'Average'.lower():
        name_df1 = rb.dataset_by_review_bracket(name_df, clean_rank_data, clean_review_data, None , operator, num_of_reviews1)
        name_df2 =  name_df1.add_column_to_df_filtered_by_reviews('Average', 'n')
        name_df2 = name_df2.sort_values('Average', ascending = False)
        graph_setup = gr.graph(name_df, name_df2, 'Average', 'n')
        graph_of_alg = graph_setup.horizontal_bar_graph(title_graph, 'orange')
        
    else:
        raise ValueError('Please enter a valid ranking algorithm name among "Wilson Function", "New Bayesian Average", and "Average"')
        
        
    return  graph_of_alg, name_df2

