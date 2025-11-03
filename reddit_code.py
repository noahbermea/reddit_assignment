
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

# Define Data Collection Function
# Create a function to download recent posts from a specified subreddit with proper error handling and improvements.
## Task 1: Fetching "Hot" Posts

def download_hot_posts(subreddit_name, limit=100, filename="hot_posts.csv"):
    """
    Download hot posts from a specified subreddit and save to CSV.

    Args:
        subreddit_name (str): Name of the subreddit to download from
        limit (int): Number of posts to download (default: 100)
        filename (str): Name of the output CSV file

    Returns:
        bool: True if successful, False otherwise
    """
    # Input validation
    if not subreddit_name or not isinstance(subreddit_name, str):
        raise ValueError("Subreddit name must be a non-empty string")
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("Limit must be a positive integer")
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")

    try:
        # --- Connect to subreddit ---
        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.hot(limit=limit) # change new to hot

        # --- Open CSV File ---
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Correct header row
            writer.writerow([
                "Title", "Score", "Upvote_ratio", "Num_comments", "Author",
                "Subreddit", "URL", "Permalink", "Created_utc", "Is_self",
                "Selftext", "Flair", "Domain", "Search_query"
            ])

            post_count = 0

            # --- Loop through posts and write each row ---
            for post in posts:
                author_name = post.author.name if post.author else "[deleted]"
                text_content = post.selftext[:1000] + "..." if len(post.selftext) > 1000 else post.selftext

                writer.writerow([
                    post.title,
                    post.score,
                    getattr(post, "upvote_ratio", "N/A"),
                    post.num_comments,
                    author_name,
                    post.subreddit.display_name,
                    post.url,
                    f"https://www.reddit.com{post.permalink}" if hasattr(post, "permalink") else "N/A",
                    getattr(post, "created_utc", "N/A"),
                    getattr(post, "is_self", "N/A"),
                    text_content,
                    post.link_flair_text if post.link_flair_text else "N/A",
                    getattr(post, "domain", "N/A"),
                    subreddit_name
                ])
                post_count += 1

        # --- Logging Summary ---
        print(f"\n✅ Collected {post_count} posts from r/{subreddit_name}.")
        print(f"📁 Data saved to '{filename}'.")

        return True

    except Exception as e:
        print(f"❌ Error while downloading posts: {e}")
        return False

print("✅ Function defined successfully!")

# Task 2: Keyword-Based Search
def search_posts(query, subreddits, limit=100, filename="search_results.csv"):
    """
    Search for posts containing a specific keyword across one or more subreddits.

    Args:
        query (str): Search keyword or phrase
        subreddits (list): List of subreddit names
        limit (int): Max number of posts to fetch per subreddit
        filename (str): Output CSV filename

    Returns:
        bool: True if successful, False otherwise
    """
    # Input validation
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")
    if not subreddits or not isinstance(subreddits, list):
        raise ValueError("Subreddits must be a non-empty list of strings")
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("Limit must be a positive integer")
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")

    try:
        # Open CSV file
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Title", "Score", "Upvote_ratio", "Num_comments", "Author",
                "Subreddit", "URL", "Permalink", "Created_utc", "Is_self",
                "Selftext", "Flair", "Domain", "Search_query"
            ])

            total_posts = 0

            for subreddit_name in subreddits:
                subreddit = reddit.subreddit(subreddit_name)
                posts = subreddit.search(query, limit=limit)

                subreddit_count = 0
                for post in posts:
                    author_name = post.author.name if post.author else None
                    text_content = post.selftext[:1000] + "..." if post.selftext and len(post.selftext) > 1000 else post.selftext or None

                    writer.writerow([
                        post.title or None,
                        post.score if hasattr(post, "score") else None,
                        getattr(post, "upvote_ratio", None),
                        post.num_comments if hasattr(post, "num_comments") else None,
                        author_name,
                        post.subreddit.display_name or subreddit_name,
                        post.url or None,
                        f"https://www.reddit.com{post.permalink}" if hasattr(post, "permalink") else None,
                        getattr(post, "created_utc", None),
                        getattr(post, "is_self", None),
                        text_content,
                        post.link_flair_text or None,
                        getattr(post, "domain", None),
                        query
                    ])
                    total_posts += 1
                    subreddit_count += 1

                # Print per-subreddit summary
                print(f"✅ Collected {subreddit_count} posts containing '{query}' from r/{subreddit_name}.")

        # Print total summary
        print(f"\n📁 Total posts collected: {total_posts}. Data saved to '{filename}'.")
        return True

    except Exception as e:
        print(f"❌ Error while searching posts: {e}")
        return False

print("✅ Function defined successfully!")

### Creating CSV for NBA, Execute Data Collection, & Verifying Results
## Configuration parameters
subreddit_name = "NBA"  # Subreddit to download posts from
limit = 100  # Number of posts to download
filename = "recent_nba_posts_notebook.csv"  # Name of the CSV file

print(f"📋 Configuration:")
print(f"   Subreddit: r/{subreddit_name}")
print(f"   Posts to download: {limit}")
print(f"   Output file: {filename}")

## Execute the data collection
success = download_hot_posts(subreddit_name, limit, filename)

if success:
    print("\n🎉 Data collection completed successfully!")
else:
    print("\n❌ Data collection failed. Please check the error messages above.")

## Verifying Results
import pandas as pd

# Check if file exists and load data
if os.path.exists(filename):
    # Load the CSV file
    df = pd.read_csv(filename)

    df = df.drop(columns=[col for col in df.columns if col.endswith(".1")], errors="ignore")
    df = df.replace("None", pd.NA)
    df = df.dropna(subset=["Title", "Author"], how="all")
    df = df.fillna("None")

    print(f"📊 Dataset Overview:")
    print(f"   Total posts: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   File size: {os.path.getsize(filename)} bytes")

    print(f"\n📝 Sample Posts:")
    print("=" * 50)

    # Display first 3 posts
    for i, row in df.head(3).iterrows():
        print(f"\nPost {i+1}:")
        print(f"Title: {row['Title'][:80]}...")
        print(f"Score: {row['Score']}")
        print(f"Upvote_ratio: {row['Upvote_ratio']}")
        print(f"Num_comments: {row['Num_comments']}")
        print(f"Author: {row['Author']}")
        print(f"Subreddit: {row['Subreddit']}")
        print(f"URL: {row['URL']}")
        print(f"Permalink: {row['Permalink']}")
        print(f"Created_utc: {row['Created_utc']}")
        print(f"Is_self: {row['Is_self']}")
        print(f"Selftext: {row['Selftext']}")
        print(f"Flair: {row['Flair']}")
        print(f"Domain: {row['Domain']}")
        print(f"Search_query: {row['Search_query']}")
        print("-" * 30)

    # Basic statistics
    print(f"\n📈 Basic Statistics:")
    print(f"   Average score: {df['Score'].mean():.2f}")
    print(f"   Highest score: {df['Score'].max()}")
    print(f"   Lowest score: {df['Score'].min()}")

else:
    print(f"❌ File '{filename}' not found!")

### Creating CSV for NFL, Execute Data Collection, & Verifying Results

## Configuration parameters
subreddit_name = "NFL"  # Subreddit to download posts from
limit = 100  # Number of posts to download
filename = "recent_nfl_posts_notebook.csv"  # Name of the CSV file

print(f"📋 Configuration:")
print(f"   Subreddit: r/{subreddit_name}")
print(f"   Posts to download: {limit}")
print(f"   Output file: {filename}")

## Execute the data collection
success = download_hot_posts(subreddit_name, limit, filename)

if success:
    print("\n🎉 Data collection completed successfully!")
else:
    print("\n❌ Data collection failed. Please check the error messages above.")

## Verifying Results
import pandas as pd

# Check if file exists and load data
if os.path.exists(filename):
    # Load the CSV file
    df = pd.read_csv(filename)

    df = df.drop(columns=[col for col in df.columns if col.endswith(".1")], errors="ignore")
    df = df.replace("None", pd.NA)
    df = df.dropna(subset=["Title", "Author"], how="all")
    df = df.fillna("None")

    print(f"📊 Dataset Overview:")
    print(f"   Total posts: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   File size: {os.path.getsize(filename)} bytes")

    print(f"\n📝 Sample Posts:")
    print("=" * 50)

    # Display first 3 posts
    for i, row in df.head(3).iterrows():
        print(f"\nPost {i+1}:")
        print(f"Title: {row['Title'][:80]}...")
        print(f"Score: {row['Score']}")
        print(f"Upvote_ratio: {row['Upvote_ratio']}")
        print(f"Num_comments: {row['Num_comments']}")
        print(f"Author: {row['Author']}")
        print(f"Subreddit: {row['Subreddit']}")
        print(f"URL: {row['URL']}")
        print(f"Permalink: {row['Permalink']}")
        print(f"Created_utc: {row['Created_utc']}")
        print(f"Is_self: {row['Is_self']}")
        print(f"Selftext: {row['Selftext']}")
        print(f"Flair: {row['Flair']}")
        print(f"Domain: {row['Domain']}")
        print(f"Search_query: {row['Search_query']}")
        print("-" * 30)

    # Basic statistics
    print(f"\n📈 Basic Statistics:")
    print(f"   Average score: {df['Score'].mean():.2f}")
    print(f"   Highest score: {df['Score'].max()}")
    print(f"   Lowest score: {df['Score'].min()}")

else:
    print(f"❌ File '{filename}' not found!")

### Creating CSV for MLB, Execute Data Collection, & Verifying Results
## Configuration parameters
subreddit_name = "MLB"  # Subreddit to download posts from
limit = 100  # Number of posts to download
filename = "recent_mlb_posts_notebook.csv"  # Name of the CSV file

print(f"📋 Configuration:")
print(f"   Subreddit: r/{subreddit_name}")
print(f"   Posts to download: {limit}")
print(f"   Output file: {filename}")

## Execute the data collection
success = download_hot_posts(subreddit_name, limit, filename)

if success:
    print("\n🎉 Data collection completed successfully!")
else:
    print("\n❌ Data collection failed. Please check the error messages above.")

## Verifying Results
import pandas as pd

# Check if file exists and load data
if os.path.exists(filename):
    # Load the CSV file
    df = pd.read_csv(filename)

    df = df.drop(columns=[col for col in df.columns if col.endswith(".1")], errors="ignore")
    df = df.replace("None", pd.NA)
    df = df.dropna(subset=["Title", "Author"], how="all")
    df = df.fillna("None")

    print(f"📊 Dataset Overview:")
    print(f"   Total posts: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   File size: {os.path.getsize(filename)} bytes")

    print(f"\n📝 Sample Posts:")
    print("=" * 50)

    # Display first 3 posts
    for i, row in df.head(3).iterrows():
        print(f"\nPost {i+1}:")
        print(f"Title: {row['Title'][:80]}...")
        print(f"Score: {row['Score']}")
        print(f"Upvote_ratio: {row['Upvote_ratio']}")
        print(f"Num_comments: {row['Num_comments']}")
        print(f"Author: {row['Author']}")
        print(f"Subreddit: {row['Subreddit']}")
        print(f"URL: {row['URL']}")
        print(f"Permalink: {row['Permalink']}")
        print(f"Created_utc: {row['Created_utc']}")
        print(f"Is_self: {row['Is_self']}")
        print(f"Selftext: {row['Selftext']}")
        print(f"Flair: {row['Flair']}")
        print(f"Domain: {row['Domain']}")
        print(f"Search_query: {row['Search_query']}")
        print("-" * 30)

    # Basic statistics
    print(f"\n📈 Basic Statistics:")
    print(f"   Average score: {df['Score'].mean():.2f}")
    print(f"   Highest score: {df['Score'].max()}")
    print(f"   Lowest score: {df['Score'].min()}")

else:
    print(f"❌ File '{filename}' not found!")

### Combining CSV files into one

csv_files = [
    "recent_mlb_posts_notebook.csv",
    "recent_nba_posts_notebook.csv",
    "recent_nfl_posts_notebook.csv"
]

# Read and concatenate all CSVs
combined_df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# Save combined CSV
combined_df.to_csv("reddit_data.csv", index=False)

print(f"✅ Combined CSV created: 'reddit_data.csv' ({len(combined_df)} rows)")

### Optional: Data Analysis
## Perform some basic analysis on the collected sports posts data.

# Additional analysis (optional)
if 'df' in locals() and not df.empty:
    print("🔍 Additional Analysis:")
    print("=" * 40)

    # Top scoring posts
    top_posts = combined_df.nlargest(5, 'Score')[['Title', 'Score', 'Author']]
    print("\n🏆 Top 5 Posts by Score:")
    for i, (_, row) in enumerate(top_posts.iterrows(), 1):
        print(f"{i}. {row['Title'][:60]}... (Score: {row['Score']}, Author: {row['Author']})")

    # Most active authors
    author_counts = combined_df['Author'].value_counts().head(5)
    print("\n👥 Most Active Authors:")
    for author, count in author_counts.items():
        print(f"   {author}: {count} posts")

    # Posts with text content
    posts_with_text = combined_df[combined_df['Selftext'].str.len() > 0]
    print(f"\n📝 Posts with text content: {len(posts_with_text)} out of {len(combined_df)}")

else:
    print("❌ No data available for analysis")
