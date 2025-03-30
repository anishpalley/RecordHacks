# splits from vocals and instrumental
import os

def extract_audio_demucs(input_song, output_folder="demucs_output"):
    """
    Uses Facebook AI's Demucs to separate vocals and instrumentals.

    Parameters:
    - input_song (str): Path to the song file (e.g., 'song.mp3').
    - output_folder (str): Folder where extracted files will be saved.

    Output:
    - Saves separated files in the specified output folder.
    """
    command = f"demucs -o {output_folder} {input_song}"
    os.system(command)
    print(f"Processing complete! Check the '{output_folder}' folder.")

# Example usage:
extract_audio_demucs("normal_song.mp3")

from pydub import AudioSegment
def merge_instrumental_stems(output_folder="demucs_output/htdemucs/normal_song", output_file="instrumental.wav"):
    """
    Merges 'drums.wav', 'bass.wav', and 'other.wav' into a single instrumental track.

    Parameters:
    - output_folder (str): The directory where Demucs saves the separated stems.
    - output_file (str): The final merged instrumental file.

    Output:
    - Saves the combined instrumental file.
    """
    # Load separated stems
    drums = AudioSegment.from_file(f"{output_folder}/drums.wav")
    bass = AudioSegment.from_file(f"{output_folder}/bass.wav")
    other = AudioSegment.from_file(f"{output_folder}/other.wav")

    # Merge stems by adding them together
    instrumental = drums.overlay(bass).overlay(other)

    # Export final instrumental file
    instrumental.export(output_file, format="wav")
    print(f"Instrumental track saved as {output_file}")

# Example usage:
merge_instrumental_stems()

import librosa
import soundfile as sf

# Load audio files
instrumental, sr = librosa.load("output/accompaniment.wav", sr=None)
new_vocals, sr = librosa.load("new_vocals.mp3", sr=None)

# Adjust tempo to match original
new_vocals = librosa.effects.time_stretch(new_vocals, rate=1.1)  # Adjust rate as needed

# Save aligned vocals
sf.write("aligned_vocals.wav", new_vocals, sr)


# combines ours vocals and adds the it to the instrumental
