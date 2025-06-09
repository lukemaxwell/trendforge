# TrendForge 🚀

**AI-Powered YouTube Growth Pipeline**

Turn trends into growth — with AI-powered content strategy for YouTube creators.

---

## What is TrendForge?

TrendForge helps YouTube creators discover hot trends and generate optimized content plans.

It combines:

✅ Your YouTube channel description + video history  
✅ Google Trends data  
✅ Reddit trends (you select the relevant subreddits)  
✅ YouTube trending ideas  

And produces:

🎯 **Summary of hot topics**  
🎬 **High-growth YouTube video ideas**  
📝 **Optimized video titles**  
🖼️ **Engaging thumbnail ideas**

---

## Demo

👉 Coming soon! (Deploy on Streamlit Cloud → instant URL 🚀)

---

## How it works

1️⃣ Enter your niche (example: "miniature painting")  
2️⃣ Provide your YouTube channel URL  
3️⃣ Select subreddits you want to monitor  
4️⃣ Click "Run Pipeline"  

TrendForge will:

- Extract your channel info
- Analyze trends from multiple sources
- Generate a full content plan

---

## Architecture

```plaintext
            +----------------------+
            |  YouTube Channel URL |
            +----------------------+
                       |
            +--------------------------+
            |  Extract Channel Info    |
            +--------------------------+
                       |
                       v
 +--------+    +--------+    +--------+
 | Reddit | -> | Google | -> | YouTube|
 | Trends |    | Trends |    | Trends |
 +--------+    +--------+    +--------+
                       |
            +--------------------------+
            |  Trend Summary Agent     |
            +--------------------------+
                       |
            +--------------------------+
            |  Channel Analysis Agent  |
            +--------------------------+
                       |
            +--------------------------+
            |  Content Planner Agent   |
            +--------------------------+
                       |
        +-------------+-------------+
        |                           |
+-------------------+    +----------------------+
| Title Optimizer   |    | Thumbnail Idea Agent |
+-------------------+    +----------------------+
