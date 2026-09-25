import os
import re
from dataclasses import dataclass
from textwrap import dedent

from dotenv import load_dotenv
from google import genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()


@dataclass
class AgentResponse:
    content: str


class YouTubeAgent:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY is missing from the .env file.")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"
        self.instructions = dedent("""\
            You are an expert YouTube content analyst with a keen eye for detail! 🎓
            Analyze the supplied transcript and produce a clear, accurate report.
            Include a video overview, meaningful timestamped sections when timestamps
            are available, major themes, key learning points, demonstrations, and
            important references. Avoid inventing details not present in the transcript.
            Use markdown and relevant emojis for educational, technical, gaming,
            technology-review, and creative content.
        """)

    @staticmethod
    def _video_id(video_url: str) -> str:
        match = re.search(
            r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|shorts/|embed/))([^?&/]+)",
            video_url,
        )
        if not match:
            raise ValueError("Please enter a valid YouTube URL.")
        return match.group(1)

    def run(self, prompt: str) -> AgentResponse:
        video_url = prompt.removeprefix("Analyze this video:").strip()
        video_id = self._video_id(video_url)
        transcript = YouTubeTranscriptApi().fetch(video_id)
        transcript_text = "\n".join(
            f"[{item.start:.0f}s] {item.text}" for item in transcript
        )
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{self.instructions}\n\nTranscript:\n{transcript_text}",
        )
        return AgentResponse(content=response.text or "Gemini returned an empty response.")


def build_youtube_agent():
    return YouTubeAgent()

# youtube_agent.print_response(
#     "Analyze this video: https://www.youtube.com/watch?v=JkaxUblCGz0",
#     stream=True,
# )