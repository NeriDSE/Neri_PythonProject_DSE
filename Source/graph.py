import matplotlib.pyplot as plt
import numpy as np

class graph():
    def __init__(self, name, dataset, sortby_variable, ascending):
        self.name = name
        self.dataset = dataset
        self.sortby_variable = sortby_variable
        self.ascending = ascending
        

    # Plotting the New_Bayesian_Average vs the common average for the top rated games (explain it better, idk what tf this means)
    
    def horizontal_bar_graph(self, graph_title, top_color = 'red', y_labels = 'Name' ):
        '''Method plots a top 10 Horizontal Bar Plot'''
    # data
        if self.ascending.lower() == 'n':
              ascending_order = False
        elif self.ascending.lower() == 'y':
            ascending_order = True
        else:
            raise ValueError("Unacceptable Value for 'ascending'. Use 'y' for ascending or 'n' for descending.")
        
        sorted_reviews = self.dataset.sort_values(self.sortby_variable, ascending = ascending_order)
        sorting_by_variable = sorted_reviews[self.sortby_variable].iloc[0:10]
        displayed_titles = sorted_reviews[y_labels].iloc[0:10]
        
        colors = [top_color,'blue','blue','blue','blue','blue','blue','blue','blue','blue' ]
        pos = np.arange(len(displayed_titles))
        
        plt.style.use('_mpl-gallery')
        # plot
        fig, ax = plt.subplots() 

        ax.barh(pos, sorting_by_variable, align = 'center', edgecolor = 'black', color = colors )
        ax.set_yticks(pos, labels = displayed_titles)
        ax.invert_yaxis()
        ax.set_xlabel(self.sortby_variable)
        ax.set_title(graph_title)
        
        return plt.show()
    
    # will it work for a top 10??
    # will I get a decent grade?