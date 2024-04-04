#!/usr/bin/env python
# coding: utf-8

def github() -> str:
    """
    This function returns a link to the GitHub repository containing solutions.

    Returns:
        str: The URL to the GitHub repository.
    """
    return "https://github.com/anasfathul/ECON481/ECON481_HW1.py>"


# Exercise 1 importing packages as needed (to show packages)
#import numpy as np
#import pandas as pd
#import scipy
#import matplotlib.pyplot as plt
#import seaborn as sns

# Exercise 2
def evens_and_odds(n: int) -> dict:
    """
    This function takes a natural number n as argument and returns a dictionary with two keys,
    “evens” and “odds”. “evens” should be the sum of all the even natural numbers less than n,
    and “odds” the sum of all natural numbers less than n.
    """
    evens_sum = sum([i for i in range(n) if i % 2 == 0])
    odd_sum = sum([i for i in range(n) if i % 2 != 0])
    return {'evens': evens_sum, 'odds': odd_sum}


# Exercise 3
from typing import Union
from datetime import datetime

def time_diff(date_1: str, date_2: str, out: str) -> Union[str,float]:
    """
    This function takes two strings in the format ‘YYYY-MM-DD’ and a keyword out dictating the output.
    If the keyword is “float”, return the time between the two dates (in absolute value) in days.
    If the keyword is “string”, return “There are XX days between the two dates”.
    If not specified, the out keyword should be assumed to be “float”.
    """
    date_1_parsed = datetime.strptime(date_1, '%Y-%m-%d')
    date_2_parsed = datetime.strptime(date_2, '%Y-%m-%d')

    # Calculate the absolute difference in days
    diff = abs((date_2_parsed - date_1_parsed).days)

    # Return the difference based on the 'out' parameter
    if out == 'string':
        return f"There are {diff} days between the two dates"
    else:  # Default to returning the difference as a float
        return diff

    return None


# Exercise 4

def reverse(in_list: list) -> list:
    """
    This function takes a list and returns a list of the arguments in reverse order.
    """
    reversed_list = []  # Initialize an empty list to store the reversed elements
    for item in in_list:
        reversed_list.insert(0, item)
    return reversed_list


# Exercise 5

def prob_k_heads(n: int, k: int) -> float:
    """
    This function takes as its arguments natural numbers n and k with n>k and
    returns the probability of getting k heads from n flips.
    """
    def factorial(x):
        if x == 0 or x == 1:
            return 1
        else:
            return x * factorial(x - 1)
    
    # Function to calculate binomial coefficient
    def binom_coeff(n, k):
        return factorial(n) / (factorial(k) * factorial(n - k))
    
    # Probability of success on a single trial
    p = 0.5
    
    # Calculating the probability
    probability = binom_coeff(n, k) * (p ** k) * ((1 - p) ** (n - k))
    
    return probability

