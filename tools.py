# tools.py

import os
import logging
import streamlit as st
from dotenv import load_dotenv
import praw
from pytrends.request import TrendReq
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import openai
import yt_dlp

# Setup logging
logger = logging.getLogger(__name__)

# Load local .env (for local dev)
load_dotenv()

# Load keys — Streamlit secrets take priority if present
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
REDDIT_CLIENT_ID = st.secrets.get("REDDIT_CLIENT_ID", os.getenv("REDDIT_CLIENT_ID"))
REDDIT_CLIENT_SECRET = st.secrets.get("REDDIT_CLIENT_SECRET", os.getenv("REDDIT_CLIENT_SECRET"))
REDDIT_USER_AGENT = st.secrets.get("REDDIT_USER_AGENT", os.getenv("REDDIT_USER_AGENT"))

# Setup NLTK
nltk.download("stopwords")
nltk.download("punkt")

# Reddit client
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
)

# Google Trends client
pytrends = TrendReq(hl="en-US", tz=360)

# Discover subreddits
def discover_subreddits(niche: str) -> list[str]:
    try:
        subreddits = []
        results = reddit.subreddits.search(query=niche, limit=20)
        for sub in results:
            if sub.subscribers > 1000:
                subreddits.append(sub.display_name)
        return subreddits
    except Exception as e:
        logger.error(f"Error discovering subreddits: {e}")
        return []

# Reddit trend search
def reddit_trend_search(subreddits: list[str]) -> str:
    try:
        combined_titles = ""
        for subreddit_name in subreddits:
            subreddit = reddit.subreddit(subreddit_name)
            for submission in subreddit.hot(limit=10):
                combined_titles += f"{submission.title}\n"

        stop_words = set(stopwords.words("english"))
        word_tokens = word_tokenize(combined_titles.lower())
        filtered_tokens = [word for word in word_tokens if word.isalnum() and word not in stop_words]

        freq = {}
        for word in filtered_tokens:
            freq[word] = freq.get(word, 0) + 1

        sorted_freq = sorted(freq.items(), key=lambda item: item[1], reverse=True)
        top_keywords = sorted_freq[:20]

        result = "\n".join([f"{word}: {count}" for word, count in top_keywords])
        return result

    except Exception as e:
        logger.error(f"Error in reddit_trend_search: {e}")
        return "Error fetching Reddit trends."

# Google trends search
def google_trends_search(niche: str) -> str:
    try:
        kw_list = [niche]
        pytrends.build_payload(kw_list, cat=0, timeframe="now 7-d", geo="", gprop="")

        related_queries_result = pytrends.related_queries()

        trends = ""
        for kw in kw_list:
            try:
                ranked_keywords = related_queries_result[kw]["top"]
                if ranked_keywords is None:
                    trends += f"No related queries found for '{kw}'.\n"
                    continue
                for index, row in ranked_keywords.iterrows():
                    trends += f"{row['query']} ({row['value']})\n"
            except Exception as e:
                trends += f"Error fetching related queries for '{kw}': {e}\n"

        return trends

    except Exception as e:
        logger.error(f"Error in google_trends_search: {e}")
        return "Error fetching Google Trends."

# YouTube trends (placeholder)
def youtube_trend_search(niche: str) -> str:
    try:
        mock_trends = [
            f"{niche} unboxing",
            f"Top 10 {niche} tips",
            f"{niche} beginner guide",
            f"{niche} review",
            f"{niche} live painting session",
        ]
        return "\n".join(mock_trends)

    except Exception as e:
        logger.error(f"Error in youtube_trend_search: {e}")
        return "Error fetching YouTube Trends."

# Channel analysis
def channel_analysis_tool(channel_description: str) -> str:
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert YouTube channel strategist."},
                {"role": "user", "content": f"Analyze this channel description and summarize its main audience interests and content style:\n\n{channel_description}"}
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        logger.error(f"Error in channel_analysis_tool: {e}")
        return "Error analyzing channel."

# Extract channel info from URL
def extract_channel_info(channel_url: str) -> dict:
    try:
        ydl_opts = {
            'extract_flat': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)

        channel_description = info.get('description', '')
        entries = info.get('entries', [])

        recent_videos = []
        for entry in entries[:10]:
            video = {
                'title': entry.get('title'),
                'url': entry.get('url'),
                'view_count': entry.get('view_count'),
                'like_count': entry.get('like_count'),
                'comment_count': entry.get('comment_count'),
            }
            recent_videos.append(video)

        return {
            'channel_description': channel_description,
            'recent_videos': recent_videos,
        }

    except Exception as e:
        logger.error(f"Error extracting channel info: {e}")
        return {
            'channel_description': '',
            'recent_videos': [],
        }
