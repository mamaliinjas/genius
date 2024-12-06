document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchResultsContainer = document.getElementById("search-results");
    const spinner = document.createElement("div");
    spinner.classList.add("loading-spinner");
    spinner.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(spinner); // Add spinner to the body

    // Function to show or hide the spinner
    function toggleSpinner(show) {
        spinner.style.display = show ? "block" : "none";
    }

    // Add event listener for when user types in the search box
    searchInput.addEventListener("input", function () {
        const query = searchInput.value;

        if (query.length > 0) { // Start search on any input
            toggleSpinner(true); // Show spinner while fetching
            fetch(`/ajax_search/?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    toggleSpinner(false); // Hide spinner after fetching
                    searchResultsContainer.innerHTML = ""; // Clear previous results

                    if (data.artists.length > 0 || data.songs.length > 0 || data.albums.length > 0) {
                        const resultList = document.createElement("ul");
                        resultList.classList.add("search-results-list");

                        // Artists results
                        if (data.artists.length > 0) {
                            const artistHeader = document.createElement("li");
                            artistHeader.innerHTML = "<strong>Artists:</strong>";
                            resultList.appendChild(artistHeader);
                            data.artists.forEach(artist => {
                                const li = document.createElement("li");
                                li.innerHTML = `<a href="/artist/${artist.id}/">${artist.name}</a>`;
                                resultList.appendChild(li);
                            });
                        }

                        // Songs results
                        if (data.songs.length > 0) {
                            const songHeader = document.createElement("li");
                            songHeader.innerHTML = "<strong>Songs:</strong>";
                            resultList.appendChild(songHeader);
                            data.songs.forEach(song => {
                                const li = document.createElement("li");
                                li.innerHTML = `<a href="/song/${song.id}/">${song.title} by ${song.artist__name}</a>`;
                                resultList.appendChild(li);
                            });
                        }

                        // Albums results
                        if (data.albums.length > 0) {
                            const albumHeader = document.createElement("li");
                            albumHeader.innerHTML = "<strong>Albums:</strong>";
                            resultList.appendChild(albumHeader);
                            data.albums.forEach(album => {
                                const li = document.createElement("li");
                                li.innerHTML = `<a href="/album/${album.id}/">${album.title} by ${album.artist__name}</a>`;
                                resultList.appendChild(li);
                            });
                        }

                        searchResultsContainer.appendChild(resultList);
                    } else {
                        searchResultsContainer.innerHTML = "<p>No results found</p>";
                    }
                })
                .catch(error => {
                    toggleSpinner(false); // Hide spinner
                    console.error("Error fetching search results:", error);
                    searchResultsContainer.innerHTML = "<p>Error loading results</p>";
                });
        } else {
            searchResultsContainer.innerHTML = ""; // Clear results if query is empty
            toggleSpinner(false); // Hide spinner
        }
    });
});