import re, json, os
from typing import List
import time
from google import genai
from dotenv import load_dotenv
from datetime import date
today = date.today()
load_dotenv()

# ---------- CONFIG ----------
MAX_CHUNK_SIZE = 4000  # Approx chars/tokens per chunk
MODEL_NAME = "gemini-2.5-flash-lite"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------- HELPER FUNCTIONS ----------

def split_into_chunks(text: str, max_size: int = MAX_CHUNK_SIZE) -> List[str]:
    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) + 1 > max_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            current_chunk += "\n" + para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def create_prompt(chunk: str) -> str:
    """
    Prepare prompt for UPSC key points with headlines
    """
    return f"""
You are an expert UPSC content analyst. I will provide you with a part of a transcript that may be in any language. 

Your task:
1. Translate fully into English if needed.
2. Detect news headlines from this transcript.
3. Organize information into UPSC Syllabus: Polity, Economy, Environment, Science & Tech, International Relations, ... , Other.
4. For each topic, list key points accurately, concise, compact, and exam-relevant.
5. Do NOT hallucinate. Only include what is present in the transcript.
6. Output as .md and follow only:

Date: {today.strftime("%d_%b_%Y")}
## <Topic Name>
#### Headline: <headline text>
  - Key Point 1
  - Key Point 2

Transcript chunk:
\"\"\"{chunk}\"\"\"
"""


def process_chunk_with_gemini(prompt: str) -> dict:
    """
    Sends chunk to Gemini via genai SDK
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    content = response.text
    return content

# ---------- MAIN PIPELINE ----------

def summarize_transcript(transcript_text: str) -> dict:
    chunks = split_into_chunks(transcript_text)
    results = []

    for i, chunk in enumerate(chunks, 1):
        print(f"Processing chunk {i}/{len(chunks)}...")
        prompt = create_prompt(chunk)
        chunk_result = process_chunk_with_gemini(prompt)
        results.append(chunk_result)
        time.sleep(1)  # avoid rate limits

    merged = "\n\n".join(results)
    return merged

# ---------- USAGE ----------
DIR = f"{today.strftime('%Y')}/{today.strftime('%b_%Y')}"
os.makedirs(DIR, exist_ok=True)
FILE = f"{DIR}/{today.strftime('%d_%b_%Y')}.md"
if __name__ == "__main__":
    # Load transcript
    with open(f"transcript.txt", "r", encoding="utf-8") as f:
        transcript_text = f.read()

    print("Starting topic-wise summarization using Gemini Free Tier...")
    topic_summary = summarize_transcript(transcript_text)

    # Save final md
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(topic_summary)

    print("✅ Topic-wise key points with headlines saved to topic_summary.json")
