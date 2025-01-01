document.addEventListener('DOMContentLoaded', () => {
    const lyricsContainer = document.querySelector('.lyrics-container');
    const meaningDisplay = document.querySelector('#lyric-meaning-display');
    const meaningText = document.querySelector('#lyric-meaning-text');

    if (lyricsContainer) {
        lyricsContainer.addEventListener('click', (e) => {
            // Ensure the clicked element is a highlighted line
            if (e.target.classList.contains('highlight')) {
                const meaning = e.target.getAttribute('data-meaning');
                if (meaning) {
                    // Update the meaning box content
                    meaningText.textContent = meaning;

                    // Show the meaning display
                    meaningDisplay.classList.remove('hidden');
                    meaningDisplay.classList.add('active');
                }
            }
        });
    }
});