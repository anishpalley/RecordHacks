# splits from vocals and instrumental
# import os

# def extract_audio_demucs(input_song, output_folder="demucs_output"):
#     """
#     Uses Facebook AI's Demucs to separate vocals and instrumentals.

#     Parameters:
#     - input_song (str): Path to the song file (e.g., 'song.mp3').
#     - output_folder (str): Folder where extracted files will be saved.

#     Output:
#     - Saves separated files in the specified output folder.
#     """
#     command = f"demucs -o {output_folder} {input_song}"
#     os.system(command)
#     print(f"Processing complete! Check the '{output_folder}' folder.")

# # Example usage:
# extract_audio_demucs("normal_song.mp3")

# from pydub import AudioSegment
# def merge_instrumental_stems(output_folder="demucs_output/htdemucs/normal_song", output_file="instrumental.wav"):
#     """
#     Merges 'drums.wav', 'bass.wav', and 'other.wav' into a single instrumental track.

#     Parameters:
#     - output_folder (str): The directory where Demucs saves the separated stems.
#     - output_file (str): The final merged instrumental file.

#     Output:
#     - Saves the combined instrumental file.
#     """
#     # Load separated stems
#     drums = AudioSegment.from_file(f"{output_folder}/drums.wav")
#     bass = AudioSegment.from_file(f"{output_folder}/bass.wav")
#     other = AudioSegment.from_file(f"{output_folder}/other.wav")

#     # Merge stems by adding them together
#     instrumental = drums.overlay(bass).overlay(other)

#     # Export final instrumental file
#     instrumental.export(output_file, format="wav")
#     print(f"Instrumental track saved as {output_file}")

# # Example usage:
# merge_instrumental_stems()

import aubio
import numpy as np

# Load tracks
instrumental = aubio.source("instrumental.wav")
vocal = aubio.source("parody_lyrics.mp3")

# Set up beat tracker
beat_detector = aubio.tempo("default", 1024, 512, instrumental.samplerate)

# Track beats in the instrumental
beats_inst = []
total_frames = 0
while True:
    samples, read = instrumental()
    if beat_detector(samples):
        beats_inst.append(total_frames)
    total_frames += read
    if read < 512:
        break

# Track beats in the vocal (same process as above)
beats_vocal = []
vocal.seek(0)
while True:
    samples, read = vocal()
    if beat_detector(samples):
        beats_vocal.append(total_frames)
    total_frames += read
    if read < 512:
        break

# Use the beat positions to adjust the timing of vocals relative to instrumental
# This is a more advanced approach where you align based on detected beats


from pydub import AudioSegment

instrumental = AudioSegment.from_wav("instrumental.wav")
new_vocals = AudioSegment.from_wav("parody_lyrics.mp3")

# Adjust volume levels
new_vocals = new_vocals - 5  # Lower vocal volume
final_mix = instrumental.overlay(new_vocals)

# Export final song
final_mix.export("final_song.mp3", format="mp3")

# combines ours vocals and adds the it to the instrumental
