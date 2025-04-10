# splits from vocals and instrumental
import os
import shutil
from pydub import AudioSegment

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

def lower_instrumental_volume(input_file="instrumental.wav", output_file="instrumental.wav", volume_reduction_db=20):
    """
    Lowers the volume of the instrumental track.

    Parameters:
    - input_file (str): Path to the input instrumental file.
    - output_file (str): Path to save the lowered volume instrumental file.
    - volume_reduction_db (int): Amount of volume reduction in decibels (dB).

    Output:
    - Saves the modified instrumental file with reduced volume.
    """
    instrumental = AudioSegment.from_file(input_file)
    
    # Reduce volume by the specified decibels
    lowered_instrumental = instrumental - volume_reduction_db  # or instrumental.apply_gain(-volume_reduction_db)
    
    # Export the modified file
    lowered_instrumental.export(output_file, format="wav")
    print(f"Lowered volume instrumental track saved as {output_file}")

def merge_instrumental_stems(output_folder="demucs_output/htdemucs/original", output_file="instrumental.wav"):
    """
    Merges 'drums.wav', 'bass.wav', and 'other.wav' into a single instrumental track.

    Parameters:
    - output_folder (str): The directory where Demucs saves the separated stems.
    - output_file (str): The final merged instrumental file.

    Output:
    - Saves the combined instrumental file.
    """
    try:
        # Load separated stems
        drums = AudioSegment.from_file(f"{output_folder}/drums.wav")
        bass = AudioSegment.from_file(f"{output_folder}/bass.wav")
        other = AudioSegment.from_file(f"{output_folder}/other.wav")

        # Merge stems by adding them together
        instrumental = drums.overlay(bass).overlay(other)

        # Export the merged instrumental file
        instrumental.export(output_file, format="wav")
        print(f"Instrumental track saved as {output_file}")

        # Lower the volume of the instrumental file
        lower_instrumental_volume(input_file=output_file, output_file=output_file)

    except FileNotFoundError as e:
        print(f"Error: {e}. Ensure the required stem files exist in {output_folder}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def mix_audio(vocal_file, instrumental_file, output_file="output.mp3"):
    """
    Mixes vocals and instrumental into a single audio file.

    Parameters:
    - vocal_file (str): Path to the vocal file.
    - instrumental_file (str): Path to the instrumental file.
    - output_file (str): Path to save the mixed audio file.

    Output:
    - Saves the mixed audio file.
    """
    vocals = AudioSegment.from_file(vocal_file)
    instrumental = AudioSegment.from_file(instrumental_file)
    combined = instrumental.overlay(vocals, position=0)
    combined.export(output_file, format="mp3")
    print(f"Output song saved as {output_file}")

def main():
    # Example usage of extract_audio_demucs
    extract_audio_demucs("original.mp3")

    # Example usage of merge_instrumental_stems
    merge_instrumental_stems()

    # Example usage of mix_audio
    mix_audio("output_speed.mp3", "instrumental.wav")

    # Delete the folder if it exists
    folder_to_delete = 'demucs_output/htdemucs'
    if os.path.exists(folder_to_delete):
        try:
            shutil.rmtree(folder_to_delete)
            print(f"Successfully deleted the folder and its contents: {folder_to_delete}")
        except OSError as e:
            print(f"Error deleting the folder: {e}")
    else:
        print(f"The folder '{folder_to_delete}' does not exist.")

     # Delete files if they exist
    files_to_delete = ["original.mp3", "output_speed.mp3", "instrumental.wav", "parody_lyrics.mp3"]
    for file in files_to_delete:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Successfully deleted the file: {file}")
            except OSError as e:
                print(f"Error deleting the file {file}: {e}")
        else:
            print(f"The file '{file}' does not exist.")

if __name__ == "__main__":
    main()

