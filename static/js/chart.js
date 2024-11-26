document.addEventListener('DOMContentLoaded', function () {
    // Get filter form elements
    const typeFilter = document.getElementById('type-filter');
    const genreFilter = document.getElementById('genre-filter');
    const timeFilter = document.getElementById('time-filter');
    const chartResultsContainer = document.getElementById('chart-results');

    // Check if elements exist
    if (!typeFilter || !genreFilter || !timeFilter || !chartResultsContainer) {
        console.error('Missing required DOM elements (filters or chart results container)');
        return;
    }

    // Function to fetch and display chart data based on selected filters
    function fetchChartData() {
        const type = typeFilter.value;  // Get selected type (song, album, artist)
        const genre = genreFilter.value;  // Get selected genre
        const time = timeFilter.value;  // Get selected time range

        // Fetch chart data from the backend based on selected filters
        fetch(`/chart_data/?type=${type}&genre=${genre}&time=${time}`)
            .then(response => response.json())
            .then(data => {
                // Check for errors
                if (data.error) {
                    console.error('Error fetching chart data:', data.error);
                    return;
                }

                // Clear previous results
                chartResultsContainer.innerHTML = '';

                // Loop through the chart data and display results
                data.chart_data.labels.forEach((label, index) => {
                    const rankItem = document.createElement('div');
                    rankItem.classList.add('chart-item');

                    rankItem.innerHTML = `
                        <div class="chart-item-content">
                            <span class="chart-rank">${index + 1}</span>
                            <span class="chart-title">${label}</span>
                            <span class="chart-artist">${data.results[index].artist}</span>
                            <span class="chart-views">${data.results[index].views} views</span>
                        </div>
                        ${data.chart_data.images[index] ? `<img class="chart-image" src="${data.chart_data.images[index]}" alt="cover photo">` : ''}
                    `;

                    chartResultsContainer.appendChild(rankItem);
                });
            })
            .catch(error => {
                console.error('Error fetching chart data:', error);
            });
    }

    // Add event listeners for filter changes to re-fetch chart data
    typeFilter.addEventListener('change', fetchChartData);
    genreFilter.addEventListener('change', fetchChartData);
    timeFilter.addEventListener('change', fetchChartData);

    // Initial fetch on page load
    fetchChartData();
});