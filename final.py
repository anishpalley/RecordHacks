import os
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv

# generates lyrics

load_dotenv()
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
    temperature=0.8,
    max_tokens=60
)

def get_song_url(song_name):
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
    search_url = f"{base_url}/search?q={requests.utils.quote(song_name)}"
    response = requests.get(search_url, headers=headers)
    hits = response.json()["response"]["hits"]

    if not hits:
        return None

    return hits[0]["result"]["url"]


def scrape_lyrics(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Try modern structure
    lyrics_divs = soup.find_all("div", class_=lambda x: x and "Lyrics__Container" in x)
    if lyrics_divs:
        lyrics = "\n".join(div.get_text(separator="\n") for div in lyrics_divs)
        return lyrics.strip()

    # Fallback for older Genius structure
    lyrics_div = soup.find("div", class_="lyrics")
    if lyrics_div:
        return lyrics_div.get_text(separator="\n").strip()

    return ""


def generate_parody(original_line, topic):
    prompt = (
        f"Original lyric: \"{original_line.strip()}\"\n"
        f"Write a parody version of this line about '{topic}'. "
        f"Try to keep the same rhythm, syllables, and rhyme if possible.\n"
        f"Make it funny or clever, but keep it listenable."
    )

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-3.5-turbo" if you don’t have GPT-4 access
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=60
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating parody: {e}")
        return original_line


# Batch multiple lines together in fewer API calls
def generate_parody_batch(original_lines, topic, batch_size=5):
    results = []
    for i in range(0, len(original_lines), batch_size):
        batch = original_lines[i:i+batch_size]
        prompts = []
        for line in batch:
            if line.strip() == "" or line.startswith("["):
                results.append(line)
            else:
                prompts.append(f"Original: \"{line.strip()}\"\nParody about '{topic}':")
        
        if prompts:
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",  # Cheaper, faster model
                    messages=[{"role": "system", "content": f"Write parody versions of these lyrics about '{topic}'. Keep the rhythm and rhyme if possible."},
                             {"role": "user", "content": "\n\n".join(prompts)}],
                    temperature=0.8
                )
                parodies = response.choices[0].message.content.strip().split("\n")
                results.extend([p for p in parodies if p.strip()])
            except Exception as e:
                print(f"Error: {e}")
                results.extend(batch)
    
    return results


def main():
    print("🎤 Parody Song Generator 🎵")
    song_name = input("Enter a song title (include artist if needed): ")
    topic = input("Enter a topic for the parody: ")

    print("\nFetching lyrics...")
    url = get_song_url(song_name)
    if not url:
        print("❌ Song not found on Genius.")
        return

    lyrics = scrape_lyrics(url)
    if not lyrics:
        print("❌ Could not extract lyrics.")
        return

    print("\nGenerating parody...\n")
    parody_lines = generate_parody_batch(lyrics.split("\n"), topic)
    
    parody_lyrics = "\n".join(parody_lines)
    print("🎶 Parody Lyrics 🎶\n")
    print(parody_lyrics)


if __name__ == "__main__":
    main()

# downloads song from online
import yt_dlp

def download_song_as_mp3(song_name, output_path="original"):
    print(f"\n🔎 Searching and downloading '{song_name}' from YouTube...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': False,
        'outtmpl': output_path,  # no .mp3
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f"ytsearch1:{song_name}"])
            print(f"✅ Downloaded and saved as {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Error downloading song: {e}")
            return None

# Example usage
download_song_as_mp3(song_name)
