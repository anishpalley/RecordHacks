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

from pydub import AudioSegment
import time  # For potential small delays if needed

def align_audio(vocal_path, instrumental_path, output_path, vocal_start_offset_ms=0):
    """
    Combines vocal and instrumental audio with manual alignment.

    Args:
        vocal_path (str): Path to the vocal MP3 file.
        instrumental_path (str): Path to the instrumental MP3 file.
        output_path (str): Path to save the combined MP3.
        vocal_start_offset_ms (int): Offset in milliseconds to adjust the vocal track.
                                      Positive value means vocals start later, negative means earlier.
    """
    try:
        vocals = AudioSegment.from_mp3(vocal_path)
        instrumental = AudioSegment.from_mp3(instrumental_path)

        # --- 1. Trim Leading Silence (Optional but Recommended) ---
        # You might want to manually inspect the waveforms in an audio editor
        # to determine if there's significant leading silence to remove.
        # You can use pydub's silence detection, but it might require tuning.
        # For manual trimming based on observation:
        # vocals = vocals[start_time_ms:]
        # instrumental = instrumental[start_time_ms:]

        # --- 2. Adjust Vocal Start Time using offset ---
        if vocal_start_offset_ms > 0:
            # Add silence to the beginning of the vocal track
            silence = AudioSegment.silent(duration=vocal_start_offset_ms)
            vocals = silence + vocals
        elif vocal_start_offset_ms < 0:
            # Remove the beginning of the vocal track
            vocals = vocals[-vocal_start_offset_ms:]  # Negative index from the end

        # --- 3. Ensure Consistent Length (Optional - depends on your goal) ---
        # If one track is longer than the other and you want them to end together,
        # you might need to trim the longer one. For a simple overlay, this might not be necessary.
        # if len(vocals) > len(instrumental):
        #     vocals = vocals[:len(instrumental)]
        # elif len(instrumental) > len(vocals):
        #     instrumental = instrumental[:len(vocals)]

        # --- 4. Overlay the Vocals on the Instrumental ---
        combined = instrumental.overlay(vocals)

        # --- 5. Export the Combined Audio ---
        combined.export(output_path, format="mp3")
        print(f"Successfully combined and aligned audio to: {output_path}")

    except FileNotFoundError:
        print("Error: One or both input files not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    vocal_file = "parody_lyrics.mp3"
    instrumental_file = "instrumental.wav"
    output_file = "out.mp3"

    # --- Manual Alignment Offset (in milliseconds) ---
    # Positive value: Vocals start later by this amount.
    # Negative value: Vocals start earlier by this amount.
    # You'll need to experiment with this value.
    alignment_offset = 0  # Start with 0 and adjust

    align_audio(vocal_file, instrumental_file, output_file, vocal_start_offset_ms=alignment_offset)

    print("\nExperiment with the 'alignment_offset' value in the script to fine-tune the synchronization.")
    print("You might need to try different positive and negative values and listen to the result.")
    print("Consider using an audio editor (like Audacity) to visually inspect the waveforms")
    print("to get a better idea of the required offset.")