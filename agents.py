from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# Trend Summary Chain
trend_summary_prompt = PromptTemplate.from_template("""
You are an expert YouTube content strategist.

Here are the current trends:

Reddit Trends:
{reddit_trends}

Google Trends:
{google_trends}

YouTube Trends:
{youtube_trends}

Channel Description:
{channel_description}

Generate a concise summary of the hot topics and emerging trends in this niche that are suitable for YouTube content. Focus on what viewers are currently interested in.

Respond in this format:

Trend Summary:
[Your text here]
""")

trend_summary_chain = LLMChain(llm=llm, prompt=trend_summary_prompt)

# Content Ideas Chain
content_ideas_prompt = PromptTemplate.from_template("""
You are an expert YouTube content strategist.

Based on this trend summary:

{trend_summary}

Generate 5 YouTube content ideas that would perform well. Each idea should be a short title or concept.

Respond in this format:

Content Ideas:
1. Idea 1
2. Idea 2
3. Idea 3
4. Idea 4
5. Idea 5
""")

content_ideas_chain = LLMChain(llm=llm, prompt=content_ideas_prompt)

# Optimized Titles Chain
optimized_titles_prompt = PromptTemplate.from_template("""
You are an expert YouTube content strategist.

Here are 5 content ideas:

{content_ideas}

For each idea, write an optimized YouTube video title that is highly clickable and engaging.

Respond in this format:

Optimized Titles:
1. Title 1
2. Title 2
3. Title 3
4. Title 4
5. Title 5
""")

optimized_titles_chain = LLMChain(llm=llm, prompt=optimized_titles_prompt)

# Thumbnail Ideas Chain
thumbnail_ideas_prompt = PromptTemplate.from_template("""
You are an expert YouTube content strategist.

Here are 5 content ideas:

{content_ideas}

For each idea, suggest a creative thumbnail concept that will attract clicks.

Respond in this format:

Thumbnail Ideas:
1. Idea 1
2. Idea 2
3. Idea 3
4. Idea 4
5. Idea 5
""")

thumbnail_ideas_chain = LLMChain(llm=llm, prompt=thumbnail_ideas_prompt)

# Pipeline Class
class Pipeline:
    def __init__(self, niche, selected_subreddits, channel_description):
        self.niche = niche
        self.selected_subreddits = selected_subreddits
        self.channel_description = channel_description

    def run(self):
        print(f"--- Running Pipeline ---")
        print(f"Niche: {self.niche}")
        print(f"Selected subreddits: {self.selected_subreddits}")
        print(f"Channel description: {self.channel_description}")

        # Step 1: Trend Summary
        trend_summary_result = trend_summary_chain.run(
            reddit_trends=", ".join(self.selected_subreddits),
            google_trends=f"Top Google Trends for niche {self.niche}...",
            youtube_trends=f"Trending YouTube topics for niche {self.niche}...",
            channel_description=self.channel_description
        )
        print(f"Trend Summary Result:\n{trend_summary_result}\n")

        # Step 2: Content Ideas
        content_ideas_result = content_ideas_chain.run(
            trend_summary=trend_summary_result
        )
        print(f"Content Ideas Result:\n{content_ideas_result}\n")

        # Step 3: Optimized Titles
        optimized_titles_result = optimized_titles_chain.run(
            content_ideas=content_ideas_result
        )
        print(f"Optimized Titles Result:\n{optimized_titles_result}\n")

        # Step 4: Thumbnail Ideas
        thumbnail_ideas_result = thumbnail_ideas_chain.run(
            content_ideas=content_ideas_result
        )
        print(f"Thumbnail Ideas Result:\n{thumbnail_ideas_result}\n")

        # Assemble the result
        result = {
            "trend_summary": {
                "text": trend_summary_result
            },
            "content_ideas": self._extract_list(content_ideas_result),
            "optimized_titles": self._extract_list(optimized_titles_result),
            "thumbnail_ideas": self._extract_list(thumbnail_ideas_result),
        }

        print(f"--- Pipeline Complete ---\n")
        return result

    def _extract_list(self, text_block):
        # Helper to parse numbered lists from LLM output
        lines = text_block.strip().split("\n")
        extracted = []
        for line in lines:
            if line.strip() and (line.strip()[0].isdigit() or line.strip().startswith("-")):
                # Remove number or dash prefix
                item = line.split(".", 1)[-1].strip() if "." in line else line[1:].strip()
                extracted.append(item)
        return extracted
