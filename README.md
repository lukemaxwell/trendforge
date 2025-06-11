# 🔥 TrendSleuth

Your AI Growth Companion 🚀

TrendSleuth helps YouTube creators grow their channels using the power of AI and trend analysis.

✨ Analyze your channel  
📈 Discover hot trends across **Reddit**, **Google**, and **YouTube**  
🧠 Generate **engaging content ideas**  
🎨 Suggest **optimized titles** & **thumbnail concepts**  
🛠 All powered by a multi-agent AI pipeline (LangChain + LLM + Streamlit).

---

## How to use:

1️⃣ Enter your **YouTube Channel URL**  
2️⃣ Enter your **niche / topic**  
3️⃣ Select which **Reddit communities** you want to focus on  
4️⃣ Click **Run Pipeline** → *TrendForge generates your content strategy!*  

---

## Architecture:

- Frontend: **Streamlit**  
- Agents: **LangChain Functions Agents**  
- Data sources:  
  - **YouTube API**  
  - **Reddit API**  
  - **Google Trends** (via pytrends)  
- LLM: **OpenAI GPT-4o**  

---

## Build images
```bash
# For Streamlit:
gcloud builds submit --tag gcr.io/youtubeaccelerator/trendsleuth-streamlit ./app/streamlit-app

# For FastAPI Webhook:
gcloud builds submit --tag gcr.io/youtubeaccelerator/trendsleuth-stripe-webhook ./app/stripe-webhook
```

## Run locally:

```bash
git clone https://github.com/lukemaxwell/trendforge.git
cd trendforge
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Add secrets to .streamlit/secrets.toml:

[default]
OPENAI_API_KEY = "sk-..."
REDDIT_CLIENT_ID = "..."
REDDIT_CLIENT_SECRET = "..."
YOUTUBE_API_KEY = "..."

# Run
streamlit run main.py
