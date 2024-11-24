import pandas as pd

class dataset_by_review_bracket():
    # Presentation of data functions: 
    def __init__(self, name, rank_database, reviews_database, algorithm, operator, num_of_reviews1):
        self.name = name
        self.rank_database = rank_database
        self.reviews_database = reviews_database
        self.algorithm = algorithm
        self.operator = operator
        self.num_of_reviews1 = num_of_reviews1
        
    
    def add_column_to_df_filtered_by_reviews(self, title_of_column = 'New Column', num_upperbound_reviews = None):
        
        ''' Function filters two dfs: the rank df by the desired number of reviews, and then the review df based on the items in the new rank df'''
        # filtering the rank database based on a preferred number/range of reviews
    
        if self.operator == 'equal':
            filtered_rank_data = self.rank_database[self.rank_database['Number of Ratings'] == self.num_of_reviews1]
        elif self.operator == 'greater':
            filtered_rank_data = self.rank_database[self.rank_database['Number of Ratings'] > self.num_of_reviews1]
        elif self.operator == 'between':
            filtered_rank_data = self.rank_database[self.rank_database['Number of Ratings'].between(self.num_of_reviews1, num_upperbound_reviews)]
        else:
            filtered_rank_data = self.rank_database[self.rank_database['Number of Ratings'] < self.num_of_reviews1]
         
        # filtering the review data based on the filtered rank database
        desired_ids = filtered_rank_data['ID']
        filtered_review_data =  self.reviews_database[self.reviews_database['ID'].isin(desired_ids)]
        
        # create an empty list (our future column)
        new_column = []
        # for each row in a dataset I have to find its ID and apply a the function over it
        for id in filtered_review_data['ID'].unique():
            new_column.append(self.algorithm(id, self.rank_database, self.reviews_database))
            
        filtered_rank_data.insert(0, title_of_column, new_column)
        
        
        return filtered_rank_data
    
    # sorting function:
    
    def sorting(self, dataset_to_sort, sort_by_variable, method_of_sorting):
        if method_of_sorting == 'Top'.lower():
            dataset_to_sort.sort_values(sort_by_variable, ascending = False)
        elif method_of_sorting == 'Bottom'.lower():
            dataset_to_sort.sort_values(sort_by_variable, ascending = True)
            
    
    # def filtering_data_by_review_number(self, operator, num_max_min_reviews, num_upperbound_reviews = None):   
        
    #     ''' Function filters two dfs: the rank df by the desired number of reviews, and then the review df based on the items in the new rank df'''
    #     # filtering the rank database based on a preferred number/range of reviews
    
    #     if operator == 'equal':
    #         filtered_rank_data = self.rank_database[self.rank_database['Number of Ratings'] == num_max_min_reviews]
    #     elif operator == 'greater':
    #         filtered_rank_data = self.rank_database[self.rank_database['Number of Ratings'] > num_max_min_reviews]
    #     elif operator == 'between':
    #         filtered_rank_data = self.rank_database[self.rank_database['Number of Ratings'].between(num_max_min_reviews,num_upperbound_reviews)]
    #     else:
    #         filtered_rank_data = self.rank_database[self.rank_database['Number of Ratings'] < num_max_min_reviews]
        
        
    #     # filtering the review data based on the filtered rank database
    #     desired_ids = filtered_rank_data['ID']
    #     filtered_review_data =  self.reviews_database[self.reviews_database['ID'].isin(desired_ids)]
        
        
        
    #     return filtered_review_data, filtered_rank_data
    
    #     # Adding a column to a dataset
    # def add_new_column_to_dataset(self, filtered_review_data, filtered_rank_data, function, title_of_column = 'New Column'):
        
    #     '''Applies a function over the review table and appends it over the filtered rank table'''
        
    #     # create an empty list (our future column)
    #     new_column = []
    #     # for each row in a dataset I have to find its ID and apply a the funciton over it
    #     for id in filtered_review_data['ID'].unique():
    #         new_column.append(function(id))
            
    #     filtered_rank_data.insert(0, title_of_column, new_column)
        
    #     # # sort
    #     # if sort is True:
    #     #     filtered_rank_data = filtered_rank_data.sort_values(new_column, ascending = False)
    #     return filtered_rank_data
    
    