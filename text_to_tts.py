
from gtts import gTTS

# Specify the filename
file_path = "parody_lyrics.txt"
output_file = "parody_lyrics.mp3"  # Name for your output MP3 file

try:
    with open(file_path, 'r') as file:
        text_to_speak = file.read()

    # Create a gTTS object
    # 'en' specifies the language (English). You can change this if needed.
    tts = gTTS(text=text_to_speak, lang='en')

    # Save the audio to an MP3 file
    tts.save(output_file)

    print(f"Text from '{file_path}' has been saved as '{output_file}'")

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Make sure it's in the same folder as the script.")
except Exception as e:
    print(f"An error occurred: {e}")