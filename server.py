from flask import Flask, request, jsonify, render_template
import asyncio
import parody_generator
import edge
import main

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Route for parody generation (parody_generator)
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

# Route for text-to-speech (edge)
@app.route("/text_to_tts", methods=["POST"])
def tts():
    data = request.json
    input_file = data.get("file_path")
    output_file = data.get("output_file")
    rate = data.get("rate", "+0%")
    if not input_file or not output_file:
        return jsonify({"error": "Missing file_path or output_file"}), 400
    try:
        # Use the edge module to generate TTS
        asyncio.run(edge.generate_speech_from_file(input_file, output_file, rate))
        return jsonify({"message": f"TTS audio saved as {output_file}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to run all scripts in sequence
@app.route("/run_all", methods=["POST"])
def run_all():
    try:
        # Run parody_generator
        parody_generator.generate_parody_song("example_song", "example_topic")
        # Run edge
        asyncio.run(edge.generate_speech_from_file("input.txt", "output.wav"))
        # Run main
        main.main()  # Replace with the actual function in main.py
        return jsonify({"message": "All scripts executed successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
