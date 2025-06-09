# main.py

import streamlit as st
from agents import Pipeline
from tools import discover_subreddits, extract_channel_info

# Initialize session state
if "discovered_subreddits" not in st.session_state:
    st.session_state["discovered_subreddits"] = []

if "selected_subreddits" not in st.session_state:
    st.session_state["selected_subreddits"] = []

if "pipeline_run" not in st.session_state:
    st.session_state["pipeline_run"] = False

if "reddit_trends" not in st.session_state:
    st.session_state["reddit_trends"] = ""

if "google_trends" not in st.session_state:
    st.session_state["google_trends"] = ""

if "youtube_trends" not in st.session_state:
    st.session_state["youtube_trends"] = ""

if "trend_summary" not in st.session_state:
    st.session_state["trend_summary"] = ""

if "content_plan" not in st.session_state:
    st.session_state["content_plan"] = ""

if "optimized_titles" not in st.session_state:
    st.session_state["optimized_titles"] = ""

if "thumbnail_ideas" not in st.session_state:
    st.session_state["thumbnail_ideas"] = ""

# App UI
st.title("📈 TrendForge - AI YouTube Growth Toolkit")

# --- Step 1: User input ---
st.header("🔍 Enter Niche + YouTube Channel URL")

niche = st.text_input("Niche / Topic", value="", placeholder="e.g. Warhammer painting")
channel_url = st.text_input("YouTube Channel URL (optional)", value="")

if st.button("Discover Subreddits + Extract Channel Info"):
    if niche.strip() == "":
        st.warning("Please enter a niche!")
    else:
        # Discover subreddits
        subreddits = discover_subreddits(niche)
        st.session_state["discovered_subreddits"] = subreddits
        st.session_state["selected_subreddits"] = subreddits.copy()

        # Extract channel info
        if channel_url:
            channel_info = extract_channel_info(channel_url)
            st.session_state["channel_description"] = channel_info.get("channel_description", "")
            st.session_state["recent_videos"] = channel_info.get("recent_videos", [])
        else:
            st.session_state["channel_description"] = ""
            st.session_state["recent_videos"] = []

        # Reset pipeline run state
        st.session_state["pipeline_run"] = False

# --- Step 2: Show channel analysis ---
if "channel_description" in st.session_state and st.session_state["channel_description"]:
    st.header("📺 Channel Analysis")
    st.write(st.session_state["channel_description"])

    st.subheader("Recent Videos")
    for video in st.session_state["recent_videos"]:
        st.markdown(f"- [{video['title']}]({video['url']}) | {video.get('view_count', 0)} views")

# --- Step 3: Subreddit selection ---
if st.session_state["discovered_subreddits"]:
    st.header("🗂️ Select Subreddits to use")

    selected_subs = []
    for sub in st.session_state["discovered_subreddits"]:
        if st.checkbox(sub, value=sub in st.session_state["selected_subreddits"], key=f"checkbox_{sub}"):
            selected_subs.append(sub)

    st.session_state["selected_subreddits"] = selected_subs

# --- Step 4: Run pipeline ---
if st.session_state["selected_subreddits"]:
    if st.button("🚀 Run TrendForge Pipeline"):
        try:
            # Run pipeline
            results = Pipeline(
                niche=niche,
                selected_subreddits=st.session_state["selected_subreddits"],
                channel_description=st.session_state.get("channel_description", ""),
            )

            # Store results
            st.session_state["reddit_trends"] = results.get("reddit_trends", "")
            st.session_state["google_trends"] = results.get("google_trends", "")
            st.session_state["youtube_trends"] = results.get("youtube_trends", "")
            st.session_state["trend_summary"] = results.get("trend_summary", "")
            st.session_state["content_plan"] = results.get("content_plan", "")
            st.session_state["optimized_titles"] = results.get("optimized_titles", "")
            st.session_state["thumbnail_ideas"] = results.get("thumbnail_ideas", "")

            st.session_state["pipeline_run"] = True

        except Exception as e:
            st.error(f"Error running pipeline: {e}")

# --- Step 5: Show results ---
if st.session_state["pipeline_run"]:
    st.header("📊 Trends")

    st.subheader("📈 Reddit Trends")
    st.code(st.session_state["reddit_trends"])

    st.subheader("📈 Google Trends")
    st.code(st.session_state["google_trends"])

    st.subheader("📈 YouTube Trends")
    st.code(st.session_state["youtube_trends"])

    st.header("📝 Trend Summary")
    st.write(st.session_state["trend_summary"])

    st.header("📅 Content Plan")
    st.write(st.session_state["content_plan"])

    st.header("🏷️ Optimized Titles")
    st.write(st.session_state["optimized_titles"])

    st.header("🖼️ Thumbnail Ideas")
    st.write(st.session_state["thumbnail_ideas"])

# --- New search ---
if st.button("🔄 New Search", key="new_search_button"):
    # Reset all session state keys
    for key in [
        "discovered_subreddits",
        "selected_subreddits",
        "pipeline_run",
        "reddit_trends",
        "google_trends",
        "youtube_trends",
        "trend_summary",
        "content_plan",
        "optimized_titles",
        "thumbnail_ideas",
        "channel_description",
        "recent_videos",
    ]:
        st.session_state[key] = []
        if key == "pipeline_run":
            st.session_state[key] = False
