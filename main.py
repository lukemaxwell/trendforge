# main.py

import streamlit as st
from agents import Pipeline
from tools import discover_subreddits, extract_channel_info

# --- Page config ---
st.set_page_config(page_title="TrendForge", page_icon="🔥", layout="wide")

# --- Page Header ---
st.title("🔥 TrendForge: Your AI Growth Companion for YouTube 🚀")
st.markdown(
    """
**TrendForge** helps YouTube creators grow their channels using **AI** and **trend analysis**.

✨ Analyze your channel  
📈 Discover hot trends across **Reddit**, **Google**, and **YouTube**  
🧠 Generate **engaging content ideas**  
🎨 Suggest **optimized titles** & **thumbnail concepts**  
🛠 All powered by a multi-agent AI pipeline.

---

### How to use:

**Step 1️⃣** Enter your YouTube Channel URL and Niche  
**Step 2️⃣** Discover Subreddits  
**Step 3️⃣** Run AI Pipeline  
"""
)

# --- Session state init ---
if "channel_url" not in st.session_state:
    st.session_state["channel_url"] = ""
if "channel_description" not in st.session_state:
    st.session_state["channel_description"] = ""
if "channel_ready" not in st.session_state:
    st.session_state["channel_ready"] = False
if "subreddits" not in st.session_state:
    st.session_state["subreddits"] = []
if "selected_subreddits" not in st.session_state:
    st.session_state["selected_subreddits"] = []
if "result" not in st.session_state:
    st.session_state["result"] = None
if "pipeline_running" not in st.session_state:
    st.session_state["pipeline_running"] = False
if "trigger_pipeline" not in st.session_state:
    st.session_state["trigger_pipeline"] = False

# --- Sidebar: Step Flow ---
with st.sidebar:
    st.header("⚙️ TrendForge Setup")

    # --- Step 1 ---
    st.subheader("Step 1️⃣ Channel & Niche")
    channel_url_input = st.text_input("YouTube Channel URL", value=st.session_state["channel_url"])
    niche_input = st.text_input("Channel Niche / Topic (e.g. Warhammer, Tiny Painting, Yoga...)")

    if st.button("📥 Analyze Channel"):
        st.session_state["channel_url"] = channel_url_input
        with st.spinner("Extracting channel info..."):
            channel_info = extract_channel_info(st.session_state["channel_url"])
        st.session_state["channel_description"] = channel_info
        st.session_state["channel_ready"] = True
        st.session_state["result"] = None
        st.session_state["subreddits"] = []
        st.session_state["selected_subreddits"] = []
        st.session_state["pipeline_running"] = False
        st.session_state["trigger_pipeline"] = False
        st.rerun()

    # --- Step 2 ---
    if st.session_state["channel_ready"]:
        st.subheader("Step 2️⃣ Discover Subreddits")
        if st.button("🔍 Discover Subreddits"):
            with st.spinner("Discovering subreddits..."):
                subreddits = discover_subreddits(niche_input)
            st.session_state["subreddits"] = subreddits
            st.session_state["selected_subreddits"] = subreddits  # select all by default
            st.session_state["result"] = None
            st.session_state["pipeline_running"] = False
            st.session_state["trigger_pipeline"] = False
            st.rerun()

        if st.session_state["subreddits"]:
            selected = st.multiselect(
                "Select subreddits to use for trend analysis:",
                options=st.session_state["subreddits"],
                default=st.session_state.get("selected_subreddits", st.session_state["subreddits"]),
                key="selected_subreddits_widget"
            )
            st.session_state["selected_subreddits"] = selected
        else:
            st.info("No subreddits found — try a broader niche or add manually.")

    # --- Step 3 ---
    if st.session_state["channel_ready"] and st.session_state["selected_subreddits"]:
        st.subheader("Step 3️⃣ Run AI Pipeline")
        if st.button("🚀 Run Pipeline"):
            st.session_state["pipeline_running"] = True
            st.session_state["trigger_pipeline"] = True  # flag to trigger actual run below
            st.session_state["result"] = None
            st.rerun()

    # --- New Search ---
    st.divider()
    if st.button("🔄 New Search", key="new_search_btn"):
        st.session_state["channel_url"] = ""
        st.session_state["channel_description"] = ""
        st.session_state["channel_ready"] = False
        st.session_state["subreddits"] = []
        st.session_state["selected_subreddits"] = []
        st.session_state["result"] = None
        st.session_state["pipeline_running"] = False
        st.session_state["trigger_pipeline"] = False
        st.rerun()

# --- Main Pane Progress Flow ---
if not st.session_state["channel_ready"]:
    st.info("👉 Please start with **Step 1** in the sidebar to Analyze Channel.")

elif st.session_state["pipeline_running"]:
    st.info("🚀 Running TrendForge pipeline... please wait...")

elif st.session_state["channel_ready"] and not st.session_state["subreddits"]:
    st.info("✅ Channel analyzed! Now proceed to **Step 2** in sidebar: Discover Subreddits.")

elif st.session_state["channel_ready"] and st.session_state["selected_subreddits"] and not st.session_state["result"]:
    st.info("✅ Subreddits selected! Now proceed to **Step 3** in sidebar: Run Pipeline.")

# --- Run pipeline logic ---
if st.session_state["trigger_pipeline"]:
    # Actually run the pipeline
    try:
        pipeline = Pipeline(
            niche=niche_input,
            selected_subreddits=st.session_state["selected_subreddits"],
            channel_description=st.session_state["channel_description"]
        )
        result = pipeline.run()
        st.session_state["result"] = result
        st.session_state["pipeline_running"] = False
        st.session_state["trigger_pipeline"] = False
        st.success("✅ Pipeline complete!")
    except Exception as e:
        st.error(f"Error running pipeline: {e}")
        st.session_state["pipeline_running"] = False
        st.session_state["trigger_pipeline"] = False

# --- Display Results ---
if st.session_state["result"]:
    result = st.session_state["result"]

    def safe_extract_text(section) -> str:
        if isinstance(section, dict):
            return section.get("text", "No data.")
        if isinstance(section, str):
            return section
        return "No data."

    trend_summary_text = safe_extract_text(result.get("Trend Summary"))
    content_ideas_text = safe_extract_text(result.get("Content Ideas"))
    optimized_titles_text = safe_extract_text(result.get("Optimized Titles"))
    thumbnail_ideas_text = safe_extract_text(result.get("Thumbnail Ideas"))

    st.subheader("📺 Channel Analysis")
    st.info(st.session_state["channel_description"])

    st.subheader("📊 Trend Summary")
    st.markdown(trend_summary_text, unsafe_allow_html=True)

    st.subheader("💡 Content Ideas")
    st.markdown(content_ideas_text, unsafe_allow_html=True)

    st.subheader("🧠 Optimized Titles")
    st.markdown(optimized_titles_text, unsafe_allow_html=True)

    st.subheader("🖼️ Thumbnail Ideas")
    st.markdown(thumbnail_ideas_text, unsafe_allow_html=True)
