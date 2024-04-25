#!/usr/bin/env python
# coding: utf-8

def github() -> str:
    """
    This function returns a link to the GitHub repository containing solutions.

    Returns:
        str: The URL to the GitHub repository.
    """
    return "https://github.com/anasfathul/ECON481/blob/main/ECON481_HW3.py"

import numpy as np
import scipy as sp
import pandas as pd

# Exercise 1
import pandas as pd

def import_yearly_data(years: list) -> pd.DataFrame:
    """
    This function takes as its argument a list of years.
    It returns a concatenated DataFrame of the Direct Emitters tab of each of those year's EPA excel sheet.
    It will add a variable year that references the year from which the data is pulled and no column use as index.
    """
    full_df = []

    for year in years:
        exl_path = f"https://lukashager.netlify.app/econ-481/data/ghgp_data_{year}.xlsx"
        temp_df = pd.read_excel(exl_path, header=3, sheet_name='Direct Emitters')
        temp_df['year'] = year
        full_df.append(temp_df)

    
    return pd.concat(full_df)

# Exercise 2
import pandas as pd

def import_parent_companies(years: list) -> pd.DataFrame:
    """
    This function takes as its argument a list of years.
    It returns a concatenated DataFrame of the corresponding tabs in the parent companies excel sheet.
    It will add a variable year that references the year from which the data is pulled and
    remove any row that is entirely null values. No column use as index.
    """
    full_df = []

    for year in years:
        exl_path = "https://lukashager.netlify.app/econ-481/data/ghgp_data_parent_company_09_2023.xlsb"
        temp_df = pd.read_excel(exl_path, sheet_name=str(year))
        temp_df['year'] = year
        full_df.append(temp_df)

    
    return pd.concat(full_df).dropna(how='all')

# Exercise 3
def n_null(df: pd.DataFrame, col: str) -> int:
    """
    This function takes as its arguments a DataFrame and a column name.
    It returns an integer corresponding to the number of null values in that column
    """
    return df[col].isna().sum()

# Exercise 4
def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes as its arguments a concatenated DataFrame of emissions sheets and a concatenated DataFrame of parent companies.
    Performs a left join on the emissions_data and parent_data DataFrames using 'year' and 'Facility Id'
    from emissions_data and 'year' and 'GHGRP FACILITY ID' from parent_data as join keys.
    Subsets the resulting DataFrame to include only the following columns: 'Facility Id', 'year', 'State',
    'Industry Type (sectors)', 'Total reported direct emissions', 'PARENT CO. STATE', and 'PARENT CO. PERCENT OWNERSHIP'.
    
    Return cleaned DataFrame with all column names to lower-case.
    """
    full_df = pd.merge(emissions_data, parent_data,
                       left_on=['year', 'Facility Id'], right_on=['year', 'GHGRP FACILITY ID'], how='left')
    col_subset = ['Facility Id', 'year', 'State',
                  'Industry Type (sectors)', 'Total reported direct emissions', 'PARENT CO. STATE', 'PARENT CO. PERCENT OWNERSHIP']
    subset_df = full_df[col_subset]
    subset_df.columns = [col.lower() for col in col_subset]
    return subset_df

# Exercise 5
def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    """
    This function takes a DataFrame (as output from Exercise 4) and a list of variables to group by.
    Computes the minimum, median, mean, and maximum values for 'total reported direct emissions' and 'parent co. percent ownership'.
    Results are grouped by the variables specified in 'group_vars'.
    Return the data sorted by highest to lowest mean total reported direct emissions.
    """
    return df.groupby(group_vars)[['total reported direct emissions',
                                   'parent co. percent ownership']].agg(['min', 'median',
                                                                         'mean', 'max']).sort_values(('total reported direct emissions', 'mean'), ascending=False)