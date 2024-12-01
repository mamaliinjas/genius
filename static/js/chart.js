document.addEventListener('DOMContentLoaded', function () {
    const chartResultsContainer = document.getElementById('chart-results');
    const filterForm = document.getElementById('filter-form');

    function fetchChartData() {
        const type = document.getElementById('type-filter').value;
        const genre = document.getElementById('genre-filter').value;
        const time = document.getElementById('time-filter').value;

        fetch(`/chart_data/?type=${type}&genre=${genre}&time=${time}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Error fetching chart data:', data.error);
                    return;
                }

                chartResultsContainer.innerHTML = ''; // Clear previous results

                data.results.forEach((item, index) => {
                    const rankItem = document.createElement('div');
                    rankItem.classList.add('chart-item');

                    // Set the correct page redirection based on item type
                    if (type === "song") {
                        rankItem.onclick = () => window.location.href = `/song/${item.id}/`;
                    } else if (type === "album") {
                        rankItem.onclick = () => window.location.href = `/album/${item.id}/`;
                    } else if (type === "artist") {
                        rankItem.onclick = () => window.location.href = `/artist/${item.id}/`;
                    }

                    // Only include the "(lyrics)" label if the filter type is "song"
                    const lyricsLabel = type === "song" ? `<span class="chart-lyrics-label">LYRICS</span>` : "";

                    // Only include the views if the filter type is "song"
                    const viewsHtml = type === "song" ? `<span class="chart-views">${item.views} views</span>` : "";

                    // If the filter type is "artist", apply bold font for artist names
                    let itemHtml = "";
                    if (type === "artist") {
                        itemHtml = `
                            <span class="chart-rank">${index + 1}</span>
                            <img class="chart-image" src="${item.image || '/static/images/default_cover.jpg'}" alt="cover photo">
                            <span class="chart-artist chart-artist-bold">${item.name}</span>
                        `;
                    } else {
                        itemHtml = `
                            <span class="chart-rank">${index + 1}</span>
                            <img class="chart-image" src="${item.image || '/static/images/default_cover.jpg'}" alt="cover photo">
                            <span class="chart-song">
                                ${item.title}
                                ${lyricsLabel}
                            </span>
                            <span class="chart-artist">${item.artist}</span>
                            ${viewsHtml}
                        `;
                    }

                    rankItem.innerHTML = itemHtml;
                    chartResultsContainer.appendChild(rankItem);
                });
            })
            .catch(error => {
                console.error('Error fetching chart data:', error);
            });
    }

    filterForm.addEventListener('change', fetchChartData);
    fetchChartData(); // Initial fetch on page load
});