# ParodyAI 🎤

ParodyAI is an AI-powered application that transforms any song into a hilarious parody. It generates parody lyrics, synthesizes vocals, and overlays them on the instrumental track to create a complete parody audio file.

---

## Features 🚀

1. **Generate Parody Lyrics**  
   - AI generates clever and funny parody lyrics while maintaining the rhythm and rhyme of the original song.

2. **Text-to-Singing AI**  
   - Converts parody lyrics into realistic vocals using AI-powered voice synthesis.

3. **Instrumental and Vocal Mixing**  
   - Overlays generated vocals on the instrumental track to produce a complete parody song.

4. **Customizable Voices and Speed**  
   - Choose from multiple AI voices and adjust playback speed for a personalized parody.

5. **Web Interface**  
   - User-friendly web interface for generating and downloading parody songs.

---

## How It Works 🛠️

1. **Input Song and Parody Theme**  
   - Provide the original song title and the theme for the parody.

2. **Generate Parody Lyrics**  
   - The app fetches the original lyrics and generates parody lyrics using OpenAI's GPT model.

3. **Download Instrumental**  
   - Extract the instrumental track using tools like `yt-dlp` or `Demucs`.

4. **Synthesize Vocals**  
   - Use Edge TTS to generate vocals from the parody lyrics.

5. **Mix and Export**  
   - Combine vocals and instrumental to create the final parody audio file.

---

## Installation 🖥️

1. Clone the repository:
   ```bash
   git clone https://github.com/anishpalley/ParodyAI.git
   cd ParodyAI
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file with the following keys:
     ```
     GENIUS_API_TOKEN=<your_genius_api_token>
     OPENAI_API_KEY=<your_openai_api_key>
     ```

4. Run the Flask server:
   ```bash
   python server.py
   ```

5. Open the app in your browser at `http://127.0.0.1:5000`.

---

## Usage 🎶

### Web Interface
1. Open the app in your browser.
2. Enter the song title, parody theme, voice, and speed.
3. Click "Generate Parody" to create and download your parody song.

### API Endpoints
- **Generate Parody**:  
  Endpoint: `/generate_parody`  
  Method: `POST`  
  Payload:  
  ```json
  {
    "song_name": "Song Title",
    "topic": "Parody Theme",
    "voice": "Voice Option",
    "speed": "normal | slow | fast"
  }
  ```
  Response:  
  - On success:  
    ```json
    {
      "parody_lyrics": "Generated parody lyrics...",
      "audio_file_url": "/download_audio"
    }
    ```
  - On failure:  
    ```json
    {
      "error": "Error message"
    }
    ```

- **Download Audio**:  
  Endpoint: `/download_audio`  
  Method: `GET`  
  Response:  
  - On success: Returns the generated MP3 file.  
  - On failure:  
    ```json
    {
      "error": "Audio file not found"
    }
    ```

---

## Tools and Libraries 🛠️

- **Flask**: Backend framework for the web interface.
- **OpenAI GPT**: Generates parody lyrics.
- **Edge TTS**: Text-to-speech synthesis.
- **Pydub**: Audio processing and mixing.
- **Demucs**: Instrumental and vocal separation.
- **yt-dlp**: Downloads audio from YouTube.
- **Genius API**: Fetches song lyrics.

---

## File Structure 📂

```
RecordHacks/
├── parody_generator.py         # Generates parody lyrics
├── server.py                   # Flask server for the web interface
├── main.py                     # Handles audio separation and mixing
├── edge.py                     # Text-to-speech synthesis
├── download_song_as_mp3.py     # Downloads songs from YouTube
├── templates/                  # HTML templates for the web interface
├── static/                     # CSS and JS files for the web interface
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
```

---

## Example 🎤

1. Input:  
   - Song: "Never Gonna Give You Up"  
   - Theme: "Snacks and Yoga"

2. Output:  
   - Parody Lyrics:  
     ```
     We're no strangers to snacks,  
     You know the crunch and so do I...  
     ```
   - Parody Audio: Downloadable MP3 file.

---

## Contributing 🤝

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

---

## License 📜

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments 🙌

- [OpenAI](https://openai.com) for GPT models.
- [Demucs](https://github.com/facebookresearch/demucs) for audio separation.
- [Genius API](https://genius.com/developers) for fetching song lyrics.