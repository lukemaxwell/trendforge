# agents.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import reddit_trend_search, google_trends_search, youtube_trend_search

# --- LLM config ---
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# --- TrendSummaryAgent ---

TrendSummaryPrompt = ChatPromptTemplate.from_template("""
You are an expert YouTube strategist.

Summarize the following trends into a concise report identifying hot topics and content opportunities.

Reddit Trends:
{reddit_trends}

Google Trends:
{google_trends}

YouTube Trends:
{youtube_trends}

Provide 3-5 key insights.
""")

TrendSummaryAgent = TrendSummaryPrompt | llm | StrOutputParser()

# --- PlannerAgent ---

PlannerPrompt = ChatPromptTemplate.from_template("""
You are an expert YouTube content strategist.

Given this trend summary and this YouTube channel description, generate 5 high-growth video content ideas.

Trend Summary:
{trend_summary}

Channel Description:
{channel_description}

For each idea, include:
- Title idea
- Short description
- Suggested format (Short, Long-form, Live, Series, etc.)
""")

PlannerAgent = PlannerPrompt | llm | StrOutputParser()

# --- TitleOptimizerAgent ---

TitleOptimizerPrompt = ChatPromptTemplate.from_template("""
You are an expert YouTube title optimizer.

Given this content plan, suggest 3 optimized click-worthy titles for each video idea.

Content Plan:
{content_plan}

Format the output clearly.
""")

TitleOptimizerAgent = TitleOptimizerPrompt | llm | StrOutputParser()

# --- ThumbnailIdeaAgent ---

ThumbnailIdeaPrompt = ChatPromptTemplate.from_template("""
You are an expert YouTube thumbnail designer.

Given this content plan, suggest 2 strong thumbnail concepts for each video idea.

Content Plan:
{content_plan}

Format the output clearly.
""")

ThumbnailIdeaAgent = ThumbnailIdeaPrompt | llm | StrOutputParser()

# --- Full Pipeline ---

def Pipeline(niche, selected_subreddits, channel_description):
    """Run the full agent pipeline"""
    print("==== DEBUG: Pipeline called ====")
    print(f"niche: {niche}")
    print(f"selected_subreddits: {selected_subreddits}")
    print(f"channel_description: {channel_description}")

    # Step 1: Reddit trends
    print("==== DEBUG: Running reddit_trend_search ====")
    reddit_trends = reddit_trend_search(selected_subreddits)
    print("==== DEBUG: Reddit trends done ====")

    # Step 2: Google trends
    print("==== DEBUG: Running google_trends_search ====")
    google_trends = google_trends_search(niche)
    print("==== DEBUG: Google trends done ====")

    # Step 3: YouTube trends
    print("==== DEBUG: Running youtube_trend_search ====")
    youtube_trends = youtube_trend_search(niche)
    print("==== DEBUG: YouTube trends done ====")

    # Step 4: Summarize trends
    print("==== DEBUG: Running TrendSummaryAgent ====")
    trend_summary = TrendSummaryAgent.invoke({
        "reddit_trends": reddit_trends,
        "google_trends": google_trends,
        "youtube_trends": youtube_trends
    })
    print("==== DEBUG: Trend summary done ====")

    # Step 5: Content plan
    print("==== DEBUG: Running PlannerAgent ====")
    content_plan = PlannerAgent.invoke({
        "trend_summary": trend_summary,
        "channel_description": channel_description
    })
    print("==== DEBUG: Content plan done ====")

    # Step 6: Title optimization
    print("==== DEBUG: Running TitleOptimizerAgent ====")
    optimized_titles = TitleOptimizerAgent.invoke({
        "content_plan": content_plan
    })
    print("==== DEBUG: Optimized titles done ====")

    # Step 7: Thumbnail ideas
    print("==== DEBUG: Running ThumbnailIdeaAgent ====")
    thumbnail_ideas = ThumbnailIdeaAgent.invoke({
        "content_plan": content_plan
    })
    print("==== DEBUG: Thumbnail ideas done ====")

    print("==== DEBUG: Pipeline completed ====")

    return {
        "reddit_trends": reddit_trends,
        "google_trends": google_trends,
        "youtube_trends": youtube_trends,
        "trend_summary": trend_summary,
        "content_plan": content_plan,
        "optimized_titles": optimized_titles,
        "thumbnail_ideas": thumbnail_ideas
    }
