document.addEventListener("DOMContentLoaded", function () {
    const chartResultsContainer = document.getElementById("chart-results");
    const showMoreButton = document.getElementById("show-more-button");
    const filterButton = document.getElementById("filter-button");
    const filterDropdown = document.getElementById("filter-dropdown");

    let selectedFilters = { type: "song", genre: "all", time: "all" };
    let currentPage = 1;

    function updateFilterButtonText() {
        filterButton.textContent = `${selectedFilters.type.toUpperCase()} / ${selectedFilters.genre.toUpperCase()} / ${selectedFilters.time.toUpperCase()}`;
    }

    function fetchChartData(isLoadMore = false) {
        const { type, genre, time } = selectedFilters;

        fetch(`/chart_data/?type=${type}&genre=${genre}&time=${time}&page=${currentPage}`)
            .then((response) => response.json())
            .then((data) => {
                if (!isLoadMore) {
                    chartResultsContainer.innerHTML = ""; // Clear previous results
                }

                if (data.results.length === 0 && currentPage === 1) {
                    chartResultsContainer.innerHTML = "<p>No results found.</p>";
                    showMoreButton.classList.add("hidden");
                    return;
                }

                // Calculate the starting rank for this page
                const startingRank = (currentPage - 1) * 10;

                data.results.forEach((item, index) => {
                    const rankItem = document.createElement("div");
                    rankItem.classList.add("chart-item");

                    // Click redirection logic
                    if (type === "song") {
                        rankItem.onclick = () => window.location.href = `/song/${item.id}/`;
                    } else if (type === "album") {
                        rankItem.onclick = () => window.location.href = `/album/${item.id}/`;
                    } else if (type === "artist") {
                        rankItem.onclick = () => window.location.href = `/artist/${item.id}/`;
                    }

                    rankItem.innerHTML = `
                        <span class="chart-rank">${startingRank + index + 1}</span>
                        <img class="chart-image" src="${item.image || '/static/images/default_cover.jpg'}" alt="cover photo">
                        <span class="chart-title">${item.title || item.name}</span>
                        <span class="chart-artist">${item.artist || ''}</span>
                        <span class="chart-views">${item.views || ''} views</span>
                    `;
                    chartResultsContainer.appendChild(rankItem);
                });

                // Show or hide "Show More" button
                if (data.has_more) {
                    showMoreButton.classList.remove("hidden");
                } else {
                    showMoreButton.classList.add("hidden");
                }
            })
            .catch((error) => {
                console.error("Error fetching chart data:", error);
            });
    }

    // Initial fetch
    fetchChartData();

    // Load more results
    showMoreButton.addEventListener("click", () => {
        currentPage++;
        fetchChartData(true);
    });

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

            currentPage = 1; // Reset to the first page
            updateFilterButtonText();
            filterDropdown.classList.add("hidden"); // Close dropdown
            fetchChartData(); // Fetch updated data
        }
    });
});