# agents.py

import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LLM instance
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# --- Helper: Safe list extraction ---
def safe_extract_list(text):
    if not text:
        return []
    if isinstance(text, list):
        return text
    # Split by line or numbered bullets
    lines = text.split("\n")
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith("- "):
            clean_lines.append(line[2:].strip())
        elif line and not line.startswith("#") and not line.startswith(">"):
            clean_lines.append(line)
    return [line for line in clean_lines if line]

# --- Trend Summary Agent ---
def TrendSummaryAgent(reddit_trends, google_trends, youtube_trends, channel_description):
    logger.info("Running TrendSummaryAgent...")

    prompt = ChatPromptTemplate.from_template(
        """
You are an expert market analyst for YouTube creators.

You will be given trends from Reddit, Google, and YouTube for a specific niche. You will also be given the channel description.

Your task is to analyze all trends and generate a concise, readable **Trend Summary**.

**Output should be 5-7 bullet points. DO NOT output a long paragraph.**

---

Reddit Trends:
{reddit_trends}

Google Trends:
{google_trends}

YouTube Trends:
{youtube_trends}

Channel Description:
{channel_description}

---

Now write the Trend Summary:
"""
    )

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({
        "reddit_trends": reddit_trends,
        "google_trends": google_trends,
        "youtube_trends": youtube_trends,
        "channel_description": channel_description
    })

    return result

# --- Content Plan Agent ---
def ContentPlanAgent(trend_summary, channel_description):
    logger.info("Running ContentPlanAgent...")

    prompt = ChatPromptTemplate.from_template(
        """
You are an expert YouTube strategist.

Given the following Trend Summary and Channel Description, suggest an engaging Content Plan paragraph that describes what kinds of videos this creator should make next.

Trend Summary:
{trend_summary}

Channel Description:
{channel_description}

---

Now write the Content Plan paragraph:
"""
    )

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({
        "trend_summary": trend_summary,
        "channel_description": channel_description
    })

    return result

# --- Optimized Titles Agent ---
def OptimizedTitlesAgent(trend_summary, content_plan):
    logger.info("Running OptimizedTitlesAgent...")

    prompt = ChatPromptTemplate.from_template(
        """
You are an expert YouTube title copywriter.

Given the following Trend Summary and Content Plan, write **5 highly clickable YouTube video titles** for this creator.

Trend Summary:
{trend_summary}

Content Plan:
{content_plan}

---

Output the 5 titles as a simple list:
- Title 1
- Title 2
- Title 3
- Title 4
- Title 5
"""
    )

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({
        "trend_summary": trend_summary,
        "content_plan": content_plan
    })

    return safe_extract_list(result)

# --- Thumbnail Ideas Agent ---
def ThumbnailIdeasAgent(trend_summary, content_plan):
    logger.info("Running ThumbnailIdeasAgent...")

    prompt = ChatPromptTemplate.from_template(
        """
You are a top YouTube thumbnail designer.

Given the following Trend Summary and Content Plan, write **5 thumbnail ideas** for this creator's next videos.

For each thumbnail idea, provide just a short descriptive sentence.

Trend Summary:
{trend_summary}

Content Plan:
{content_plan}

---

Output the 5 thumbnail ideas as a simple list:
- Thumbnail idea 1
- Thumbnail idea 2
- Thumbnail idea 3
- Thumbnail idea 4
- Thumbnail idea 5
"""
    )

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({
        "trend_summary": trend_summary,
        "content_plan": content_plan
    })

    return safe_extract_list(result)

# --- Full Pipeline class ---
class Pipeline:
    def __init__(self, niche, selected_subreddits, channel_description):
        self.niche = niche
        self.selected_subreddits = selected_subreddits
        self.channel_description = channel_description

    def run(self, reddit_trends, google_trends, youtube_trends):
        logger.info("Starting full pipeline...")

        trend_summary = TrendSummaryAgent(
            reddit_trends, google_trends, youtube_trends, self.channel_description
        )
        logger.info("✅ TrendSummaryAgent complete")

        content_plan = ContentPlanAgent(trend_summary, self.channel_description)
        logger.info("✅ ContentPlanAgent complete")

        optimized_titles = OptimizedTitlesAgent(trend_summary, content_plan)
        logger.info("✅ OptimizedTitlesAgent complete")

        thumbnail_ideas = ThumbnailIdeasAgent(trend_summary, content_plan)
        logger.info("✅ ThumbnailIdeasAgent complete")

        return {
            "trend_summary": trend_summary,
            "content_plan": content_plan,
            "optimized_titles": optimized_titles,
            "thumbnail_ideas": thumbnail_ideas,
        }
