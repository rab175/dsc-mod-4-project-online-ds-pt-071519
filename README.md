
# Mod 4 Project - Real Estate Portfolio Analysis

This notebook contains the data processing and analysis for the Flatiron School Data Science Bootcamp Mod 4 Project. In this module we're learning about time series analysis and SARIMA models. Below we'll analyze a dataset comprised of Zillow data - zipcodes from around the U.S., and seek to answer the question:

"What are the top 5 best zipcodes to invest in?

In this case we'll act as a consultant to a real estate investment firm, but are otherwise left to our own devices to determine how to qualify the term "best". We'll further state our business case and assumptions below, but we'll start by stating that "best" will be more complex than the fastest growing and most expensive areas. We'll seek to create a balanced portfolio of properties that match or exceed market returns, but are spread across value segments to diversify our holdings and thereby mitigate risk.

To make this notebook more readable I've placed a number of functions I created (or found) in two separate text files and imported them into this notebook. Check out **'ryans_ts_helper.py'** and **'SARIMA_grid_search.py'** to see some of those functions.

See those files and presentation here:

[ryans_ts_helper.py](https://github.com/rab175/dsc-mod-4-project-online-ds-pt-071519/blob/master/ryans_ts_helper.py)

[SARIMA_grid_search.py](https://github.com/rab175/dsc-mod-4-project-online-ds-pt-071519/blob/master/SARIMA_grid_search.py)

[Non-technical Presentation](https://docs.google.com/presentation/d/17PkAMyvhgYcwayZvrQ0b8f4zLqRy2PF1TfWArZ2nbGY/edit?usp=sharing)

### Outline

This notebook is organized as follows:

1. Business Case
2. Data Import and Cleaning
3. Exploratory Data Analysis
4. Modeling
5. Results and Conclusions


### Business Case

Our real estate investment strategy will involve choosing a combination of 5 separate zip codes from across the United States that range from high to low priced properties, and determining a strategy with which to invest $50mm across them. This strategy is focused on acquiring a diverse range of assets, acknowledging that it also may involve working in very different markets and locales, and may involve acquiring properties that have very different management and sales requirements. Nevertheless we believe that this strategy will allow us to benefit from having access to the performance of a wide range of properties and markets, both helping spread risk, and potentially find opportunities for over-performance.

We will disperse our $50mm of investment resources evenly across the 5 zipcodes, and across three different value segments: High, Medium, and Low cost areas, defined in more detail below.

Ultimately our goal is to implement a strategy that will at least match or exceed the performance of current housing indices.

### Modeling Approach

We will work through each segment of value areas building SARIMA models for each area we've chosen, with the ultimate goal of choosing 1 high value, 2 medium value, and 2 lower value areas to invest in. 

We will use a few different processes to experiment with stationarity and parameter selection, using methods we were taught in class as well as methods I have decided to incorporate on my own (e.g. grid search). 

SARIMA is an approach for modeling univariate time series data that may have a trend or seasonality. The model takes multiple parameters that I understand can be very dependent on deep domain knowledge (which I hope to grow), but we've learned methods for iterating through parameters that may help. 

Despite the fact that SARIMA is designed to deal with non-stationary data, for the sake of learning I have tried a few things out in the section that I think are fun.

Modeling for each zipcode will follow the following rough outline: 
- Check for stationarity (understanding this isn't entirely necessary)
    - For the first model I will do some transformations for learning purposes
- Inspect Autocorrelation Function and Partial Autocorrelation Function
- Identify optimal model parameters 
- Fit model and inspect diagnostics
- Plot model and forecast
- Check future values and choose final city_zipcodes