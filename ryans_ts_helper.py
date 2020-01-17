def growth_rates(df):
    """Add 4 growth rate columns ('total', '5yr_growth', '3yr_growth', '1yr_growth') to a dataframe. 
       Dataframe must have columns with montlhy dates from 2009-01 to 2018-04"""
    
    # Determine the change in values from the beggining to the end of the time period     
    df['total_growth'] = (df['2018-04'] - df['2009-01']) / df['2009-01']
    
    # Determine the change in values over the last five years     
    df['5yr_growth'] = (df['2018-04'] - df['2013-04']) / df['2013-04']

    # Determine the change in values over the last three years
    df['3yr_growth'] = (df['2018-04'] - df['2015-04']) / df['2015-04']

    # Determine the change in values over the last year    
    df['1yr_growth'] = (df['2018-04'] - df['2017-04']) / df['2017-04']
    

def top_growth_cities(df):
    """Enter a dataframe with total, 5yr, 3yr, and 1yr growth rates and return a set of cities that
       represent the top 5 for each growth period."""
    
    # Sort values by greatest total growth rates and return the top 5    
    top_total = list(df.sort_values('total_growth', ascending=False)['city_zipcode'].values[:5])
    
    # Sort values by greatest 5 year growth rates and return the top 5    
    top_5yr = list(df.sort_values('5yr_growth', ascending=False)['city_zipcode'].values[:5])

    # Sort values by greatest 3 year growth rates and return the top 5        
    top_3yr = list(df.sort_values('3yr_growth', ascending=False)['city_zipcode'].values[:5])

    # Sort values by greatest 1 year growth rates and return the top 5        
    top_1yr = list(df.sort_values('1yr_growth', ascending=False)['city_zipcode'].values[:5])
    
    # create a unique set of citied 
    top_cities = set(top_total + top_5yr + top_3yr + top_1yr)
    
    # return a dataframe that only includes cities in the top_cities set     
    return df[df['city_zipcode'].isin(top_cities)]


def stacked_growth(df):
    """Plot the growth rates of all cities in a dataframe in clustered bar chart,
       along with the mean growth rates of all cities, ordered from left to right by 
       1yr_growth rate."""
    
    # keys for columns to plot from the dataframe   
    grow_rates = ['total_growth', '5yr_growth', '3yr_growth', '1yr_growth']

    # get the mean growth rate for each time period      
    means = [df[i].mean() for i in grow_rates]

    # colors to assign horizontal lines
    colors = ['blue', 'red', 'gold', 'green']

    #plot clustered cities 
    fig = plt.figure(figsize=(26, 8))

    # sort by 1yr growth and plot clustered bar chart    
    df.sort_values('1yr_growth').plot(x= 'city_zipcode', y = grow_rates, kind='bar', figsize=(16, 8))
    
    # plot growth rate means as horizontal lines
    plt.hlines(y= means, xmin=-1, xmax=len(df), color=colors, label=('Mean growth'))
    
    plt.legend()
    plt.title('City_zipcode Growth Rates')
    
    plt.show()

    
def graph_growth(df):
    """Plot the total, 5yr, 3yr, and 1yr growth rates for each city in the data frame in 
       individual bar charts. Plot a horixontal line that represents the mean.""" 
    
    
    f = plt.figure(figsize= ( 16, 16))
    # create space between plots
    plt.subplots_adjust(hspace= .5)

    # set the value for x to the key for the city name in the dataframe
    x = 'city_zipcode'
    # set the lenth of the horizintal line 
    x_len = len(df)

    # plot total growth     
    ax1 = f.add_subplot(2,2,1)
    df.sort_values('total_growth').plot(x=x, y='total_growth', kind='bar', ax=ax1)
    plt.hlines(y=df.total_growth.mean(), xmin=0, xmax=x_len, label=('Mean Total Growth'))
    plt.title('Total Growth')
    plt.legend()

    # plot 5yr growth
    ax2 = f.add_subplot(2,2,2)
    df.sort_values('5yr_growth').plot(x=x, y='5yr_growth', kind='bar', ax=ax2)
    plt.hlines(y=df['5yr_growth'].mean(), xmin=0, xmax=x_len, label=('Mean 5-year Growth'))
    plt.title('5-year Growth')
    plt.legend()

    # plot 3yr growth
    ax3 = f.add_subplot(2,2,3)
    df.sort_values('3yr_growth').plot(x=x, y='3yr_growth', kind='bar', ax=ax3)
    plt.hlines(y=df['3yr_growth'].mean(), xmin=0, xmax=x_len, label=('Mean 3-year Growth'))
    plt.title('3-year Growth')
    plt.legend()

    # plot 1yr growth
    ax4 = f.add_subplot(2,2,4)
    df.sort_values('1yr_growth').plot(x=x, y='1yr_growth', kind='bar', ax=ax4)
    plt.hlines(y=df['1yr_growth'].mean(), xmin=0, xmax=x_len, label=('Mean 1-year Growth'))
    plt.title('1-year Growth')
    plt.legend()
    
    plt.show()   


def melt_data(df):
    """takes a dataframe and converts value data stored horizontally to a 
       vertical time series and change the index to datetime"""

    #drop unnecessary columns     
    df = df.drop(columns=['SizeRank', 'total_growth', '5yr_growth', '3yr_growth', '1yr_growth']).copy()
    
    # melt data to covert to value to a vertical orientation
    melted = pd.melt(df, id_vars=['city_zipcode', 'State', 'Metro', 'CountyName'], var_name='time')
    # convert 'time' to datetime
    
    melted['time'] = pd.to_datetime(melted['time'], infer_datetime_format=True)
    
    # make 'time' the index
    melted.set_index('time', inplace=True)
    
    # return the new time series dataframe
    return melted


def YoY_change(ts_dict):
    """take a dictionary of monthly time series dataframes and
       creates a column with the YoY change in value for
       each key:value pair"""
    
    # iterate through each key and calculate the percent change in each value 
    # over the last 12 month period
    for v in ts_dict:
        df = ts_dict[v]
        df['YoY_change'] = df.value.pct_change(periods=12)


def YoY_rate_o_change(ts_dict):
    """take a dictionary of monthly time series dataframes and
       creates a column with the YoY rate of change in value for
       each key:value pair"""

    # iterate through each key and calculate the differnce in each YoY change 
    # over the last 3 periods
    for v in ts_dict:
        df = ts_dict[v]
        df['YoY_rate_change'] = df.YoY_change.diff(periods=3)


def get_time_series(df):
    """takes a dataframe and returns a dictionary with unique city names as 
       keys and a dataframe for that city as a value. Also calulates new values
       'YoY_change' and 'YoY_rate_o_change' and adds new columns"""
    
    # create keys to use in new dictionary
    list_of_cities = list(df.city_zipcode)
    
    # create an empty dictionary to populate
    time_series_dict = {}
    
    # iterate through the list of cities and create new key:value pairs for city and city data
    for c in list_of_cities:
        time_series_dict[c] = melt_data(df[df['city_zipcode'] == c])
    
    # calculate YoY change in value for each city
    YoY_change(time_series_dict)
    
    # calcualte YoY rate of change for each city
    YoY_rate_o_change(time_series_dict)
    
    # return a dictionary with cities and city data
    return time_series_dict


def plot_time_series(ts, variable):
    """takes a dictionary of time series data frames and plots a 
        chosen variable (ex. 'value') in a series of subplots"""
    
    # creat figure and space between subplots
    fig = plt.figure(figsize=(20,18))
    plt.subplots_adjust(hspace= .5)
    
    # determine the number of subplots to create
    nrows = len(ts)//3 + 1
    ncols = 3
    
    # use dict keys as plot titles
    titles = list(ts.keys())
    
    # iterate through dict and plot each plot in a new sub plot 
    for i,v in enumerate(ts):
        ax = fig.add_subplot(nrows, ncols, i+1)
        ts[v][variable].plot(label=variable, ax=ax)
        plt.title(titles[i])
        plt.ylabel(variable)
        
    plt.show()


def plot_time_series2(ts):
    """takes a dictionary of time series dataframes and makes three plots 
       for each key:value pair: 'value', YoY_change', and 'YoY_rate_change'"""
    
    # creat figure and space between subplots
    fig = plt.figure(figsize=(16,40))
    plt.subplots_adjust(hspace= 1)
    
    # create subplot values
    nrows = len(ts)
    ncols = 3
    
    # use dict keys as plot titles
    titles = list(ts.keys())
    
    # columns to plot from eact dataframe
    variables = ['value', 'YoY_change', 'YoY_rate_change']
    
    # set base value to iterate on for axes
    axs = 0
    
    # iterate through each key:value pair and each variable to plot
    # enumerate to use as axes values
    for i,v in enumerate(ts):
        for x in variables:
            axs += 1 
            ax = fig.add_subplot(nrows, ncols, axs)
            ts[v][x].plot(label=x, ax=ax)
            plt.title(titles[i] + '_' + x)
            plt.ylabel(x)
            plt.hlines(y=0, xmin='2009-01', xmax='2018-04', colors='orange', linestyles='--')

    plt.show()


def avg_YoY_change(ts_dict):
    """take a dictionary of time series data frames and calculate
       the average YoY change for each one"""
    
    # create an empty list to add averages to
    avg_YoY = []
    
    # iterate through the dict and claculate the average YoY change for each 
    # key:value pair and add it to the list of averages
    for v in ts_dict:
        avg = ts_dict[v]['YoY_change'].mean()
        avg_YoY.append(avg)

    # combine the city names and average values and return a sorted list
    city_names = list(ts_dict.keys())
    avg_YoY = list(zip(city_names, avg_YoY))
    return sorted(avg_YoY, key=lambda x: x[1])


def plot_avg_YoY(ts_dict):
    """take a dicitonary of time series dataframes and plot a bar chart
       of average YoY growth"""
    
    # get a sorted list of average YoY changes
    avgs = avg_YoY_change(ts_dict)
    
    # establish x and y values 
    x = [i[0] for i in avgs]
    y = [i[1] for i in avgs]
    
    # plot avearges in a bar chart
    fig = plt.figure(figsize=(14,6))
    plt.bar(x=x, height=y)
    plt.xticks(rotation='vertical')
    plt.show()

