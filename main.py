import os
from llm import summarize_transcript
from fetch_transcript import get_youtube_transcript
from datetime import date

today = date.today()
DIR = f"dev/{today.strftime('%Y')}/{today.strftime('%b_%Y')}"
os.makedirs(DIR, exist_ok=True)
FILE = f"{DIR}/{today.strftime('%d_%b_%Y')}.md"

if __name__ == "__main__":
    URL = f"https://www.youtube.com/watch?v=G9kTwGdrN1U"
    VIDEO_ID = URL.split("=")[-1]
    print(VIDEO_ID)

    transcript = get_youtube_transcript(VIDEO_ID)
    if transcript:
        transcript_text = " ".join(line.text for line in transcript)
        print(len(transcript_text))
    else:
        print("No Transcript")
        exit()

    print("Starting llm...")
    try:
        topic_summary = summarize_transcript(transcript_text)
        with open(FILE, "w", encoding="utf-8") as f:
            f.write(topic_summary)
        print(f"✅ saved to {FILE}")

    except Exception as e:
        with open(f"{FILE.split('.')[0]}.txt", "w", encoding="utf-8") as f:
            f.write(transcript_text)
        print("ERROR: ", str(e))
        print(f"\n✅ Transcript saved to {FILE.split('.')[0]}.txt")

    
