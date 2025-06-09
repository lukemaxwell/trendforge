# main.py

import streamlit as st
from agents import Pipeline
from tools import discover_subreddits, extract_channel_info

# --- Streamlit config ---
st.set_page_config(page_title="TrendForge", page_icon="🔥", layout="wide")
st.title("🔥 TrendForge - AI-Led Growth for YouTube Creators")

# --- Session State init ---
if "niche" not in st.session_state:
    st.session_state["niche"] = ""
if "subreddits" not in st.session_state:
    st.session_state["subreddits"] = []
if "selected_subreddits" not in st.session_state:
    st.session_state["selected_subreddits"] = []
if "channel_url" not in st.session_state:
    st.session_state["channel_url"] = ""
if "channel_description" not in st.session_state:
    st.session_state["channel_description"] = ""
if "channel_ready" not in st.session_state:
    st.session_state["channel_ready"] = False
if "pipeline_output" not in st.session_state:
    st.session_state["pipeline_output"] = None

# --- Functions ---
def reset_search():
    st.session_state["niche"] = ""
    st.session_state["subreddits"] = []
    st.session_state["selected_subreddits"] = []
    st.session_state["channel_url"] = ""
    st.session_state["channel_description"] = ""
    st.session_state["channel_ready"] = False
    st.session_state["pipeline_output"] = None

# --- UI: Niche input ---
st.header("🕵️‍♂️ Discover Subreddits")

niche_input = st.text_input("Enter your niche/topic", value=st.session_state["niche"])

if st.button("🔍 Discover Subreddits"):
    st.session_state["niche"] = niche_input
    with st.spinner("Discovering subreddits..."):
        discovered_subreddits = discover_subreddits(niche_input)
    st.session_state["subreddits"] = discovered_subreddits
    st.session_state["selected_subreddits"] = discovered_subreddits  # Auto-select all initially

# --- UI: Subreddits selection ---
if st.session_state["subreddits"]:
    st.write("### Select Subreddits to Analyze:")
    selected = st.multiselect(
        "Subreddits:",
        st.session_state["subreddits"],
        default=st.session_state["selected_subreddits"]
    )
    st.session_state["selected_subreddits"] = selected
elif st.session_state["niche"]:
    st.info("No subreddits found — try a broader niche or add manually.")

# --- UI: YouTube channel input ---
st.header("📺 Channel Analysis")

channel_url_input = st.text_input("Enter YouTube channel URL", value=st.session_state["channel_url"])

if st.button("📥 Analyze Channel"):
    st.session_state["channel_url"] = channel_url_input
    with st.spinner("Extracting channel info..."):
        channel_info = extract_channel_info(st.session_state["channel_url"])
    # PATCHED: store channel_info directly (string)
    st.session_state["channel_description"] = channel_info
    st.session_state["channel_ready"] = True
    st.rerun()

# --- UI: Channel preview ---
if st.session_state["channel_ready"]:
    st.write("### Channel Info:")
    st.text_area("Channel Description", st.session_state["channel_description"], height=200)

# --- UI: Run Pipeline ---
st.header("🚀 Run Growth Pipeline")

if st.button("🧠 Run Pipeline"):
    with st.spinner("Running AI pipeline... this may take a minute..."):
        try:
            output = Pipeline(
                st.session_state["niche"],
                st.session_state["selected_subreddits"],
                st.session_state["channel_description"]
            )
            st.session_state["pipeline_output"] = output
        except Exception as e:
            st.error(f"Error running pipeline: {e}")

# --- UI: Show Pipeline Output ---
if st.session_state["pipeline_output"]:
    output = st.session_state["pipeline_output"]

    st.header("📈 Pipeline Results")

    with st.expander("🗂 Reddit Trends"):
        st.text(output["reddit_trends"])

    with st.expander("🔎 Google Trends"):
        st.text(output["google_trends"])

    with st.expander("📺 YouTube Trends"):
        st.text(output["youtube_trends"])

    with st.expander("🧑‍🔬 Trend Summary"):
        st.text(output["trend_summary"])

    with st.expander("🎬 Content Plan"):
        st.text(output["content_plan"])

    with st.expander("📝 Optimized Titles"):
        st.text(output["optimized_titles"])

    with st.expander("🖼 Thumbnail Ideas"):
        st.text(output["thumbnail_ideas"])

# --- UI: New Search ---
st.divider()
st.button("🔄 New Search", on_click=reset_search, key="new_search_button")
