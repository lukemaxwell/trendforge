# tools.py

import os
import streamlit as st
import praw
from pytrends.request import TrendReq
import googleapiclient.discovery
import re

# Load secrets or env vars
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
REDDIT_CLIENT_ID = st.secrets.get("REDDIT_CLIENT_ID", os.getenv("REDDIT_CLIENT_ID"))
REDDIT_CLIENT_SECRET = st.secrets.get("REDDIT_CLIENT_SECRET", os.getenv("REDDIT_CLIENT_SECRET"))
YOUTUBE_API_KEY = st.secrets.get("YOUTUBE_API_KEY", os.getenv("YOUTUBE_API_KEY"))

# --- Discover subreddits ---

def discover_subreddits(niche, limit=10):
    print(f"DEBUG: Discovering subreddits for niche '{niche}'")
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent="trendforge (by u/yourusername)"
        )

        # Use Reddit full text search (BETTER than search_by_name)
        results = reddit.subreddits.search(query=niche, limit=15)
        subreddit_names = [sub.display_name for sub in results]

        if not subreddit_names:
            print("DEBUG: No subreddits found.")
            return []

        print(f"DEBUG: Found subreddits: {subreddit_names[:limit]}")
        return subreddit_names[:limit]

    except Exception as e:
        print(f"ERROR: Failed to discover subreddits: {e}")
        return []

# --- Reddit trend search ---

def reddit_trend_search(subreddits):
    print(f"DEBUG: Fetching Reddit trends for subreddits: {subreddits}")

    if not subreddits:
        return "No subreddits provided."

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent="trendforge (by u/yourusername)"
        )

        all_trends = ""

        for subreddit_name in subreddits:
            print(f"DEBUG: Fetching top posts from r/{subreddit_name}")
            subreddit = reddit.subreddit(subreddit_name)
            top_posts = subreddit.top("week", limit=10)

            trends_text = f"\n\nr/{subreddit_name} Top Posts:\n"
            for post in top_posts:
                trends_text += f"- {post.title} ({post.score} upvotes)\n"

            all_trends += trends_text

        if not all_trends:
            print("DEBUG: No Reddit trends found.")
            return "No Reddit trends found."

        print("DEBUG: Reddit trends fetched successfully.")
        return all_trends

    except Exception as e:
        print(f"ERROR: Error fetching Reddit trends: {e}")
        return f"Error fetching Reddit trends: {e}"

# --- Google Trends search ---

def google_trends_search(niche):
    print(f"DEBUG: Fetching Google Trends for niche '{niche}'")
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([niche], timeframe='today 7-d', geo='')

        related_queries_result = pytrends.related_queries()
        related_queries = []

        if niche in related_queries_result:
            top_queries = related_queries_result[niche].get("top", None)
            if top_queries is not None:
                related_queries = top_queries["query"].tolist()

        if not related_queries:
            print("DEBUG: No Google Trends found.")
            return "No Google Trends found."

        print(f"DEBUG: Google Trends fetched successfully: {related_queries}")
        return "\n".join(related_queries)

    except Exception as e:
        print(f"ERROR: Error fetching Google Trends: {e}")
        return f"Error fetching Google Trends: {e}"

# --- YouTube trend search ---

def youtube_trend_search(niche):
    print(f"DEBUG: Fetching YouTube trends for niche '{niche}'")
    try:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

        request = youtube.search().list(
            part="snippet",
            maxResults=10,
            q=niche,
            type="video",
            order="viewCount",
            relevanceLanguage="en"
        )
        response = request.execute()

        video_titles = []
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            video_titles.append(title)

        if not video_titles:
            print("DEBUG: No YouTube trends found.")
            return "No YouTube trends found."

        print(f"DEBUG: YouTube trends fetched successfully: {video_titles}")
        return "\n".join(video_titles)

    except Exception as e:
        print(f"ERROR: Error fetching YouTube trends: {e}")
        return f"Error fetching YouTube trends: {e}"

# --- YouTube channel extractor ---

def extract_channel_info(channel_url):
    print(f"DEBUG: Extracting channel info from URL: {channel_url}")
    try:
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

        # Extract channel ID from URL
        channel_id = None
        if "channel/" in channel_url:
            match = re.search(r"channel/([a-zA-Z0-9_-]+)", channel_url)
            if match:
                channel_id = match.group(1)
        elif "user/" in channel_url:
            match = re.search(r"user/([a-zA-Z0-9_-]+)", channel_url)
            if match:
                username = match.group(1)
                request = youtube.channels().list(part="id", forUsername=username)
                response = request.execute()
                if response["items"]:
                    channel_id = response["items"][0]["id"]

        if not channel_id:
            print("ERROR: Could not extract channel ID from URL.")
            return "Error: Could not extract channel ID."

        # Fetch channel details
        request = youtube.channels().list(part="snippet,statistics", id=channel_id)
        response = request.execute()

        if not response["items"]:
            print("ERROR: No channel data found.")
            return "Error: No channel data found."

        item = response["items"][0]
        snippet = item["snippet"]
        stats = item["statistics"]

        description = snippet.get("description", "")
        subscribers = stats.get("subscriberCount", "N/A")
        video_count = stats.get("videoCount", "N/A")
        view_count = stats.get("viewCount", "N/A")

        channel_info = f"""
Description: {description}

Subscribers: {subscribers}
Videos: {video_count}
Total Views: {view_count}
"""
        print("DEBUG: Channel info extracted successfully.")
        return channel_info

    except Exception as e:
        print(f"ERROR: Error extracting channel info: {e}")
        return f"Error extracting channel info: {e}"
