# FINAL FINAL main.py

import streamlit as st
from agents import Pipeline
from tools import (
    discover_subreddits,
    extract_channel_info,
    reddit_trend_search,
    google_trends_search,
    youtube_trends_search
)

# Initialize session state
if "step_status" not in st.session_state:
    st.session_state["step_status"] = {
        "subreddits": "not_started",
        "pipeline": "not_started"
    }
if "discovered_subreddits" not in st.session_state:
    st.session_state["discovered_subreddits"] = []
if "selected_subreddits" not in st.session_state:
    st.session_state["selected_subreddits"] = []
if "channel_description" not in st.session_state:
    st.session_state["channel_description"] = ""
if "result" not in st.session_state:
    st.session_state["result"] = None

# App title
st.set_page_config(page_title="TrendForge - AI Growth Engine for YouTube Creators", layout="wide")
st.title("🔥 TrendForge: AI Growth Engine for YouTube Creators")
st.write("TrendForge analyzes YouTube trends, your channel, and Reddit/Google trends to generate optimized content ideas, titles, and thumbnails. 🚀")

# Sidebar - user input
st.sidebar.header("Step 1: Define your niche and channel")

with st.sidebar.form(key="input_form"):
    niche_query = st.text_input("Enter niche/topic", value="Warhammer")
    youtube_url = st.text_input("YouTube Channel URL (optional)", value="")
    submit_button = st.form_submit_button(label="Find Subreddits")

# Handle Find Subreddits button
if submit_button:
    st.session_state["step_status"]["subreddits"] = "in_progress"
    st.experimental_rerun()

# Main pane
main_placeholder = st.empty()

# Subreddit discovery logic
if st.session_state["step_status"]["subreddits"] == "in_progress":
    with main_placeholder.container():
        st.write("🔍 Discovering subreddits...")
        subreddits = discover_subreddits(niche_query)
        st.session_state["discovered_subreddits"] = subreddits
        st.session_state["step_status"]["subreddits"] = "complete"
        st.experimental_rerun()

# Sidebar - show discovered subreddits if available
if st.session_state["step_status"]["subreddits"] == "complete":
    st.sidebar.header("Step 2: Select subreddits to analyze")
    if st.session_state["discovered_subreddits"]:
        selected_subs = st.sidebar.multiselect(
            "Select subreddits:",
            st.session_state["discovered_subreddits"],
            default=st.session_state["discovered_subreddits"]
        )
        st.session_state["selected_subreddits"] = selected_subs
    else:
        st.sidebar.warning("No subreddits found — try a broader niche or add manually.")
        st.session_state["selected_subreddits"] = []

    st.sidebar.header("Step 3: Run pipeline")
    if st.sidebar.button("🚀 Run Pipeline"):
        st.session_state["step_status"]["pipeline"] = "in_progress"
        st.session_state["result"] = None
        st.experimental_rerun()

# Main pane logic for pipeline
if st.session_state["step_status"]["pipeline"] == "in_progress":
    with main_placeholder.container():
        st.write("🛠️ Running TrendForge pipeline...")
        try:
            # Extract channel description if URL provided
            channel_description = ""
            if youtube_url:
                try:
                    channel_info = extract_channel_info(youtube_url)
                    channel_description = channel_info.get("channel_description", "") if isinstance(channel_info, dict) else ""
                    st.session_state["channel_description"] = channel_description
                except Exception as e:
                    st.warning(f"Error analyzing channel: {e}")

            # Run pipeline
            pipeline = Pipeline(
                niche=niche_query,
                selected_subreddits=st.session_state["selected_subreddits"],
                channel_description=st.session_state["channel_description"]
            )
            result = pipeline.run()
            st.session_state["result"] = result
            st.session_state["step_status"]["pipeline"] = "complete"
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error running pipeline: {e}")
            st.session_state["step_status"]["pipeline"] = "not_started"

# Display final result
if st.session_state["step_status"]["pipeline"] == "complete" and st.session_state["result"]:
    with main_placeholder.container():
        st.header("✅ Pipeline complete!")

        def safe_extract_text(data, key):
            value = data.get(key, "")
            if isinstance(value, str):
                return value
            elif isinstance(value, list):
                return "\n".join([f"- {v}" for v in value])
            else:
                return str(value)

        st.subheader("📊 Trend Summary")
        st.markdown(safe_extract_text(st.session_state["result"], "trend_summary"))

        st.subheader("🎬 Content Plan")
        st.markdown(safe_extract_text(st.session_state["result"], "content_plan"))

        st.subheader("🧠 Optimized Titles")
        st.markdown(safe_extract_text(st.session_state["result"], "optimized_titles"))

        st.subheader("🎨 Thumbnail Ideas")
        st.markdown(safe_extract_text(st.session_state["result"], "thumbnail_ideas"))
