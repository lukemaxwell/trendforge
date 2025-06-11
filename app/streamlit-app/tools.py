# tools.py
import os
import logging
import streamlit as st
from dotenv import load_dotenv
from pytrends.request import TrendReq
import praw
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Initialize Reddit
try:
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    reddit_readable = True
    logger.info("✅ Reddit API initialized")
except Exception as e:
    reddit_readable = False
    logger.warning(f"⚠️ Reddit init failed: {e}")

# --- Discover Subreddits ---
def discover_subreddits(niche, limit=15):
    logger.info(f"🔍 Discovering subreddits for niche: {niche}")
    if not reddit_readable:
        logger.warning("Reddit API not available. Returning empty subreddit list.")
        return []

    try:
        subreddits = []
        # Use search() instead of search_by_name
        search_results = list(reddit.subreddits.search(query=niche, limit=limit))
        for sr in search_results:
            subreddits.append(sr.display_name)

        # Fallback for common niches
        if len(subreddits) == 0:
            if "warhammer" in niche.lower() or "miniature" in niche.lower():
                subreddits = [
                    "Warhammer",
                    "Warhammer40k",
                    "PaintingWarhammer",
                    "minipainting",
                    "miniatures",
                    "AgeOfSigmar",
                    "WarhammerFantasy"
                ]
                logger.info("✅ Using fallback subreddits for Warhammer niche.")

        logger.info(f"✅ Found subreddits: {subreddits}")
        return subreddits
    except Exception as e:
        logger.error(f"Error discovering subreddits: {e}")
        return []

# --- Extract Channel Info ---
def extract_channel_info(channel_url):
    logger.info(f"📺 Extracting channel info from URL: {channel_url}")

    # Extract channel ID
    match = re.search(r"(?:/channel/|/c/|/user/|@)([^/?]+)", channel_url)
    if not match:
        raise ValueError("Could not extract channel ID from URL")

    channel_id = match.group(1)
    logger.info(f"✅ Extracted channel ID: {channel_id}")

    # Simulate channel info (replace with YouTube Data API if needed)
    simulated_description = f"Simulated channel description for {channel_id}. This channel focuses on amazing content about {channel_id}'s niche."

    return {
        "channel_id": channel_id,
        "channel_description": simulated_description
    }

# --- Reddit Trend Search ---
def reddit_trend_search(subreddits, limit=10):
    logger.info(f"🔍 Searching Reddit trends for subreddits: {subreddits}")
    if not reddit_readable:
        logger.warning("Reddit API not available. Returning empty trends.")
        return "Reddit trends unavailable."

    trends = []
    try:
        for sub in subreddits:
            subreddit = reddit.subreddit(sub)
            for post in subreddit.hot(limit=limit):
                trends.append(post.title)
        logger.info(f"✅ Retrieved {len(trends)} Reddit trends.")
        return "\n".join(f"- {trend}" for trend in trends)
    except Exception as e:
        logger.error(f"Error fetching Reddit trends: {e}")
        return "Error fetching Reddit trends."

# --- Google Trends Search ---
def google_trends_search(niche):
    logger.info(f"🔍 Searching Google trends for niche: {niche}")
    try:
        pytrends = TrendReq(hl="en-US", tz=360)
        pytrends.build_payload([niche], timeframe="now 7-d")
        related_queries_result = pytrends.related_queries()
        top_queries = []

        for key, value in related_queries_result.items():
            try:
                top = value["top"]
                if top is not None:
                    top_queries.extend(top["query"].tolist())
            except Exception as e:
                logger.warning(f"Warning parsing Google trends: {e}")

        if not top_queries:
            logger.info("No Google trends found.")
            return "No Google trends found."

        logger.info(f"✅ Retrieved {len(top_queries)} Google trends.")
        return "\n".join(f"- {query}" for query in top_queries)
    except Exception as e:
        logger.error(f"Error fetching Google trends: {e}")
        return "Error fetching Google trends."

# --- YouTube Trends Search (Simulated) ---
def youtube_trends_search(niche):
    logger.info(f"🔍 Simulating YouTube trends for niche: {niche}")
    # Replace with real YouTube Data API if needed
    simulated_trends = [
        f"Top YouTube video idea for {niche} #1",
        f"Top YouTube video idea for {niche} #2",
        f"Top YouTube video idea for {niche} #3",
        f"Top YouTube video idea for {niche} #4",
        f"Top YouTube video idea for {niche} #5",
    ]
    logger.info("✅ Simulated YouTube trends ready.")
    return "\n".join(f"- {trend}" for trend in simulated_trends)
