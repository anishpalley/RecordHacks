from flask import Flask, request, jsonify
import os
import importlib.util

# Import modules with valid names
import parody_generator
import download_song_as_mp3
import parody_mixer
import text_to_tts
import parody_audio_generator

# Import wav-to-mp3.py via importlib because of the dash in its filename
wav_mp3_path = os.path.join(os.getcwd(), "wav-to-mp3.py")
spec = importlib.util.spec_from_file_location("wav_to_mp3", wav_mp3_path)
if spec is None:
    raise ImportError(f"Could not load module spec for 'wav-to-mp3.py' from {wav_mp3_path}. Verify the file exists and the path is correct.")
wav_to_mp3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wav_to_mp3)

# For edge.py (asynchronous), we import normally
import edge
import asyncio

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the Music AI App API!"

@app.route("/generate_parody", methods=["POST"])
def generate_parody():
    data = request.json
    song_name = data.get("song_name")
    topic = data.get("topic")
    if not song_name or not topic:
        return jsonify({"error": "Missing song_name or topic"}), 400
    # This function writes a file and returns its path
    result_file = parody_generator.generate_parody_song(song_name, topic)
    if result_file:
        with open(result_file, "r") as f:
            content = f.read()
        return jsonify({"parody_lyrics": content})
    return jsonify({"error": "Parody generation failed"}), 500

@app.route("/download_song", methods=["POST"])
def download_song():
    data = request.json
    song_name = data.get("song_name")
    if not song_name:
        return jsonify({"error": "Missing song_name"}), 400
    output = download_song_as_mp3.download_song_as_mp3(song_name)
    if output:
        return jsonify({"message": f"Song downloaded as {output}"})
    return jsonify({"error": "Download failed"}), 500

@app.route("/convert_wav", methods=["POST"])
def convert_wav():
    data = request.json
    wav_filepath = data.get("wav_filepath")
    mp3_filepath = data.get("mp3_filepath")
    if not wav_filepath or not mp3_filepath:
        return jsonify({"error": "Missing wav_filepath or mp3_filepath"}), 400
    wav_to_mp3.convert_wav_to_mp3(wav_filepath, mp3_filepath)
    return jsonify({"message": f"Converted {wav_filepath} to {mp3_filepath}"})

@app.route("/mix_audio", methods=["POST"])
def mix_audio():
    data = request.json
    vocal_file = data.get("vocal_file")
    instrumental_file = data.get("instrumental_file")
    output_file = data.get("output_file", "final_parody.mp3")
    if not vocal_file or not instrumental_file:
        return jsonify({"error": "Missing vocal_file or instrumental_file"}), 400
    parody_mixer.overlay_parody_on_instrumental(instrumental_file, vocal_file, output_file)
    return jsonify({"message": f"Mixed audio saved as {output_file}"})

@app.route("/text_to_tts", methods=["POST"])
def tts():
    data = request.json
    file_path = data.get("file_path")
    output_file = data.get("output_file")
    if not file_path or not output_file:
        return jsonify({"error": "Missing file_path or output_file"}), 400
    try:
        text_to_tts.convert_text_to_tts(file_path, output_file)
        return jsonify({"message": f"TTS audio saved as {output_file}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_vocals", methods=["POST"])
def generate_vocals():
    data = request.json
    parody_text = data.get("parody_text")
    output_file = data.get("output_file", "vocals.wav")
    if not parody_text:
        return jsonify({"error": "Missing parody_text"}), 400
    try:
        vocals_path = parody_audio_generator.generate_vocals(parody_text, output_file)
        return jsonify({"message": f"Vocals generated and saved as {vocals_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/edge_tts", methods=["POST"])
def edge_tts_route():
    data = request.json
    input_file = data.get("input_file")
    output_filename = data.get("output_filename", "edge_output.mp3")
    rate = data.get("rate", "+0%")
    if not input_file:
        return jsonify({"error": "Missing input_file"}), 400
    try:
        # Run the async edge function
        asyncio.run(edge.generate_speech_from_file(input_file, output_filename, rate))
        return jsonify({"message": f"Edge TTS audio saved as {output_filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
