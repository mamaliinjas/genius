document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchResultsContainer = document.getElementById("search-results");

    // Add event listener for when user types in search box
    searchInput.addEventListener("input", function () {
        const query = searchInput.value;

        // Only search if query length is greater than 2 characters
        if (query.length > 2) {
            fetch(`/ajax_search/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    searchResultsContainer.innerHTML = ''; // Clear previous results

                    // Display artists results
                    if (data.artists.length > 0) {
                        const artistsList = document.createElement("ul");
                        data.artists.forEach(artist => {
                            const li = document.createElement("li");
                            li.innerHTML = `<a href="/artist/${artist.id}/">${artist.name}</a>`;
                            artistsList.appendChild(li);
                        });
                        searchResultsContainer.appendChild(artistsList);
                    }

                    // Display songs results
                    if (data.songs.length > 0) {
                        const songsList = document.createElement("ul");
                        data.songs.forEach(song => {
                            const li = document.createElement("li");
                            li.innerHTML = `<a href="/song/${song.id}/">${song.title} by ${song.artist__name}</a>`;
                            songsList.appendChild(li);
                        });
                        searchResultsContainer.appendChild(songsList);
                    }

                    // Display albums results
                    if (data.albums.length > 0) {
                        const albumsList = document.createElement("ul");
                        data.albums.forEach(album => {
                            const li = document.createElement("li");
                            li.innerHTML = `<a href="/album/${album.id}/">${album.title} by ${album.artist__name}</a>`;
                            albumsList.appendChild(li);
                        });
                        searchResultsContainer.appendChild(albumsList);
                    }

                    // Display lyrics results if no other results
                    if (data.lyrics_results.length > 0) {
                        const lyricsList = document.createElement("ul");
                        data.lyrics_results.forEach(song => {
                            const li = document.createElement("li");
                            li.innerHTML = `<a href="/song/${song.id}/">${song.title}</a> - ${song.lyrics}`;
                            lyricsList.appendChild(li);
                        });
                        searchResultsContainer.appendChild(lyricsList);
                    }

                    // If no results, show a message
                    if (!data.artists.length && !data.songs.length && !data.albums.length && !data.lyrics_results.length) {
                        searchResultsContainer.innerHTML = '<p>No results found</p>';
                    }
                })
                .catch(error => console.error('Error:', error));
        } else {
            searchResultsContainer.innerHTML = ''; // Clear results if query is too short
        }
    });
});