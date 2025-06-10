import streamlit as st
import logging
from agents import Pipeline
from tools import discover_subreddits, extract_channel_info

# Setup logging
logging.basicConfig(level=logging.INFO)

# Page Config
st.set_page_config(page_title="TrendForge: AI Growth Engine for YouTube Creators", layout="wide")

# App Title
st.title("🔥 TrendForge: AI Growth Engine for YouTube Creators")
st.markdown("**Supercharge your YouTube growth with data-driven AI insights and trending content ideas.**")
st.markdown("**Steps:** Input your niche and channel → Select relevant subreddits → Run Pipeline → Get Growth Ideas 🚀")

# Initialize session state
if "selected_subreddits" not in st.session_state:
    st.session_state["selected_subreddits"] = []

if "pipeline_result" not in st.session_state:
    st.session_state["pipeline_result"] = None

if "step_status" not in st.session_state:
    st.session_state["step_status"] = {
        "discover_subreddits": "pending",
        "extract_channel": "pending",
        "pipeline": "pending",
    }

if "main_state" not in st.session_state:
    st.session_state["main_state"] = "idle"

# Sidebar
with st.sidebar:
    st.header("🛠️ Configure")

    niche = st.text_input("🎯 Niche / Topic", placeholder="e.g. Warhammer, Yoga, Personal Finance")
    yt_url = st.text_input("📺 YouTube Channel URL", placeholder="Paste full channel URL")

    # Step 1: Discover Subreddits
    if st.button("🔍 Find Subreddits"):
        if not niche:
            st.warning("Please enter a niche first!")
        else:
            st.session_state["step_status"]["discover_subreddits"] = "running"
            try:
                subreddits = discover_subreddits(niche)
                if subreddits:
                    st.session_state["selected_subreddits"] = subreddits
                    st.session_state["step_status"]["discover_subreddits"] = "complete"
                    st.success(f"Found {len(subreddits)} subreddits!")
                else:
                    st.session_state["step_status"]["discover_subreddits"] = "no results"
                    st.warning("No subreddits found — try a broader niche or add manually.")
            except Exception as e:
                logging.error(f"Error discovering subreddits: {e}")
                st.session_state["step_status"]["discover_subreddits"] = "error"
                st.error(f"Error discovering subreddits: {e}")

    st.markdown("---")

    # Subreddit selection
    st.session_state["selected_subreddits"] = st.multiselect(
        "🗂️ Selected Subreddits",
        options=st.session_state.get("selected_subreddits", []),
        default=st.session_state.get("selected_subreddits", []),
        key="subreddit_multiselect"
    )

    st.markdown("---")

    # Step 2: Extract channel info
    if yt_url:
        st.session_state["step_status"]["extract_channel"] = "running"
        try:
            channel_info = extract_channel_info(yt_url)
            st.session_state["channel_description"] = channel_info.get("channel_description", "")
            st.session_state["step_status"]["extract_channel"] = "complete"
            st.success("Channel description extracted!")
        except Exception as e:
            logging.error(f"Error analyzing channel: {e}")
            st.session_state["step_status"]["extract_channel"] = "error"
            st.session_state["channel_description"] = ""
            st.error(f"Error analyzing channel: {e}")

    else:
        st.session_state["channel_description"] = ""

    # Run Pipeline
    if st.button("🚀 Run Pipeline"):
        if not niche or not st.session_state["selected_subreddits"]:
            st.warning("Please enter niche and select subreddits first!")
        else:
            st.session_state["step_status"]["pipeline"] = "running"
            st.session_state["main_state"] = "running"
            st.session_state["pipeline_result"] = None

    st.markdown("---")
    st.markdown("### Step Progress")
    for step, status in st.session_state["step_status"].items():
        emoji = "🟢" if status == "complete" else "🟡" if status == "running" else "⚪️"
        st.write(f"{emoji} **{step.replace('_', ' ').title()}** → `{status}`")

# Main content area
if st.session_state["main_state"] == "idle":
    st.header("📈 Welcome to TrendForge!")
    st.markdown("Input your niche and YouTube channel on the left. Then click **Find Subreddits** → **Run Pipeline** to generate your custom content growth report.")

elif st.session_state["main_state"] == "running":
    st.header("Analyzing trends and generating content ideas...")
    with st.spinner("Crunching Reddit, Google & YouTube trends... 🚀"):
        try:
            # Run pipeline
            pipeline = Pipeline()
            result = pipeline.run(
                niche=niche,
                selected_subreddits=st.session_state["selected_subreddits"],
                channel_description=st.session_state["channel_description"],
            )
            # Save result
            st.session_state["pipeline_result"] = result
            st.session_state["step_status"]["pipeline"] = "complete"
            st.session_state["main_state"] = "complete"

        except Exception as e:
            logging.error(f"Error running pipeline: {e}")
            st.session_state["step_status"]["pipeline"] = f"error ({str(e)})"
            st.session_state["main_state"] = "idle"
            st.error(f"Error running pipeline: {e}")

elif st.session_state["main_state"] == "complete" and st.session_state["pipeline_result"]:
    st.header("✅ Pipeline complete!")
    result = st.session_state["pipeline_result"]

    # Safe extract
    def safe_extract_text(result_dict, key):
        try:
            value = result_dict.get(key, "")
            if isinstance(value, dict) and "text" in value:
                return value["text"]
            if isinstance(value, str):
                return value
            return ""
        except Exception as e:
            logging.warning(f"Error extracting {key}: {e}")
            return ""

    # Display final report
    st.header("📊 Trend Summary")
    st.markdown(safe_extract_text(result, "trend_summary"))

    st.header("🎬 Content Plan")
    st.markdown(safe_extract_text(result, "content_plan"))

    st.header("🧠 Optimized Titles")
    st.markdown(safe_extract_text(result, "optimized_titles"))

    st.header("🎨 Thumbnail Ideas")
    st.markdown(safe_extract_text(result, "thumbnail_ideas"))
