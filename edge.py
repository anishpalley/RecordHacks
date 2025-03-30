import edge_tts
import asyncio

async def generate_speech_from_file(input_file, output_filename, rate="+0%", voice="en-US-BrianNeural"):
    with open(input_file, 'r', encoding="utf-8") as file:
        text = file.read()

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate  # ✅ Correct format: "+50%", "-20%", etc.
    )

    await communicate.save(output_filename)
    print(f"✅ Audio saved as {output_filename} (Rate: {rate})")

def main(voice="en-US-BrianNeural", speed="1.0x"):
    # Example usage
    input_file = "parody_lyrics.txt"
    output_filename = "output_speed.mp3"

    # Map speed to percentage format
    speed_map = {
        "1.5x": "+50%",
        "1.0x": "+0%",
        "0.75x": "-25%"
    }
    rate = speed_map.get(speed, "+0%")  # Default to normal speed if invalid

    # Generate speech with the mapped rate
    asyncio.run(generate_speech_from_file(input_file, output_filename, rate=rate, voice=voice))

if __name__ == "__main__":
    main()