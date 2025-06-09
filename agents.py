# agents.py

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# --- LLM config ---
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# --- Prompt templates ---

# 1️⃣ Trend Summary
trend_summary_prompt = PromptTemplate.from_template(
    """
You are a YouTube trend analyst.

Based on the following Reddit trends, Google Trends, and YouTube trends, provide a concise summary of:
- What topics are hot in this niche
- What emerging trends you notice
- What the target audience seems interested in right now

Reddit Trends:
{reddit_trends}

Google Trends:
{google_trends}

YouTube Trends:
{youtube_trends}

Your summary:
"""
)

TrendSummaryAgent = LLMChain(llm=llm, prompt=trend_summary_prompt)

# 2️⃣ Content Planning
content_ideas_prompt = PromptTemplate.from_template(
    """
You are a YouTube content strategist.

Based on this Trend Summary and this YouTube Channel description, suggest 5 engaging YouTube video ideas that will likely drive growth and engagement:

Trend Summary:
{trend_summary}

Channel Description:
{channel_description}

Video Ideas:
"""
)

ContentPlanningAgent = LLMChain(llm=llm, prompt=content_ideas_prompt)

# 3️⃣ Title Optimizer
title_optimizer_prompt = PromptTemplate.from_template(
    """
You are an expert YouTube title copywriter.

Given these content ideas, suggest 2 optimized titles for each idea, designed to maximize clicks and engagement.

Content Ideas:
{content_ideas}

Optimized Titles:
"""
)

TitleOptimizerAgent = LLMChain(llm=llm, prompt=title_optimizer_prompt)

# 4️⃣ Thumbnail Ideas
thumbnail_ideas_prompt = PromptTemplate.from_template(
    """
You are an expert YouTube thumbnail designer.

Given these content ideas and titles, suggest a compelling thumbnail concept for each video idea — keep it visual, minimal text, highly eye-catching.

Content Ideas:
{content_ideas}

Optimized Titles:
{optimized_titles}

Thumbnail Ideas:
"""
)

ThumbnailIdeaAgent = LLMChain(llm=llm, prompt=thumbnail_ideas_prompt)

# --- Pipeline class ---
class Pipeline:
    def __init__(self, niche, selected_subreddits, channel_description):
        self.niche = niche
        self.selected_subreddits = selected_subreddits
        self.channel_description = channel_description

    def run(self):
        # For now, we simulate the trend data (your tools.py can populate these)
        reddit_trends = f"Trending topics in {', '.join(self.selected_subreddits)}..."
        google_trends = f"Top Google Trends for niche {self.niche}..."
        youtube_trends = f"Trending YouTube topics for niche {self.niche}..."

        # 1️⃣ Trend Summary
        trend_summary = TrendSummaryAgent.invoke({
            "reddit_trends": reddit_trends,
            "google_trends": google_trends,
            "youtube_trends": youtube_trends
        })

        # 2️⃣ Content Ideas
        content_ideas = ContentPlanningAgent.invoke({
            "trend_summary": trend_summary,
            "channel_description": self.channel_description
        })

        # 3️⃣ Optimized Titles
        optimized_titles = TitleOptimizerAgent.invoke({
            "content_ideas": content_ideas
        })

        # 4️⃣ Thumbnail Ideas
        thumbnail_ideas = ThumbnailIdeaAgent.invoke({
            "content_ideas": content_ideas,
            "optimized_titles": optimized_titles
        })

        return {
            "Trend Summary": trend_summary,
            "Content Ideas": content_ideas,
            "Optimized Titles": optimized_titles,
            "Thumbnail Ideas": thumbnail_ideas
        }
