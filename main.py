import streamlit as st
from tools import discover_subreddits, extract_channel_info
from agents import Pipeline

# Session state init
if "selected_subreddits" not in st.session_state:
    st.session_state.selected_subreddits = []
if "search_completed" not in st.session_state:
    st.session_state.search_completed = False

# App title
st.title("📈 YouTube Growth Pipeline")

# Inputs
niche = st.text_input("Enter your niche:", "")
channel_url = st.text_input("Enter YouTube Channel URL (optional):", "")

# Discover subreddits
if niche and not st.session_state.selected_subreddits:
    st.write("🔍 Discovering subreddits...")
    discovered_subreddits = discover_subreddits(niche)

    if discovered_subreddits:
        st.write("✅ Select relevant subreddits:")
        selected = st.multiselect("Subreddits:", discovered_subreddits, default=discovered_subreddits[:5])
        st.session_state.selected_subreddits = selected
    else:
        st.warning("No subreddits found — try a broader niche or add manually.")
        manual_subreddits = st.text_input("Manually enter subreddits (comma-separated):")
        if manual_subreddits:
            st.session_state.selected_subreddits = [s.strip() for s in manual_subreddits.split(",")]

# Run pipeline
if st.session_state.selected_subreddits and niche:
    if st.button("🚀 Run Pipeline"):
        # Extract channel info if URL provided
        if channel_url:
            st.write("🎬 Extracting channel info...")
            channel_info = extract_channel_info(channel_url)
            channel_description = channel_info["channel_description"]
            recent_videos = channel_info["recent_videos"]

            st.write("📺 Channel Description:")
            st.write(channel_description)

            st.write("🎥 Recent Videos:")
            for vid in recent_videos:
                st.write(f"- {vid['title']} (Views: {vid.get('view_count', 'N/A')})")
        else:
            channel_description = ""
            recent_videos = []

        # Run the full pipeline
        st.write("🧠 Running pipeline...")
        outputs = Pipeline.run(
            niche=niche,
            subreddits=st.session_state.selected_subreddits,
            channel_description=channel_description,
            recent_video_titles=[v["title"] for v in recent_videos]
        )

        # Display results
        st.header("📺 Channel Analysis")
        st.write(outputs["channel_analysis"])

        st.header("🔥 Trend Summary")
        st.write(outputs["trend_summary"])

        st.header("🎬 Content Plan")
        st.write(outputs["content_plan"])

        st.header("📝 Optimized Titles")
        st.write(outputs["optimized_titles"])

        st.header("🖼️ Thumbnail Ideas")
        st.write(outputs["thumbnail_ideas"])

        st.session_state.search_completed = True

# Reset button
def reset_search():
    st.session_state.selected_subreddits = []
    st.session_state.search_completed = False

st.sidebar.button("🔄 New Search", key="new_search_sidebar", on_click=reset_search)
