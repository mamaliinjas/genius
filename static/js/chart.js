document.addEventListener('DOMContentLoaded', function () {
    const typeFilter = document.getElementById('type-filter');
    const genreFilter = document.getElementById('genre-filter');
    const timeFilter = document.getElementById('time-filter');
    const chartResults = document.getElementById('chart-results');
    const chartCanvas = document.getElementById('chart');
    let chartInstance = null; // Store the Chart.js instance

    function fetchFilteredResults() {
        const type = typeFilter.value;
        const genre = genreFilter.value;
        const time = timeFilter.value;

        fetch(`/filter_views/?type=${type}&genre=${genre}&time=${time}`)
            .then(response => response.json())
            .then(data => {
                chartResults.innerHTML = ''; // Clear previous results

                if (data.results.length > 0) {
                    const resultList = document.createElement('ul');
                    data.results.forEach(item => {
                        const li = document.createElement('li');
                        if (type === 'song') {
                            li.innerHTML = `<img src="${item.image}" alt="${item.title}" style="width: 50px; height: 50px;"/> <a href='/song/${item.id}/'>${item.title} by ${item.artist}</a> - ${item.views} views`;
                        } else if (type === 'album') {
                            li.innerHTML = `<img src="${item.image}" alt="${item.title}" style="width: 50px; height: 50px;"/> <a href='/album/${item.id}/'>${item.title} by ${item.artist}</a> - ${item.views} views`;
                        } else if (type === 'artist') {
                            li.innerHTML = `<img src="${item.image}" alt="${item.name}" style="width: 50px; height: 50px;"/> <a href='/artist/${item.id}/'>${item.name}</a> - ${item.views} views`;
                        }
                        resultList.appendChild(li);
                    });
                    chartResults.appendChild(resultList);
                } else {
                    chartResults.innerHTML = '<p>No results found</p>';
                }

                // Render chart
                renderChart(data.chart_data.labels, data.chart_data.values, data.chart_data.images, type);
            })
            .catch(error => console.error('Error:', error));
    }

    function renderChart(labels, values, images, type) {
        if (chartInstance) {
            chartInstance.destroy(); // Destroy the old chart if it exists
        }

        chartInstance = new Chart(chartCanvas, {
            type: 'bar',
            data: {
                labels: labels, // Song/Album/Artist names
                datasets: [{
                    label: `Top ${type}s by Views`,
                    data: values, // View counts
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                }],
            },
            options: {
                indexAxis: 'y', // Make the bars horizontal
                responsive: true,
                scales: {
                    x: {
                        beginAtZero: true,
                    },
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            title: function (tooltipItem) {
                                const index = tooltipItem[0].dataIndex;
                                const label = labels[index];
                                const artist = images[index] ? `<img src="${images[index]}" alt="${label}" style="width: 20px; height: 20px;"/>` : '';
                                return `${label} ${artist}`;
                            },
                        },
                    },
                },
            },
        });
    }

    // Add event listeners to filters
    [typeFilter, genreFilter, timeFilter].forEach(filter =>
        filter.addEventListener('change', fetchFilteredResults)
    );

    // Initial fetch
    fetchFilteredResults();
});