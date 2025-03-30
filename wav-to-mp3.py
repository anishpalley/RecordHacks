from pydub import AudioSegment
import os

def convert_wav_to_mp3(wav_filepath, mp3_filepath):
    """Converts a WAV file to an MP3 file using pydub.

    Args:
        wav_filepath: The path to the input WAV file.
        mp3_filepath: The path to the output MP3 file.
    """
    try:
        # Load the WAV file
        audio = AudioSegment.from_wav(wav_filepath)

        # Export the audio to MP3 format
        audio.export(mp3_filepath, format="mp3")

        print(f"Successfully converted '{wav_filepath}' to '{mp3_filepath}'")

    except FileNotFoundError:
        print(f"Error: WAV file not found at '{wav_filepath}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Specify the input WAV file path
    wav_file = "/demucs_output/htdemucs/normal_song/vocals.wav"

    # Specify the desired output MP3 filename in the current folder
    mp3_file = "vocals.mp3"

    convert_wav_to_mp3(wav_file, mp3_file)