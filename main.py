import streamlit as st
from agents import Pipeline
from tools import discover_subreddits, extract_channel_info

# Improved safe_extract_text
def safe_extract_text(value):
    if isinstance(value, dict) and "text" in value:
        return value["text"]
    elif isinstance(value, list):
        return "\n".join(str(item) for item in value)
    elif isinstance(value, str):
        return value
    else:
        return ""

# Initialize session state
if "step_status" not in st.session_state:
    st.session_state["step_status"] = {
        "step1": "pending",
        "step2": "pending",
        "step3": "pending"
    }
if "selected_subreddits" not in st.session_state:
    st.session_state["selected_subreddits"] = []
if "result" not in st.session_state:
    st.session_state["result"] = None
if "pipeline_running" not in st.session_state:
    st.session_state["pipeline_running"] = False
if "channel_description" not in st.session_state:
    st.session_state["channel_description"] = ""
if "discovered_subreddits" not in st.session_state:
    st.session_state["discovered_subreddits"] = []

# App title and description
st.set_page_config(page_title="TrendForge", page_icon="🔥")
st.sidebar.title("🔥 TrendForge")
st.sidebar.markdown("""
Grow your YouTube channel with AI-powered content ideas.

**How it works:**  
1️⃣ Analyze your niche and channel  
2️⃣ Discover hot trends on Reddit, Google, YouTube  
3️⃣ Generate content ideas, optimized titles, thumbnail ideas  
""")

# Sidebar inputs
niche_input = st.sidebar.text_input("Enter your niche", "")
channel_url = st.sidebar.text_input("YouTube channel URL (optional)", "")

# Step indicators
st.sidebar.markdown("### Progress")
for step, status in st.session_state["step_status"].items():
    icon = "✅" if status == "complete" else "⏳" if status == "running" else "⚪️"
    st.sidebar.write(f"{icon} {step.capitalize()}")

# Buttons in sidebar
if st.sidebar.button("🔍 Find Subreddits"):
    st.session_state["discovered_subreddits"] = discover_subreddits(niche_input)
    st.session_state["step_status"]["step1"] = "complete"

if st.sidebar.button("📺 Analyze Channel"):
    try:
        st.session_state["channel_description"] = extract_channel_info(channel_url)
        st.session_state["step_status"]["step2"] = "complete"
    except Exception as e:
        st.error(f"Error analyzing channel: {e}")

# Subreddit selection
if st.session_state["discovered_subreddits"]:
    selected = st.sidebar.multiselect(
        "Select subreddits for trend mining:",
        st.session_state["discovered_subreddits"],
        default=st.session_state["selected_subreddits"],
        key="selected_subreddits_widget"
    )
    st.session_state["selected_subreddits"] = selected

# Main content area
st.title("🔥 TrendForge: AI Growth Engine for YouTube Creators")

# Main flow
if st.session_state["step_status"]["step3"] == "complete" and st.session_state["result"]:
    st.success("✅ Pipeline complete!")
    st.write("### 📊 Trend Summary")
    st.markdown(safe_extract_text(st.session_state["result"].get("trend_summary")))
    st.write("### 🎬 Content Plan")
    st.markdown(safe_extract_text(st.session_state["result"].get("content_ideas")))
    st.write("### 🧠 Optimized Titles")
    st.markdown(safe_extract_text(st.session_state["result"].get("optimized_titles")))
    st.write("### 🎨 Thumbnail Ideas")
    st.markdown(safe_extract_text(st.session_state["result"].get("thumbnail_ideas")))

elif st.session_state["pipeline_running"]:
    # Show analyzing message while pipeline is running
    st.info("🚀 Analyzing trends... please wait...")
    with st.spinner("Running TrendForge pipeline..."):
        try:
            pipeline = Pipeline(
                niche=niche_input,
                selected_subreddits=st.session_state["selected_subreddits"],
                channel_description=st.session_state["channel_description"]
            )
            result = pipeline.run()
            st.session_state["result"] = result
            st.session_state["pipeline_running"] = False
            st.session_state["step_status"]["step3"] = "complete"
            st.rerun()
        except Exception as e:
            st.error(f"Error running pipeline: {e}")
            st.session_state["pipeline_running"] = False
            st.session_state["step_status"]["step3"] = "pending"

elif st.session_state["step_status"]["step2"] == "complete":
    # Ready to run pipeline
    st.write("### Step 3: Run TrendForge Pipeline")
    st.write("Click below to generate your AI-powered content plan:")
    if st.button("🚀 Run Pipeline"):
        st.session_state["pipeline_running"] = True
        st.session_state["step_status"]["step3"] = "running"
        st.session_state["result"] = None
        st.rerun()

else:
    # Initial instructions
    st.write("### Welcome to TrendForge!")
    st.markdown("""
**Steps:**  
1️⃣ Enter your niche and click *Find Subreddits*  
2️⃣ (Optional) Enter your YouTube channel URL and click *Analyze Channel*  
3️⃣ Select subreddits and click *Run Pipeline* to generate your AI-powered content plan 🚀  
""")
