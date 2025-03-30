document.getElementById('generate-parody').addEventListener('click', async () => {
    const originalSong = document.getElementById('songName').value;
    const parodyTheme = document.getElementById('topic').value;

    if (!originalSong || !parodyTheme) {
        alert('Please fill out all fields!');
        return;
    }

    try {
        const response = await fetch('/generate_parody', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                song_name: originalSong,
                topic: parodyTheme,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            alert(`Error: ${error.error}`);
            return;
        }

        const data = await response.json();
        document.getElementById('parodyResult').innerText = data.parody_lyrics;
    } catch (error) {
        alert(`Failed to generate parody: ${error.message}`);
    }
});