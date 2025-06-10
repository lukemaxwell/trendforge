# tools.py

import logging
import os
import praw
from pytrends.request import TrendReq
import time
import re

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load API keys from Streamlit secrets or environment variables
import streamlit as st

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
REDDIT_CLIENT_ID = st.secrets.get("REDDIT_CLIENT_ID", os.getenv("REDDIT_CLIENT_ID"))
REDDIT_CLIENT_SECRET = st.secrets.get("REDDIT_CLIENT_SECRET", os.getenv("REDDIT_CLIENT_SECRET"))
REDDIT_USER_AGENT = st.secrets.get("REDDIT_USER_AGENT", os.getenv("REDDIT_USER_AGENT"))

# Initialize PRAW Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# --- Subreddit discovery ---
def discover_subreddits(niche, max_results=10):
    """Discover relevant subreddits for a given niche."""
    try:
        logging.info(f"Discovering subreddits for niche: {niche}")

        # Simple search using PRAW's subreddit search
        results = []
        for subreddit in reddit.subreddits.search_by_name(query=niche, include_nsfw=False, exact=False):
            # Filter out restricted/private subreddits
            if not subreddit.over18 and not subreddit.quarantine and not subreddit.user_is_banned:
                results.append(subreddit.display_name)
                if len(results) >= max_results:
                    break

        logging.info(f"Found subreddits: {results}")
        return results

    except Exception as e:
        logging.error(f"Error discovering subreddits: {e}")
        return []

# --- Reddit trends search ---
def reddit_trend_search(selected_subreddits, limit=10):
    """Fetch trending topics from selected subreddits."""
    try:
        logging.info(f"Fetching Reddit trends from: {selected_subreddits}")
        trends = {}

        for subreddit_name in selected_subreddits:
            subreddit = reddit.subreddit(subreddit_name)
            titles = []
            for post in subreddit.hot(limit=limit):
                titles.append(post.title)

            trends[subreddit_name] = titles
            time.sleep(1)  # be nice to Reddit

        # Combine into a simple text summary
        trend_summary = ""
        for sub, titles in trends.items():
            trend_summary += f"\n### r/{sub}\n"
            for title in titles:
                trend_summary += f"- {title}\n"

        return trend_summary

    except Exception as e:
        logging.error(f"Error fetching Reddit trends: {e}")
        return "Error fetching Reddit trends."

# --- Google trends search ---
def google_trends_search(niche):
    """Fetch related Google trends for the niche."""
    try:
        logging.info(f"Fetching Google trends for niche: {niche}")
        pytrends = TrendReq()
        pytrends.build_payload([niche], timeframe='now 7-d')

        related_queries_result = pytrends.related_queries()
        related_queries = []

        for kw, data in related_queries_result.items():
            if data and data.get("top") is not None:
                df = data["top"]
                related_queries.extend(df["query"].tolist())

        # De-duplicate
        related_queries = list(dict.fromkeys(related_queries))

        # Combine to text
        summary = ""
        for query in related_queries:
            summary += f"- {query}\n"

        return summary or "No related queries found."

    except Exception as e:
        logging.error(f"Error fetching Google trends: {e}")
        return "Error fetching Google trends."

# --- Extract YouTube channel info ---
def extract_channel_info(yt_url):
    """Extract YouTube channel description (placeholder)."""
    try:
        logging.info(f"Extracting channel info for URL: {yt_url}")

        # Example: extract channel ID (if needed in future real API)
        channel_id_match = re.search(r"(?:\/channel\/|\/c\/|\/user\/|youtube\.com\/@)([^\/?\s]+)", yt_url)
        channel_id = channel_id_match.group(1) if channel_id_match else "unknown"

        # Dummy channel description for now
        channel_description = f"Extracted channel description for URL: {yt_url} (channel ID: {channel_id})"

        return {"channel_description": channel_description}

    except Exception as e:
        logging.error(f"Error extracting channel info: {e}")
        return {"channel_description": ""}
