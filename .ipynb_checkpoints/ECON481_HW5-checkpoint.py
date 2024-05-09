#!/usr/bin/env python
# coding: utf-8

def github() -> str:
    """
    This function returns a link to the GitHub repository containing solutions.

    Returns:
        str: The URL to the GitHub repository.
    """
    return "https://github.com/anasfathul/ECON481/blob/main/ECON481_HW5.py"

from bs4 import BeautifulSoup
import requests

def scrape_code(url: str) -> str:
    """
    This function takes as its argument a lecture’s URL on the course website.
    It will returns a string containing all the python code in the lecture formatted
    in such a way that we could save it as a python file and run it without syntax issues.
    """

    # Send a request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for a successful request

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize an empty string to hold all Python code
    python_code = ''

    # Find all <code> tags with class "sourceCode python"
    code_blocks = soup.find_all('code', class_='sourceCode python')

    # Iterate over each code block and extract the text, stripping unwanted text if necessary
    for code in code_blocks:
        # Retrieve text and strip leading/trailing whitespace
        code_text = code.get_text().strip()
        
        # Further processing to filter out unwanted snippets or lines
        lines = code_text.split('\n')
        relevant_lines = [line for line in lines if not line.strip().startswith('%')]  
        # Example condition to filter lines
        
        # Join filtered lines and add to the final Python code string
        python_code += '\n'.join(relevant_lines) + '\n'

    return python_code.strip()  # Remove any extra newlines at the end
    