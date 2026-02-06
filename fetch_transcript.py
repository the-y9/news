from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    VideoUnavailable,
)


def get_youtube_transcript(video_id):
    if video_id is None:
        return
    try:        
        api = YouTubeTranscriptApi()

        # en → hi → anything
        return api.fetch(
            video_id=video_id,
            languages=["en", "hi"]
        )
    except (NoTranscriptFound, VideoUnavailable) as e:
        # print(str(e))
        return None



if __name__ == "__main__":

    URL = f"https://www.youtube.com/watch?v=N7MVVQamfX0"
    VIDEO_ID = URL.split("=")[-1]
    print(VIDEO_ID)

    transcript = get_youtube_transcript(VIDEO_ID)

    if transcript:
        text = " ".join(line.text for line in transcript)
        print(len(text))
    else:
        text = "error"
        print(text)

    with open("transcript.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ Transcript saved to rough.txt")
