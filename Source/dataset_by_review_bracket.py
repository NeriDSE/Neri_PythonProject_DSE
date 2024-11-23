class dataset_by_review_bracket():
    # Presentation of data functions: 
    def __init__(self, name, rank_database, reviews_database):
        self.name = name
        self.rank_database = rank_database
        self.reviews_database = reviews_database
    
    def filtering_data_by_review_number(self, operator, num_max_min_reviews, num_upperbound_reviews = None):    
        
        
        # filtering the rank database based on a preferred number/range of reviews
    
        if operator == 'equal':
            filtered_rank_data = self.rank_database[self.rank_database['Number_of_Ratings'] == num_max_min_reviews]
        elif operator == 'greater':
            filtered_rank_data = self.rank_database[self.rank_database['Number_of_Ratings'] > num_max_min_reviews]
        elif operator == 'between':
            filtered_rank_data = self.rank_database[self.rank_database['Number_of_Ratings'].between(num_max_min_reviews,num_upperbound_reviews)]
        else:
            filtered_rank_data = self.rank_database[self.rank_database['Number_of_Ratings'] < num_max_min_reviews]
        
        
        # filtering the review data based on the filtered rank database
        desired_ids = filtered_rank_data['ID']
        filtered_review_data =  self.reviews_database[self.reviews_database['ID'].isin(desired_ids)]
        
        
        
        return filtered_review_data, filtered_rank_data
    
        # Adding a column to a dataset
    def add_new_column_to_dataset(self, filtered_review_data, filtered_rank_data, function, title_of_column = 'New Column', sort = True):
        # create an empty list (our future column)
        New_column = []
        # for each row in a dataset I have to find its ID and apply a the funciton over it
        for id in filtered_review_data['ID'].unique():
            New_column.append(function(id))
            
        filtered_rank_data.insert(0, title_of_column, New_column)
        
        # sort
        if sort == True:
            filtered_rank_data = filtered_rank_data.sort_values(New_column, ascending = False)
        else:
            filtered_rank_data = filtered_rank_data
            
        return filtered_rank_data
    
    