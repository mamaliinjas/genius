document.addEventListener('DOMContentLoaded', () => {
    const lyricLines = document.querySelectorAll('.lyric-line');
    const meaningDisplay = document.getElementById('lyric-meaning-display');
    const meaningText = document.getElementById('lyric-meaning-text');

    lyricLines.forEach(line => {
        line.addEventListener('click', () => {
            const meaning = line.getAttribute('data-meaning');
            if (meaning) {
                meaningText.textContent = meaning;
                meaningDisplay.classList.remove('hidden');
            } else {
                meaningText.textContent = "No meaning available for this line.";
                meaningDisplay.classList.remove('hidden');
            }
        });
    });
});