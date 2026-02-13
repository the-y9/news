import os
from llm import summarize_transcript
from fetch_transcript import get_youtube_transcript
from datetime import date
from urllib.parse import urlparse, parse_qs

# ndate = date.today()
ndate = date(2026,2,12)
DIR = f"docs/{ndate.strftime('%Y')}/{ndate.strftime('%b_%Y')}"
os.makedirs(DIR, exist_ok=True)
FILE = f"{DIR}/{ndate.strftime('%d_%b_%Y')}.md"

if __name__ == "__main__":
    URL = f"https://www.youtube.com/watch?v=BPcBX5bWBxM&list=PLDnIeUIsbmQsN2Nt59WGRGyirDO3zWccZ"
    parsed_url = urlparse(URL)
    query_params = parse_qs(parsed_url.query)

    VIDEO_ID = query_params.get("v", [None])[0]

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
        topic_summary = summarize_transcript(transcript_text, ndate=ndate)
        with open(FILE, "w", encoding="utf-8") as f:
            f.write(topic_summary)
        print(f"✅ saved to {FILE}")

    except Exception as e:
        # if error store transcript
        with open(f"{FILE.split('.')[0]}.txt", "w", encoding="utf-8") as f:
            f.write(transcript_text)
        print("ERROR: ", str(e))
        print(f"\n✅ Transcript saved to {FILE.split('.')[0]}.txt")

    
