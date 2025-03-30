import os
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv

load_dotenv()
GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
    {"role": "system", "content": "You are a helpful assistant that creates parody versions of song lyrics. Ensure the output maintains the same rhythm, syllables, and rhyme as the original lyrics, and make it funny or clever. Do not include the word 'Parody:' in the output."},
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

# Batch multiple lines together in fewer API calls
def generate_parody_batch(original_lines, topic, batch_size=10):

    original_lines_count = len("\n".join(original_lines).split())
    
    prompt = (
    f"Write a parody version of this music about '{topic}'. Do not include the original song in the output "
    f"Try to keep the same rhythm, syllables, and rhyme if possible, and limit it to {original_lines_count/len(original_lines)} words or less\n"
    f"Make it funny or clever, but keep it listenable. Do not include section headers such as verses or chorus or outro.\n"
    f"Do not include the word 'Parody:' or any similar prefix in the output. Include only the lyrics. Return as plain song lyrics"
    )

    results = []
    for i in range(0, len(original_lines), batch_size):
        batch = original_lines[i:i+batch_size]
        prompts = [prompt]
        for line in batch:
            prompts.append(f"Original: \"{line.strip()}\"")

        if prompts:
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",  # Cheaper, faster model
                    messages=[{"role": "system", "content": prompt},
                             {"role": "user", "content": "\n\n".join(prompts)}],
                    temperature=0.8,
                    max_tokens=60

                )
                parodies = response.choices[0].message.content.strip().split("\n")
                results.extend([p for p in parodies if p.strip()])
            except Exception as e:
                print(f"Error: {e}")
                results.extend(batch)

    return results

def generate_parody_song(song_name, topic):
    print("🎤 Parody Song Generator 🎵")
    # Fetch lyrics using existing functions
    url = get_song_url(song_name)
    if not url:
        print("❌ Song not found on Genius.")
        return None
    lyrics = scrape_lyrics(url)
    if not lyrics:
        print("❌ Could not extract lyrics.")
        return None
    print("Generating parody...\n")
    original_lines = lyrics.split("\n")
    # Reuse your batch logic (keeping the original batch size)
    parody_lines = generate_parody_batch(original_lines, topic)
    parody_lyrics = "\n".join(parody_lines)
    with open("parody_lyrics.txt", "w") as file:
        file.write(parody_lyrics)
    print("Parody lyrics saved to parody_lyrics.txt")
    return "parody_lyrics.txt"

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

    # Store the output in a file
    with open("parody_lyrics.txt", "w") as file:
        file.write(parody_lyrics)

    print("\nParody lyrics saved to parody_lyrics.txt")


if __name__ == "__main__":
    main()