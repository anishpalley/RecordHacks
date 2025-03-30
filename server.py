from flask import Flask, request, jsonify, render_template, send_file
import asyncio
import download_song_as_mp3
import parody_generator
import edge
import main
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Route for parody generation
@app.route("/generate_parody", methods=["POST"])
def generate_parody():
    data = request.json
    song_name = data.get("song_name")
    topic = data.get("topic")
    if not song_name or not topic:
        return jsonify({"error": "Missing song_name or topic"}), 400

    result_file = parody_generator.generate_parody_song(song_name, topic)
    if result_file:
        try:
            download_song_as_mp3.main(song_name)
            edge.main()  # Generate TTS vocals
            main.main()
            return jsonify({
                "parody_lyrics": open(result_file).read(),
                "audio_file_url": "/download_audio"
            })
        except Exception as e:
            return jsonify({"error": f"Parody generated, but audio processing failed: {str(e)}"}), 500
    return jsonify({"error": "Parody generation failed"}), 500

# Route to serve the audio file
@app.route("/download_audio")
def download_audio():
    audio_path = "output.mp3"  # Ensure this matches the output file path
    if os.path.exists(audio_path):
        return send_file(audio_path, mimetype="audio/mpeg", as_attachment=False)
    return jsonify({"error": "Audio file not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
