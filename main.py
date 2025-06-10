import streamlit as st
import logging
from tools import discover_subreddits, extract_channel_info
from agents import Pipeline

# Configure logging
logging.basicConfig(level=logging.INFO)

# Safe text extractor
def safe_extract_text(section):
    if isinstance(section, str):
        return section
    elif isinstance(section, dict) and "text" in section:
        return section["text"]
    else:
        return str(section)

# App Config
st.set_page_config(page_title="🔥 TrendForge: AI Growth Engine for YouTube Creators", page_icon="🔥", layout="wide")

# Initialize Session State
if "step_status" not in st.session_state:
    st.session_state["step_status"] = {
        "subreddits": "pending",
        "channel": "pending",
        "pipeline": "pending"
    }

if "selected_subreddits" not in st.session_state:
    st.session_state["selected_subreddits"] = []

if "result" not in st.session_state:
    st.session_state["result"] = None

# App Title & Intro
st.title("🔥 TrendForge: AI Growth Engine for YouTube Creators")

# Sidebar
with st.sidebar:
    st.header("🚀 Pipeline Steps")
    st.markdown(f"**Subreddit Discovery:** {st.session_state['step_status']['subreddits']}")
    st.markdown(f"**Channel Analysis:** {st.session_state['step_status']['channel']}")
    st.markdown(f"**Pipeline:** {st.session_state['step_status']['pipeline']}")

    st.divider()

    st.header("🎬 Inputs")
    niche = st.text_input("Niche (e.g. Warhammer, Travel Vlogs, Fitness)", key="niche_input")

    youtube_url = st.text_input("YouTube Channel URL", key="youtube_url_input")

    if st.button("🔍 Find Subreddits"):
        logging.info("=== Step 1: Finding subreddits ===")
        st.session_state["step_status"]["subreddits"] = "running"
        st.session_state["step_status"]["pipeline"] = "pending"
        st.session_state["result"] = None

        try:
            st.session_state["discovered_subreddits"] = discover_subreddits(niche)
            logging.info(f"Discovered subreddits: {st.session_state['discovered_subreddits']}")
            st.session_state["step_status"]["subreddits"] = "complete"
        except Exception as e:
            logging.error(f"Error discovering subreddits: {e}")
            st.session_state["discovered_subreddits"] = []
            st.session_state["step_status"]["subreddits"] = f"error ({str(e)})"

    if "discovered_subreddits" in st.session_state:
        st.session_state["selected_subreddits"] = st.multiselect(
            "Select Subreddits to Analyze",
            st.session_state["discovered_subreddits"],
            default=st.session_state["discovered_subreddits"]
        )

    if st.button("📊 Run Pipeline"):
        logging.info("=== Step 2: Running pipeline ===")
        st.session_state["step_status"]["pipeline"] = "running"
        st.session_state["result"] = None
        st.session_state["main_state"] = "analyzing"

# Main Pane
if "main_state" not in st.session_state:
    st.session_state["main_state"] = "idle"

if st.session_state["main_state"] == "idle":
    st.subheader("Welcome to TrendForge!")
    st.markdown("""
    **TrendForge** helps YouTube creators grow their audience with data-driven AI insights.

    **How it works:**
    1. Enter your niche and YouTube channel URL.
    2. Discover relevant subreddits.
    3. Select subreddits to analyze.
    4. Run the pipeline → get trending topics, content ideas, optimized titles, and thumbnail concepts!

    👉 Start by entering your niche and channel URL in the sidebar.
    """)

elif st.session_state["main_state"] == "analyzing":
    st.subheader("Analyzing trends and generating content ideas...")
    with st.spinner("Running TrendForge pipeline..."):
        try:
            logging.info("=== Step 3: Extracting channel info ===")
            channel_description = extract_channel_info(st.session_state["youtube_url_input"])
            logging.info(f"Extracted channel description: {channel_description[:100]}...")
            st.session_state["channel_description"] = channel_description
            st.session_state["step_status"]["channel"] = "complete"

            logging.info("=== Step 4: Initializing Pipeline ===")
            pipeline = Pipeline(
                niche=st.session_state["niche_input"],
                selected_subreddits=st.session_state["selected_subreddits"],
                channel_description=st.session_state["channel_description"]
            )
            logging.info("Pipeline initialized. Running Pipeline.run()...")

            result = pipeline.run()

            logging.info("Pipeline run complete.")
            logging.info(f"Pipeline result: {result}")

            st.session_state["result"] = result
            st.session_state["step_status"]["pipeline"] = "complete"
            st.session_state["main_state"] = "done"

        except Exception as e:
            logging.error(f"Error running pipeline: {e}")
            st.error(f"Error running pipeline: {e}")
            st.session_state["step_status"]["pipeline"] = f"error ({str(e)})"
            st.session_state["main_state"] = "idle"

elif st.session_state["main_state"] == "done":
    st.subheader("✅ Pipeline complete!")
    result = st.session_state["result"]

    # Trend Summary
    st.header("📊 Trend Summary")
    st.markdown(safe_extract_text(result.get("trend_summary", "No trend summary.")))

    # Content Plan
    st.header("🎬 Content Plan")
    content_ideas = result.get("content_ideas", [])
    if content_ideas:
        for idx, idea in enumerate(content_ideas, 1):
            st.markdown(f"{idx}. {idea}")
    else:
        st.markdown("No content ideas.")

    # Optimized Titles
    st.header("🧠 Optimized Titles")
    optimized_titles = result.get("optimized_titles", [])
    if optimized_titles:
        for idx, title in enumerate(optimized_titles, 1):
            st.markdown(f"{idx}. {title}")
    else:
        st.markdown("No optimized titles.")

    # Thumbnail Ideas
    st.header("🎨 Thumbnail Ideas")
    thumbnail_ideas = result.get("thumbnail_ideas", [])
    if thumbnail_ideas:
        for idx, idea in enumerate(thumbnail_ideas, 1):
            st.markdown(f"{idx}. {idea}")
    else:
        st.markdown("No thumbnail ideas.")

    st.divider()
    if st.button("🔄 New Search", key="new_search_button"):
        # Reset state
        logging.info("Resetting app to new search.")
        st.session_state["step_status"] = {
            "subreddits": "pending",
            "channel": "pending",
            "pipeline": "pending"
        }
        st.session_state["selected_subreddits"] = []
        st.session_state["discovered_subreddits"] = []
        st.session_state["result"] = None
        st.session_state["main_state"] = "idle"
        st.rerun()
