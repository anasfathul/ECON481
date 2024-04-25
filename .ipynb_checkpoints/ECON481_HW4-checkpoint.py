#!/usr/bin/env python
# coding: utf-8

def github() -> str:
    """
    This function returns a link to the GitHub repository containing solutions.

    Returns:
        str: The URL to the GitHub repository.
    """
    return "https://github.com/anasfathul/ECON481/blob/main/ECON481_HW4.py"

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Exercise 1
def load_data() -> pd.DataFrame:
    """
    A function that accesses the file on Tesla stock price history on the course website.
    Returns that data as a pd.DataFrame
    """
    temp_df = pd.read_csv("https://lukashager.netlify.app/econ-481/data/TSLA.csv", index_col=0, parse_dates=True)
    temp_df.index = pd.to_datetime(temp_df.index)
    
    return temp_df

# Exercise 2
def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:
    """
    A function that takes the output of load_data() as defined above,
    as well as an optional start and end date (strings formatted as ‘YYYY-MM-DD’).
    Plots the closing price of the stock between those dates as a line graph.
    Include the date range in the title of the graph.
    """
    # Masked the DataFrame to the specified date range
    mask = (df.index >= start) & (df.index <= end)
    filtered_df = df.loc[mask]

    plt.style.use('classic')
    plt.figure(figsize=(12, 6)) 
    plt.plot(filtered_df.index, filtered_df['Close'], label='Close Price', color='blue', linewidth=2)
    plt.title(f'Tesla Stock Close Prices from {start} to {end}')  
    plt.xlabel('Date') 
    plt.ylabel('Close Price (USD)')
    plt.grid(True)  
    plt.legend() 
    plt.show() 

# Exercise 3
def autoregress(df: pd.DataFrame) -> float:
    """
    This function takes a dataframe as argument.
    Return t-statistics on beta0 hat from regression of delta xt to delta xt - 1
    Using HC1 standard errors in regression
    """
    # Calculate \Delta x_t
    df['delta_close'] = df['Close'].diff()
    
    # Create the lagged variable \Delta x_{t-1}
    df['lag_delta_close'] = df['delta_close'].shift(1)
    df.dropna(inplace=True)
    
    # Define the variables
    X = df['lag_delta_close']
    y = df['delta_close']

    # OLS model
    model = sm.OLS(y, X).fit(cov_type='HC1')  # (HC1)
    
    return model.tvalues[0] # Return the t-statistic for \hat{\beta}_0

# Exercise 4
def autoregress_logit(df: pd.DataFrame) -> float:
    """
    This function takes a dataframe as argument.
    Return t-statistics on beta0 hat from logistic regression of positive delta xt
    """
    # Calculate \Delta x_t
    df['delta_close'] = df['Close'].diff()
    df['delta_Positive'] = (df['delta_close'] > 0).astype(int)
    
    # Create the lagged variable \Delta x_{t-1}
    df['lag_delta_close'] = df['delta_close'].shift(1)
    df.dropna(inplace=True)
    
    # Define the variables
    X = df['lag_delta_close']
    y = df['delta_Positive']

    # Logit model without result output
    model = sm.Logit(y, X).fit(disp=0) 
    
    return model.tvalues['lag_delta_close'] # Return the t-statistic for \hat{\beta}_0

# Exercise 5
def plot_delta(df: pd.DataFrame) -> None:
    """
    This function takes a single argument df and plots changes in closing price for the full dataset.
    """
    df['delta_close'] = df['Close'].diff()
    plt.style.use('classic')
    plt.figure(figsize=(12, 6)) 
    plt.plot(df.index, df['delta_close'], label=r'$\Delta x_t$', color='blue', linewidth=2)
    plt.grid(color='gray', linestyle=':', linewidth=0.5)
    plt.title(r'$\Delta x_t$: Changes in Tesla Stock Market Price')
    plt.xlabel('Year')
    plt.ylabel('Change in Close Price (USD)')
    plt.legend()
    plt.show() 
    