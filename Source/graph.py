import matplotlib as plt
import numpy as np

class graph():
    def __init__(self, name, dataset):
        self.name = name
        self.dataset = dataset
    # Plotting the New_Bayesian_Average vs the common average for the top rated games (explain it better, idk what tf this means)
    
    def horizontal_bar_graph(self, sortby_variable, graph_title, y_labels = 'Name', top_color = 'red' ):
    # data
        sorted_reviews = self.dataset.sort_values(sortby_variable, ascending = False)
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