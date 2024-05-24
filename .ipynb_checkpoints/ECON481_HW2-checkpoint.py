#!/usr/bin/env python
# coding: utf-8

def github() -> str:
    """
    This function returns a link to the GitHub repository containing solutions.

    Returns:
        str: The URL to the GitHub repository.
    """
    return "https://github.com/anasfathul/ECON481/blob/main/ECON481_HW2.py"

import numpy as np
import scipy as sp

# Exercise 1
def simulate_data(seed: int = 481) -> tuple:
    """
    This function returns 1000 simulated observations.
    It take one argument for seed, an integer.
    It return a tuple of two arrays,
    (y, X), where y has a shape of 1000 x 1 and X has shape of 1000 x 3. 
    """
    rng = np.random.default_rng(seed)
    # Generate X matrix (1000 x 3)
    X = rng.normal(0, np.sqrt(2), size=(1000, 3))

    epsilon = rng.normal(0, 1, size=(1000, 1))

    y = 5 + 3*X[:, 0:1] + 2*X[:, 1:2] + 6*X[:, 2:3] + epsilon

    return y.reshape(-1, 1), X

# Exercise 2
def estimate_mle(y, X):
    """
    Estimates the MLE parameters for a linear model using optimization.
    
    Parameters:
    - y: Dependent variable (1000 x 1 np.array).
    - X: Independent variables (1000 x 3 np.array).
    
    Returns:
    - A 4 x 1 np.array with the coefficients (beta_0, beta_1, beta_2, beta_3).
    """
    
    # Initial guess for the coefficients (including intercept)
    initial_guess = np.zeros(X.shape[1] + 1)
    # Minimize the negative log-likelihood
    result = sp.optimize.minimize(fun=neg_log_likelihood, x0=initial_guess, args=(X, y), method = 'Nelder-Mead')
    # Return the estimated parameters
    return np.round(result.x, decimals = 0)

def neg_log_likelihood(beta, X, y):
    """
    Compute the negative log-likelihood for a linear regression model.
    
    Parameters:
    - beta: Coefficients (including intercept) for the linear model as a numpy array.
    - X: Independent variables as a numpy array (with an intercept column if applicable).
    - y: Dependent variable as a numpy array.
    
    Returns:
    - The negative log-likelihood of the linear regression model given the data.
    """
    y_pred = np.hstack((np.ones(X.shape[0]).reshape(-1,1), X)) * beta  # Using matrix multiplication for predictions
    
    # Calculate residuals
    residuals = y - y_pred
    
    # Estimate the variance of the residuals
    sigma2_hat = np.sum(residuals**2) / len(y)
    
    # Compute the negative log-likelihood
    nll = len(y) / 2 * np.log(2 * np.pi * sigma2_hat) + np.sum(residuals**2) / (2 * sigma2_hat)
    
    return nll

# Exercise 3
def sum_of_squared_residuals(beta, X, y):
    """
    Calculate the sum of squared residuals (SSR).
    
    Parameters:
    - beta: np.array, the model coefficients including the intercept.
    - X: np.array, the independent variables (observations x features).
    - y: np.array, the dependent variable (observations x 1).
    
    Returns:
    - The sum of squared residuals.
    """
    # Predicted values from the model
    y_pred = X * beta
    # Calculate residuals
    residuals = y - y_pred
    # Sum of squared residuals
    ssr = np.sum(residuals**2)
    return ssr

def estimate_ols(y: np.array, X: np.array) -> np.array:
    """
    Estimate OLS coefficients for the given data without using the closed-form solution.
    
    Parameters:
    - y: np.array, the dependent variable (1000 x 1).
    - X: np.array, the independent variables (1000 x 3).
    
    Returns:
    - A np.array with the estimated coefficients (4 x 1), including the intercept.
    """
    # Augment X with a column of ones for the intercept term
    X_with_intercept = np.hstack([np.ones((X.shape[0], 1)), X])
    # Initial guess for the coefficients (intercept + coefficients for each feature)
    initial_guess = np.zeros(X_with_intercept.shape[1])
    # Minimize the sum of squared residuals
    result = sp.optimize.minimize(fun=sum_of_squared_residuals, x0=initial_guess, args=(X_with_intercept, y))
    
    return np.round(result.x, decimals = 0)