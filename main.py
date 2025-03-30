# import pyttsx3

# engine = pyttsx3.init()

# text_to_sing = "La la la, I'm trying to sing."

# # Adjust the rate (words per minute) - lower rate might sound more like a slow song
# engine.setProperty('rate', 200)

# # You can try different voices if available
# voices = engine.getProperty('voices')
# # for voice in voices:
# #     print("Voice:", voice.name, voice.id)
# # engine.setProperty('voice', voices[0].id) # Try different indices

# engine.say(text_to_sing)
# engine.runAndWait()


from transformers import pipeline
from playsound import playsound

text_to_speech = pipeline("text-to-speech", model="suno/bark")
text = "hello my name is anish and im short."
audio = text_to_speech(text)

# Save the audio to a temporary file
output_path = "output.wav"
with open(output_path, "wb") as f:
    f.write(audio["audio"].tobytes())  # Convert to bytes

# Play the audio file
playsound(output_path)