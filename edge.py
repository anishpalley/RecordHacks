import edge_tts
import asyncio

async def generate_speech_from_file(input_file, output_filename, rate="+0%"):
    with open(input_file, 'r') as file:
        text = file.read()

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AriaNeural",
        rate=rate  # ✅ Correct format: "+50%", "-20%", etc.
    )

    await communicate.save(output_filename)
    print(f"✅ Audio saved as {output_filename} (Rate: {rate})")

# Example usage
input_file = "parody_lyrics.txt"
output_filename = "output_speed.mp3"

# Adjust speed:
# - "+50%" = 50% faster
# - "-30%" = 30% slower
# - "+100%" = double speed
asyncio.run(generate_speech_from_file(input_file, output_filename, rate="+50%"))