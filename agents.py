from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from tools import (
    reddit_trend_search,
    google_trends_search,
    youtube_trend_search,
    channel_analysis_tool,
)

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# TrendSummaryAgent
trend_summary_prompt = PromptTemplate.from_template("""
Given the following trends from Reddit, Google, and YouTube, and the titles of recent YouTube videos, generate a summary of hot topics in this niche.

Reddit Trends:
{reddit_trends}

Google Trends:
{google_trends}

YouTube Trends:
{youtube_trends}

Recent Video Titles:
{recent_video_titles}

Summary of Hot Topics:
""")

TrendSummaryAgent = LLMChain(llm=llm, prompt=trend_summary_prompt)

# PlannerAgent
planner_prompt = PromptTemplate.from_template("""
You are a YouTube content strategist.

Channel Description:
{channel_description}

Hot Topics:
{trend_summary}

Generate 5 high-growth YouTube video ideas:
""")

PlannerAgent = LLMChain(llm=llm, prompt=planner_prompt)

# TitleOptimizerAgent
title_optimizer_prompt = PromptTemplate.from_template("""
Optimize the following video titles for maximum YouTube engagement:

{video_ideas}

Optimized Titles:
""")

TitleOptimizerAgent = LLMChain(llm=llm, prompt=title_optimizer_prompt)

# ThumbnailIdeaAgent
thumbnail_idea_prompt = PromptTemplate.from_template("""
For each of the following video titles, suggest a compelling YouTube thumbnail idea:

{optimized_titles}

Thumbnail Ideas:
""")

ThumbnailIdeaAgent = LLMChain(llm=llm, prompt=thumbnail_idea_prompt)

# Full Pipeline wrapper
class Pipeline:
    @staticmethod
    def run(niche, subreddits, channel_description, recent_video_titles):
        # Trends
        reddit_trends = reddit_trend_search(subreddits)
        google_trends = google_trends_search(niche)
        youtube_trends = youtube_trend_search(niche)

        # Trend summary
        trend_summary = TrendSummaryAgent.run({
            "reddit_trends": reddit_trends,
            "google_trends": google_trends,
            "youtube_trends": youtube_trends,
            "recent_video_titles": "\n".join(recent_video_titles)
        })

        # Channel analysis
        channel_analysis = channel_analysis_tool(channel_description)

        # Content plan
        content_plan = PlannerAgent.run({
            "channel_description": channel_description,
            "trend_summary": trend_summary
        })

        # Optimized titles
        optimized_titles = TitleOptimizerAgent.run({"video_ideas": content_plan})

        # Thumbnail ideas
        thumbnail_ideas = ThumbnailIdeaAgent.run({"optimized_titles": optimized_titles})

        return {
            "channel_analysis": channel_analysis,
            "trend_summary": trend_summary,
            "content_plan": content_plan,
            "optimized_titles": optimized_titles,
            "thumbnail_ideas": thumbnail_ideas,
        }
