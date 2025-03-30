import yt_dlp

def download_song_as_mp3(song_name, output_path="original.mp3"):
    print(f"\n🔎 Searching and downloading '{song_name}' from YouTube...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': False,
        'outtmpl': output_path,  # force output to original.mp3
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
if __name__ == "__main__":
    song = input("Enter the song title to download: ")
    download_song_as_mp3(song)
