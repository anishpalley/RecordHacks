import os
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv
from pydub import AudioSegment
import subprocess

load_dotenv()
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# 1. Get lyrics from Genius
def get_song_url(song_name):
    base_url = "https://api.genius.com"
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
    search_url = f"{base_url}/search?q={requests.utils.quote(song_name)}"
    response = requests.get(search_url, headers=headers)
    hits = response.json().get("response", {}).get("hits", [])
    return hits[0]["result"]["url"] if hits else None

def scrape_lyrics(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    lyrics_divs = soup.find_all("div", class_=lambda x: x and "Lyrics__Container" in x)
    if lyrics_divs:
        lyrics = "\n".join(div.get_text(separator="\n") for div in lyrics_divs)
        return lyrics.strip()
    lyrics_div = soup.find("div", class_="lyrics")
    return lyrics_div.get_text(separator="\n").strip() if lyrics_div else ""

# 2. Generate parody lyrics with OpenAI
def generate_parody(original_line, topic):
    prompt = (
        f"Original lyric: \"{original_line.strip()}\"\n"
        f"Write a parody version of this line about '{topic}'. "
        f"Keep rhythm and rhyme similar. Make it clever and listenable."
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=60
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating parody: {e}")
        return original_line

def generate_vocals(parody_text, output_file="vocals.wav"):
    import numpy as np
    from scipy.io.wavfile import write as write_wav

    from bark_module.api import generate_audio, preload_models

    preload_models()
    audio_array = generate_audio(parody_text)

    write_wav(output_file, 22050, np.array(audio_array))
    return output_file





# 4. Overlay vocals on instrumental

def mix_audio(vocal_file, instrumental_file, output_file="final_parody.mp3"):
    vocals = AudioSegment.from_file(vocal_file)
    instrumental = AudioSegment.from_file(instrumental_file)
    mixed = instrumental.overlay(vocals, position=0)
    mixed.export(output_file, format="mp3")

# 5. Main CLI Program

def main():
    print("\U0001F3A4 Parody Song Generator 🎵")
    song_name = input("Enter a song title (include artist): ")
    topic = input("Enter a topic for the parody: ")
    instrumental_path = input("Enter path to instrumental audio file (e.g. MP3): ")

    print("\nFetching lyrics...")
    url = get_song_url(song_name)
    if not url:
        print("❌ Song not found on Genius.")
        return

    lyrics = scrape_lyrics(url)
    if not lyrics:
        print("❌ Could not extract lyrics.")
        return

    print("\nGenerating parody lyrics...")
    parody_lines = []
    for line in lyrics.split("\n")[:12]:  # Limit to 12 lines for speed
        if line.strip() == "" or line.startswith("["):
            parody_lines.append(line)
        else:
            parody_lines.append(generate_parody(line, topic))

    parody_text = "\n".join(parody_lines)
    print("\nGenerated Parody:\n")
    print(parody_text)

    print("\nSynthesizing vocals with Bark...")
    vocals_path = generate_vocals(parody_text)

    print("\nMixing vocals with instrumental...")
    mix_audio(vocals_path, instrumental_path)

    print("\n✅ Final parody saved as final_parody.mp3")

if __name__ == "__main__":
    main()
