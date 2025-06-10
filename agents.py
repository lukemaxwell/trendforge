# agents.py
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# --- Trend Summary Agent ---
trend_summary_prompt = ChatPromptTemplate.from_template("""
You are a YouTube trend analyst.

Given the following trends from Reddit, Google, and YouTube, write a concise executive summary of the key hot topics, emerging trends, and opportunities in this niche.

### Reddit Trends
{reddit_trends}

### Google Trends
{google_trends}

### YouTube Trends
{youtube_trends}

### Channel Description
{channel_description}

Instructions:
- Summarize clearly for a YouTube content creator
- Use plain English
- Highlight what is hot right now
- Highlight emerging trends
- Suggest what type of content creators should focus on
- Do NOT include generic phrases like "as an AI language model"
- Keep it short, easy to scan

Output format:
Trend Summary: <your summary here>
""")

TrendSummaryAgent = LLMChain(
    llm=llm,
    prompt=trend_summary_prompt,
    verbose=True
)

# --- Content Plan Agent ---
content_plan_prompt = ChatPromptTemplate.from_template("""
You are an expert YouTube content strategist.

Given the following Trend Summary and Channel Description, suggest 5 creative, specific video ideas for this channel that would likely perform well.

### Trend Summary
{trend_summary}

### Channel Description
{channel_description}

Instructions:
- Return 5 video ideas as bullet points
- Make them creative and aligned with the trends
- Target the interests of the audience implied by the trends and channel
- Do NOT return explanations — just the ideas

Output format:
- Idea 1
- Idea 2
- Idea 3
- Idea 4
- Idea 5
""")

ContentPlanAgent = LLMChain(
    llm=llm,
    prompt=content_plan_prompt,
    verbose=True
)

# --- Optimized Titles Agent ---
optimized_titles_prompt = ChatPromptTemplate.from_template("""
You are a YouTube title optimization expert.

Given the following Content Plan and Trend Summary, suggest 5 optimized, click-worthy YouTube video titles.

### Content Plan
{content_plan}

### Trend Summary
{trend_summary}

Instructions:
- Return 5 optimized titles
- Make them punchy and engaging
- Use good YouTube title conventions
- Do NOT add explanations

Output format:
- Title 1
- Title 2
- Title 3
- Title 4
- Title 5
""")

OptimizedTitlesAgent = LLMChain(
    llm=llm,
    prompt=optimized_titles_prompt,
    verbose=True
)

# --- Thumbnail Ideas Agent ---
thumbnail_ideas_prompt = ChatPromptTemplate.from_template("""
You are a YouTube thumbnail designer.

Given the following Content Plan and Trend Summary, suggest 5 thumbnail ideas for these videos.

### Content Plan
{content_plan}

### Trend Summary
{trend_summary}

Instructions:
For each idea:
1. Provide a short thumbnail text overlay suggestion
2. Describe any visual elements, colors, or effects to include

Format your output like this:

Thumbnail 1 Title
- Visual description

Thumbnail 2 Title
- Visual description

...

Do NOT add explanations or preambles — just give the list.

""")

ThumbnailIdeasAgent = LLMChain(
    llm=llm,
    prompt=thumbnail_ideas_prompt,
    verbose=True
)

# --- Pipeline ---
class Pipeline:
    def __init__(self, niche, selected_subreddits, channel_description):
        self.niche = niche
        self.selected_subreddits = selected_subreddits
        self.channel_description = channel_description

    def run(self, reddit_trends, google_trends, youtube_trends):
        # --- Trend Summary ---
        logger.info("🟢 Generating trend summary...")
        trend_summary_response = TrendSummaryAgent.run(
            reddit_trends=reddit_trends,
            google_trends=google_trends,
            youtube_trends=youtube_trends,
            channel_description=self.channel_description
        )
        logger.info("✅ Trend summary generated.")

        # --- Content Plan ---
        logger.info("🟢 Generating content plan...")
        content_plan_response = ContentPlanAgent.run(
            trend_summary=trend_summary_response,
            channel_description=self.channel_description
        )
        logger.info("✅ Content plan generated.")

        # --- Optimized Titles ---
        logger.info("🟢 Generating optimized titles...")
        optimized_titles_response = OptimizedTitlesAgent.run(
            content_plan=content_plan_response,
            trend_summary=trend_summary_response
        )
        logger.info("✅ Optimized titles generated.")

        # --- Thumbnail Ideas ---
        logger.info("🟢 Generating thumbnail ideas...")
        thumbnail_ideas_response = ThumbnailIdeasAgent.run(
            content_plan=content_plan_response,
            trend_summary=trend_summary_response
        )
        logger.info("✅ Thumbnail ideas generated.")

        # Return all results
        return {
            "trend_summary": trend_summary_response,
            "content_plan": content_plan_response,
            "optimized_titles": optimized_titles_response,
            "thumbnail_ideas": thumbnail_ideas_response
        }
