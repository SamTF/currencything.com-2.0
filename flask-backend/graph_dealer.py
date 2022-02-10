# IMPORTS
import matplotlib.pyplot as plt
import pandas as pd


### CONSTANTS
GRAPH_DIR = '../svelte-frontend/static/graphs/{}.svg'


###### HELPER FUNCTIONS ##############################################################################################################
# Helper function - Converts the dates from Datetime to a readable string
def format_dates(array):
    dates_formatted = []                # temp array to store format dates
    for date in array:                  # loops thru all dates
        d = pd.to_datetime(str(date))   # converts from numpy's datetime format to string
        d = d.strftime('%-d/%-m/%y')    # the dash - removes leading zeros
        dates_formatted.append(d)       # adds the formatted dates to the temp array
    
    return dates_formatted              # outputs the formatted array


###### ACTUAL GRAPHING ##############################################################################################################
def plot_line_chart(data: pd.DataFrame, file_name: str, title: str, xlabel: str = '# Of Trades', ylabel: str = '₡urrency Things', date_index:bool = False) -> str:
    '''
    Generic plotting function for a line chart. Plots a DataFrame with the index as the X values and the SIZE column as the Y values.
    Save the graph as an SVG and returns the its file name.

    data: Pandas DataFrame with the values to plot. Must contain a SIZE column.
    file_name: Name to save the SVG as.
    title: The title of the graph.
    xlabel: Label for the X-axis.
    ylabel: Label for the Y-axis.
    date_index: Whether the x-axis values are dates. 
    '''
    # setting the graph size
    plt.figure(figsize=(8,6), dpi=150)

    # formats dates nicely if the axis values are indeed dates
    xaxis = data.index if not date_index else format_dates(data.index)

    # getting appropriate Y-data
    yaxis = data.SIZE if 'SIZE' in data else data.SUPPLY

    # plotting the values 
    plt.plot(xaxis, yaxis, c='xkcd:hot pink', linewidth = 0)
    plt.fill_between(xaxis, yaxis, facecolor = 'xkcd:hot pink')     # filling the area under the line to make it look nice - > bloomberg.py

    # Titles
    plt.title(title,    fontdict={'fontname': 'Comic Sans MS', 'fontsize': 20, 'color': 'white'})
    plt.xlabel(xlabel,  fontdict={'fontname': 'Comic Sans MS', 'fontsize': 12, 'color': 'white'})
    plt.ylabel(ylabel,  fontdict={'fontsize': 12, 'color': 'white'})

    # Customising Colours                        - background, borders, tick markers
    ax = plt.gca()                               # gets the axes somehow, i dunno what this does
    ax.set_facecolor('black')                    # background colour
    ax.spines['bottom'].set_color('white')       # x-axis border colour
    ax.spines['left'].set_color('white')         # y-axis border colour
    ax.tick_params(colors="white", labelsize=10) # colour and size of the tick markers

    # Amount of ticks
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))  # sets a maximum amount of 6 ticks on the X Axis

    # Saving the graph as an SVG
    plt.savefig(GRAPH_DIR.format(file_name), transparent=True)

    # Closing any open figures from memory
    plt.close('all')

    return file_name


if __name__ == '__main__':
    from explorer import Explorer
    ex = Explorer()
    data = ex.supply_over_time()

    print(data)

    g = plot_line_chart(data, 'supply', 'Supply Over Time', 'Time', date_index=True)
    print(g)