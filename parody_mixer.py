from pydub import AudioSegment

def overlay_parody_on_instrumental(instrumental_path, parody_vocals_path, output_path="final_parody.mp3"):
    print("🔊 Loading audio...")
    instrumental = AudioSegment.from_file(instrumental_path)
    parody_vocals = AudioSegment.from_file(parody_vocals_path)

    print(f"🎧 Instrumental duration: {len(instrumental) / 1000:.2f}s")
    print(f"🎙️ Parody vocals duration: {len(parody_vocals) / 1000:.2f}s")

    # ✅ Overlay parody vocals on top of instrumental from time 0
    combined = instrumental.overlay(parody_vocals, position=0)

    # ✅ If instrumental is longer, keep the rest after vocals
    if len(instrumental) > len(parody_vocals):
        tail = instrumental[len(parody_vocals):]
        combined += tail

    # Export the result
    print(f"💾 Exporting to {output_path}")
    combined.export(output_path, format="mp3")
    print("✅ Done!")

# Example usage
if __name__ == "__main__":
    overlay_parody_on_instrumental(
        instrumental_path="instrumental.wav",
        parody_vocals_path="parody_lyrics.mp3",
        output_path="OUTPUT.mp3"
    )
