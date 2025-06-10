# main.py
import streamlit as st
import logging
from agents import Pipeline
from tools import (
    discover_subreddits,
    extract_channel_info,
    reddit_trend_search,
    google_trends_search,
    youtube_trends_search,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit page setup
st.set_page_config(page_title="TrendForge - AI Growth Engine", layout="wide")

# App title
st.title("🔥 TrendForge: AI Growth Engine for YouTube Creators")

# Session state init
if "step_status" not in st.session_state:
    st.session_state["step_status"] = {
        "discover_subreddits": "pending",
        "extract_channel_info": "pending",
        "run_pipeline": "pending",
    }
if "selected_subreddits" not in st.session_state:
    st.session_state["selected_subreddits"] = []
if "result" not in st.session_state:
    st.session_state["result"] = None
if "pipeline_running" not in st.session_state:
    st.session_state["pipeline_running"] = False
if "subreddits_found" not in st.session_state:
    st.session_state["subreddits_found"] = []

# Sidebar input
with st.sidebar:
    st.header("Step 1: Niche & Channel")
    niche = st.text_input("🎯 Niche (e.g. 'Warhammer', 'Miniature Painting')")
    channel_url = st.text_input("📺 YouTube Channel URL")

    st.header("Step 2: Discover Subreddits")
    if st.button("Find subreddits"):
        st.session_state["step_status"]["discover_subreddits"] = "running"
        st.session_state["selected_subreddits"] = []
        try:
            subreddits = discover_subreddits(niche)
            st.session_state["subreddits_found"] = subreddits
            st.session_state["step_status"]["discover_subreddits"] = "complete"
            st.session_state["step_status"]["extract_channel_info"] = "running"
            channel_info = extract_channel_info(channel_url)
            st.session_state["channel_description"] = channel_info.get("channel_description", "")
            st.session_state["step_status"]["extract_channel_info"] = "complete"
        except Exception as e:
            logger.error(f"Error analyzing channel: {e}")
            st.error(f"Error analyzing channel: {e}")
            st.session_state["step_status"]["extract_channel_info"] = "error"

    if st.session_state["subreddits_found"]:
        st.header("Step 3: Select Subreddits")
        selected_subs = st.multiselect(
            "Select subreddits to analyze:",
            options=st.session_state["subreddits_found"],
            default=st.session_state["selected_subreddits"] or st.session_state["subreddits_found"],
        )
        st.session_state["selected_subreddits"] = selected_subs

    if (
        st.session_state["step_status"]["discover_subreddits"] == "complete"
        and st.session_state["step_status"]["extract_channel_info"] == "complete"
        and st.session_state["selected_subreddits"]
    ):
        if st.button("🚀 Run pipeline"):
            st.session_state["pipeline_running"] = True
            st.session_state["step_status"]["run_pipeline"] = "running"
            st.session_state["result"] = None  # Clear previous result

    # Sidebar status
    st.header("Status")
    for step, status in st.session_state["step_status"].items():
        emoji = "⏳" if status == "running" else "✅" if status == "complete" else "❌" if status == "error" else "🕓"
        st.write(f"{emoji} {step.replace('_', ' ').title()}")

# Main pane content
if st.session_state["pipeline_running"]:
    st.subheader("Analyzing trends and generating content ideas...")
    with st.spinner("Running TrendForge pipeline..."):
        try:
            # Fetch trends
            reddit_trends = reddit_trend_search(st.session_state["selected_subreddits"])
            google_trends = google_trends_search(niche)
            youtube_trends = youtube_trends_search(niche)

            # Run pipeline
            pipeline = Pipeline(
                niche=niche,
                selected_subreddits=st.session_state["selected_subreddits"],
                channel_description=st.session_state.get("channel_description", ""),
            )
            result = pipeline.run(
                reddit_trends=reddit_trends,
                google_trends=google_trends,
                youtube_trends=youtube_trends,
            )
            st.session_state["result"] = result
            st.session_state["pipeline_running"] = False
            st.session_state["step_status"]["run_pipeline"] = "complete"
        except Exception as e:
            logger.error(f"Error running pipeline: {e}")
            st.error(f"Error running pipeline: {e}")
            st.session_state["pipeline_running"] = False
            st.session_state["step_status"]["run_pipeline"] = "error"

# Show results after pipeline complete
if (
    st.session_state["step_status"]["run_pipeline"] == "complete"
    and st.session_state["result"]
):
    st.header("✅ Pipeline complete!")

    result = st.session_state["result"]

    # Trend Summary
    st.markdown("### 📊 Trend Summary\n")
    trend_summary_text = result.get("trend_summary", "")
    if isinstance(trend_summary_text, dict):
        trend_summary_text = trend_summary_text.get("text", "")
    st.markdown(trend_summary_text)

    # Content Plan
    content_plan_text = result.get("content_plan", "")
    st.markdown("### 🎬 Content Plan\n")
    if content_plan_text:
        st.markdown(content_plan_text)
    else:
        st.markdown("_No content plan generated._")

    # Optimized Titles
    titles = result.get("optimized_titles", [])
    st.markdown("### 🧠 Optimized Titles")
    if isinstance(titles, list) and titles:
        for title in titles:
            st.markdown(f"- {title}")
    else:
        st.markdown("_No optimized titles generated._")

    # Thumbnail Ideas
    thumbnails = result.get("thumbnail_ideas", [])
    st.markdown("### 🎨 Thumbnail Ideas")
    if isinstance(thumbnails, list) and thumbnails:
        for idea in thumbnails:
            st.markdown(f"- {idea}")
    else:
        st.markdown("_No thumbnail ideas generated._")
