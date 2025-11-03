# Assignment Overview

This assignment collects data from Reddit for sports-related subreddits (`MLB`, `NBA`, `NFL`).  
It fetches both "hot posts" and "keyword-based search results", cleans the data, removes duplicates, and exports it to a CSV file for further analysis.

# How to Run

## 1. Prerequisites

- Python 3.8 or higher  
- PRAW  
- pandas  

## 2. Installation

Install the required Python packages using pip:
- install praw python-dotenv

Import
-import praw
-import csv
-import os

from dotenv import load_dotenv
from google.colab import drive

## 3. Configuration

Create a Reddit application at https://www.reddit.com/prefs/apps
to obtain:

client_id
client_secret
user_agent

Add these credentials to your script directly or use a .env file.
Example .env content:

## 4. Execution

Run the Python script using:
- python reddit_code.py
