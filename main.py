# main.py

import streamlit as st
import logging
from tools import discover_subreddits, extract_channel_info
from agents import Pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)

# Streamlit app config
st.set_page_config(page_title="TrendForge - AI Growth Engine for YouTube Creators", page_icon="🔥", layout="wide")

# Initialize session state
if "selected_subreddits" not in st.session_state:
    st.session_state["selected_subreddits"] = []
if "discovered_subreddits" not in st.session_state:
    st.session_state["discovered_subreddits"] = []
if "pipeline_result" not in st.session_state:
    st.session_state["pipeline_result"] = None
if "step_status" not in st.session_state:
    st.session_state["step_status"] = "idle"
if "niche" not in st.session_state:
    st.session_state["niche"] = ""
if "youtube_url" not in st.session_state:
    st.session_state["youtube_url"] = ""
if "channel_description" not in st.session_state:
    st.session_state["channel_description"] = ""

# App header
st.markdown("# 🔥 TrendForge: AI Growth Engine for YouTube Creators")

# Sidebar input
st.sidebar.header("1️⃣ Enter Input")

st.sidebar.markdown("### Niche / Topic")
niche_input = st.sidebar.text_input("Niche (e.g. Warhammer, Cold Plunge, Yoga, etc.)", value=st.session_state["niche"])

st.sidebar.markdown("### YouTube Channel URL (optional)")
youtube_url_input = st.sidebar.text_input("YouTube Channel URL", value=st.session_state["youtube_url"])

# Button to discover subreddits
if st.sidebar.button("🔍 Find Subreddits"):
    st.session_state["niche"] = niche_input
    st.session_state["youtube_url"] = youtube_url_input

    try:
        # Extract channel description
        channel_info = extract_channel_info(st.session_state["youtube_url"])
        st.session_state["channel_description"] = channel_info.get("channel_description", "")
    except Exception as e:
        st.error(f"Error analyzing channel: {e}")
        st.session_state["channel_description"] = ""

    # Discover subreddits
    subreddits = discover_subreddits(st.session_state["niche"])
    st.session_state["discovered_subreddits"] = subreddits
    st.session_state["selected_subreddits"] = subreddits  # default all selected

# Sidebar select subreddits
if st.session_state["discovered_subreddits"]:
    st.sidebar.header("2️⃣ Select Subreddits")
    st.sidebar.multiselect(
        "Choose subreddits to analyze:",
        st.session_state["discovered_subreddits"],
        default=st.session_state["selected_subreddits"],
        key="selected_subreddits"
    )

# Sidebar run pipeline button
st.sidebar.header("3️⃣ Run Pipeline")
if st.sidebar.button("🚀 Run Pipeline"):
    if not st.session_state["selected_subreddits"]:
        st.warning("Please select at least one subreddit.")
    else:
        st.session_state["step_status"] = "running"
        st.session_state["pipeline_result"] = None
        st.rerun()

# Sidebar new search button
if st.sidebar.button("🔄 New Search"):
    st.session_state["selected_subreddits"] = []
    st.session_state["discovered_subreddits"] = []
    st.session_state["pipeline_result"] = None
    st.session_state["step_status"] = "idle"
    st.session_state["niche"] = ""
    st.session_state["youtube_url"] = ""
    st.session_state["channel_description"] = ""
    st.rerun()

# --- MAIN PANE ---

# Show progress or results
if st.session_state["step_status"] == "running":
    st.info("Analyzing trends and generating content ideas...")

    try:
        # Run pipeline
        pipeline = Pipeline(
            niche=st.session_state["niche"],
            selected_subreddits=st.session_state["selected_subreddits"],
            channel_description=st.session_state["channel_description"],
        )
        result = pipeline.run()

        # Save result
        st.session_state["pipeline_result"] = result
        st.session_state["step_status"] = "complete"
        st.rerun()
    except Exception as e:
        st.error(f"Error running pipeline: {e}")
        st.session_state["step_status"] = "idle"

elif st.session_state["step_status"] == "complete" and st.session_state["pipeline_result"]:
    st.success("✅ Pipeline complete!")

    result = st.session_state["pipeline_result"]

    # Helper
    def safe_extract_text(obj, key):
        val = obj.get(key, "")
        if isinstance(val, dict):
            return val.get("text", "")
        return str(val)

    # Display sections
    st.markdown("### 📊 Trend Summary")
    st.markdown(safe_extract_text(result, "trend_summary"))

    st.markdown("### 🎬 Content Plan")
    st.markdown(safe_extract_text(result, "content_plan"))

    st.markdown("### 🧠 Optimized Titles")
    st.markdown(safe_extract_text(result, "optimized_titles"))

    st.markdown("### 🎨 Thumbnail Ideas")
    st.markdown(safe_extract_text(result, "thumbnail_ideas"))

else:
    # Initial instructions
    st.markdown("## Welcome to TrendForge!")
    st.markdown("""
    **TrendForge** helps YouTube creators discover trending topics and generate AI-powered content ideas.

    👉 Enter a niche and optionally your YouTube channel  
    👉 Discover relevant subreddits to analyze  
    👉 Run the pipeline to get a content plan and optimized ideas  
    """)
