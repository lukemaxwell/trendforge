import streamlit as st
from agents import Pipeline
from tools import discover_subreddits, extract_channel_info, reddit_trend_search, google_trends_search, youtube_trends_search

# --- Helper Functions ---
def safe_extract_text(obj, key):
    val = obj.get(key, "")
    if isinstance(val, dict):
        return val.get("text", "")
    elif isinstance(val, list):
        # Render list nicely in markdown
        return "\n".join([f"- {item}" for item in val])
    return str(val)

# --- App Config ---
st.set_page_config(page_title="TrendForge: AI Growth Engine for YouTube Creators", layout="wide")

# --- Sidebar ---
st.sidebar.title("🔥 TrendForge")
st.sidebar.subheader("AI Growth Engine for YouTube Creators")
st.sidebar.markdown(
    """
    Enter your niche and YouTube channel URL below. TrendForge will analyze trends from Reddit, Google, and YouTube, 
    extract your channel data, and generate optimized content ideas.
    """
)

niche = st.sidebar.text_input("🎯 Enter your niche", value=st.session_state.get("niche", ""))
channel_url = st.sidebar.text_input("📺 Enter YouTube channel URL", value=st.session_state.get("channel_url", ""))

if "discovered_subreddits" not in st.session_state:
    st.session_state["discovered_subreddits"] = []

if "selected_subreddits" not in st.session_state:
    st.session_state["selected_subreddits"] = []

if "pipeline_result" not in st.session_state:
    st.session_state["pipeline_result"] = None

# --- Find Subreddits ---
if st.sidebar.button("🔍 Find Subreddits"):
    try:
        st.session_state["channel_info"] = extract_channel_info(channel_url)
    except Exception as e:
        st.sidebar.error(f"Error analyzing channel: {e}")
        st.stop()

    try:
        subreddits = discover_subreddits(niche)
        st.session_state["discovered_subreddits"] = subreddits
        st.session_state["selected_subreddits"] = subreddits  # default: all selected
    except Exception as e:
        st.sidebar.error(f"Error discovering subreddits: {e}")
        st.stop()

# --- Subreddit Selection ---
if st.session_state["discovered_subreddits"]:
    st.sidebar.subheader("🗂 Select Subreddits")
    selected_subs = st.sidebar.multiselect(
        "Choose subreddits to analyze:",
        st.session_state["discovered_subreddits"],
        default=st.session_state["selected_subreddits"],
    )
    st.session_state["selected_subreddits"] = selected_subs

# --- Run Pipeline ---
run_pipeline_button = st.sidebar.button("🚀 Run Pipeline")

# --- Main Content ---
st.title("🔥 TrendForge: AI Growth Engine for YouTube Creators")

if run_pipeline_button:
    # Set state for running
    st.session_state["is_running_pipeline"] = True
    st.session_state["pipeline_result"] = None
    st.rerun()

# Display progress / analyzing / results
if st.session_state.get("is_running_pipeline", False):
    with st.spinner("Analyzing trends and generating content ideas..."):
        try:
            pipeline = Pipeline(
                niche=niche,
                selected_subreddits=st.session_state["selected_subreddits"],
                channel_description=st.session_state["channel_info"]["channel_description"]
            )
            result = pipeline.run()
            st.session_state["pipeline_result"] = result
            st.session_state["is_running_pipeline"] = False
            st.rerun()
        except Exception as e:
            st.error(f"Error running pipeline: {e}")
            st.session_state["is_running_pipeline"] = False

elif st.session_state.get("pipeline_result"):
    result = st.session_state["pipeline_result"]

    st.success("✅ Pipeline complete!")
    
    st.subheader("📊 Trend Summary")
    st.markdown(safe_extract_text(result, "trend_summary"))

    st.subheader("🎬 Content Plan")
    st.markdown(safe_extract_text(result, "content_plan"))

    st.subheader("🧠 Optimized Titles")
    st.markdown(safe_extract_text(result, "optimized_titles"))

    st.subheader("🎨 Thumbnail Ideas")
    st.markdown(safe_extract_text(result, "thumbnail_ideas"))

else:
    st.markdown(
        """
        ### How to use:
        1️⃣ Enter your niche and YouTube channel URL in the sidebar.  
        2️⃣ Click **Find Subreddits**.  
        3️⃣ Select which subreddits to analyze.  
        4️⃣ Click **Run Pipeline** to generate an AI-powered growth report 🚀.  
        """
    )
