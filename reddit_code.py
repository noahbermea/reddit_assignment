
# -*- coding: utf-8 -*-
import praw
import csv
import os
from dotenv import load_dotenv

print("✅ Libraries imported successfully!")

# Load Environment Variables
# Load Reddit API credentials from the environment file.
from google.colab import drive
drive.mount('/content/drive')

# Load environment variables from .env file
# load_dotenv('reddit_api.env') # This line was commented out
from dotenv import dotenv_values
import os

# Define the path to your .env file in Google Drive
# IMPORTANT: Update this path to the actual location of your reddit_api.env file in your Google Drive
env_file_path = '/content/drive/My Drive/Colab Notebooks/reddit_api.env1.txt'


# Load environment variables from reddit_api.env file if it exists
if os.path.exists(env_file_path):
    config = dotenv_values(env_file_path)
    print(f"✅ Environment variables loaded from {env_file_path}!")
else:
    config = {}
    print(f"❌ Error: '{env_file_path}' not found. Environment variables not loaded.")
    print("Please ensure the 'reddit_api.env' file is in the specified Google Drive path.")

# Authenticate with Reddit using environment variables
reddit = praw.Reddit(
    client_id=config.get('REDDIT_CLIENT_ID'),
    client_secret=config.get('REDDIT_CLIENT_SECRET'),
    username=config.get('REDDIT_USERNAME'),
    password=config.get('REDDIT_PASSWORD'),
    user_agent=config.get('REDDIT_USER_AGENT')
)

print("✅ Reddit API authenticated successfully!")
print(f"Connected as: {reddit.user.me()}")


