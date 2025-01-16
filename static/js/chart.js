document.addEventListener("DOMContentLoaded", function () {
    const chartResultsContainer = document.getElementById("chart-results");
    const filterButton = document.getElementById("filter-button");
    const filterDropdown = document.getElementById("filter-dropdown");
    const showMoreButton = document.getElementById("show-more-button");

    let selectedFilters = { type: "song", genre: "all", time: "all" };
    let currentPage = 1; // Track the current page for "Show More"
    let currentRank = 1; // Track the overall rank (across pages)
    let isFetching = false; // Flag to prevent multiple fetches at once

    if (filterDropdown) {
        filterDropdown.classList.add("hidden");
    }

    function updateFilterButtonText() {
        filterButton.textContent = `${selectedFilters.type.toUpperCase()} / ${selectedFilters.genre.toUpperCase()} / ${selectedFilters.time.toUpperCase()}`;
    }

    function fetchChartData() {
        if (isFetching) return; // Prevent multiple fetches at once
        isFetching = true;

        const { type, genre, time } = selectedFilters;
        fetch(`/chart_data/?type=${type}&genre=${genre}&time=${time}&page=${currentPage}`)
            .then((response) => response.json())
            .then((data) => {
                if (currentPage === 1) {
                    chartResultsContainer.innerHTML = ""; // Clear results on the first page
                }

                if (data.results.length === 0 && currentPage === 1) {
                    chartResultsContainer.innerHTML = "<p>No results found.</p>";
                    showMoreButton.classList.add("hidden");
                    return;
                }

                data.results.forEach((item) => {
                    const rankItem = document.createElement("div");
                    rankItem.classList.add("chart-item");

                    // Click redirection logic
                    rankItem.onclick = () => {
                        if (type === "song") window.location.href = `/song/${item.id}/`;
                        else if (type === "album") window.location.href = `/album/${item.id}/`;
                        else if (type === "artist") window.location.href = `/artist/${item.id}/`;
                    };

                    rankItem.innerHTML = `
                        <span class="chart-rank">${currentRank}</span>
                        <img class="chart-image" src="${item.image || '/static/images/default_cover.jpg'}" alt="cover photo">
                        <span class="chart-song">${item.title || item.name}</span>
                        <span class="chart-artist">${item.artist || ''}</span>
                        <span class="chart-views">${item.views || ''} views</span>
                    `;
                    chartResultsContainer.appendChild(rankItem);
                    currentRank++;
                });

                // Show or hide the "Show More" button
                if (data.has_more) {
                    showMoreButton.classList.remove("hidden");
                } else {
                    showMoreButton.classList.add("hidden");
                }

                currentPage++;
                isFetching = false; // Reset fetching flag
            })
            .catch((error) => {
                console.error("Error fetching chart data:", error);
                isFetching = false;
            });
    }

    // Show more button click event
    showMoreButton.addEventListener("click", fetchChartData);

    // Toggle filter dropdown
    filterButton.addEventListener("click", () => {
        filterDropdown.classList.toggle("hidden");
    });

    // Handle filter selection
    filterDropdown.addEventListener("click", (event) => {
        const target = event.target;
        if (target.tagName === "LI") {
            const filterType = target.getAttribute("data-type");
            const filterGenre = target.getAttribute("data-genre");
            const filterTime = target.getAttribute("data-time");

            if (filterType) selectedFilters.type = filterType;
            if (filterGenre) selectedFilters.genre = filterGenre;
            if (filterTime) selectedFilters.time = filterTime;

            updateFilterButtonText();
            filterDropdown.classList.add("hidden"); // Close dropdown
            currentPage = 1; // Reset page
            currentRank = 1; // Reset rank
            fetchChartData(); // Fetch updated data
        }
    });

    // Initial fetch
    fetchChartData();
});