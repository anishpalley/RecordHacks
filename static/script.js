document.getElementById('generate-parody').addEventListener('click', () => {
    const originalSong = document.getElementById('original-song').value;
    const parodyTheme = document.getElementById('parody-theme').value;
    const voice = document.getElementById('voice').value;
    const speed = document.getElementById('speed').value;

    if (!originalSong || !parodyTheme) {
        alert('Please fill out all fields!');
        return;
    }

    alert(`Generating parody for "${originalSong}" with theme "${parodyTheme}", voice "${voice}", and speed "${speed}".`);
});