# main.py

import streamlit as st
from agents import Pipeline
from tools import discover_subreddits, extract_channel_info

# --- Page config ---
st.set_page_config(page_title="TrendForge", page_icon="🔥", layout="wide")

# --- Header ---
st.title("🔥 TrendForge: Your AI Growth Companion for YouTube 🚀")
st.markdown(
    """
**TrendForge** helps YouTube creators grow their channels using the power of **AI** and **trend analysis**.

✨ Analyze your channel  
📈 Discover hot trends across **Reddit**, **Google**, and **YouTube**  
🧠 Generate **engaging content ideas**  
🎨 Suggest **optimized titles** & **thumbnail concepts**  
🛠 All powered by a multi-agent AI pipeline.

---

### How to use:

1️⃣ Enter your **YouTube Channel URL** → *We'll analyze your current content & audience*  
2️⃣ Enter your **niche / topic** → *We'll find trending communities & topics for you*  
3️⃣ Select which **Reddit communities** you want to focus on  
4️⃣ Click **Run Pipeline** → *Sit back while TrendForge creates your next content strategy!*  
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

# --- Sidebar ---
with st.sidebar:
    st.header("🔗 Input Your Channel & Niche")
    channel_url_input = st.text_input("YouTube Channel URL", value=st.session_state["channel_url"])
    niche_input = st.text_input("Channel Niche / Topic (e.g. Warhammer, Tiny Painting, Yoga...)")

    # --- Analyze button ---
    if st.button("📥 Analyze Channel"):
        st.session_state["channel_url"] = channel_url_input
        with st.spinner("Extracting channel info..."):
            channel_info = extract_channel_info(st.session_state["channel_url"])
        st.session_state["channel_description"] = channel_info
        st.session_state["channel_ready"] = True
        st.rerun()

# --- Channel Analysis ---
st.subheader("📺 Channel Analysis")

if st.session_state["channel_ready"]:
    st.info(st.session_state["channel_description"])
else:
    st.info("Please enter your YouTube Channel URL and click 'Analyze Channel'.")

# --- Subreddit Discovery ---
if st.session_state["channel_ready"]:
    st.subheader("🗂 Discover Subreddits")

    if st.button("🔍 Discover Subreddits"):
        with st.spinner("Discovering subreddits..."):
            subreddits = discover_subreddits(niche_input)
        st.session_state["subreddits"] = subreddits
        st.session_state["selected_subreddits"] = subreddits  # select all by default
        st.rerun()

    # Display subreddit multiselect if subreddits were discovered
    if st.session_state["subreddits"]:
        selected = st.multiselect(
            "Select subreddits to use for trend analysis:",
            options=st.session_state["subreddits"],
            default=st.session_state.get("selected_subreddits", st.session_state["subreddits"])
        )
        st.session_state["selected_subreddits"] = selected
    else:
        st.info("No subreddits found — try a broader niche or add manually.")

# --- Run pipeline ---
if st.session_state["channel_ready"] and st.session_state["selected_subreddits"]:
    st.subheader("🚀 Run AI Pipeline")

    if st.button("Run Pipeline"):
        with st.spinner("Running TrendForge pipeline..."):
            try:
                pipeline = Pipeline(
                    niche=niche_input,
                    selected_subreddits=st.session_state["selected_subreddits"],
                    channel_description=st.session_state["channel_description"]
                )
                result = pipeline.run()
                st.success("✅ Pipeline complete!")
                st.markdown("### 📄 Results:")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error running pipeline: {e}")

# --- New Search ---
st.divider()
if st.button("🔄 New Search", key="new_search_btn"):
    st.session_state["channel_url"] = ""
    st.session_state["channel_description"] = ""
    st.session_state["channel_ready"] = False
    st.session_state["subreddits"] = []
    st.session_state["selected_subreddits"] = []
    st.rerun()
