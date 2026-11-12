function Graph(graphLab, graphVal) {
    console.log("Data received:", graphLab); 
    
    console.log("Data received:", graphVal); 
    console.log(data);
    const graphData = {
        labels:graphLab,
        datasets: [{
            label: 'Percentages',
            data: graphVal,
            backgroundColor: 'rgba(54, 162, 235, 0.4)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    };
    const config = {
        type: 'bar',
        orientation: 'h',
        data: graphData,
        options: {
            indexAxis: 'y',
            scales: {
                x: {
                    ticks: {
                        font: {
                            size: 15,
                            family: 'Arial',
                        },
                        color: 'black'
                    }
                },
                y: {
                    ticks: {
                        font: {
                            size: 15,
                            family: 'Arial',
                        },
                        color: 'black'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        font: {
                            size: 15
                        }
                    }
                }
            }
        }
    };
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, config);
}

document.addEventListener('DOMContentLoaded', function() {
    Graph('{{ data.graphLab | tojson | safe | escape }}', '{{ data.graphVal | tojson | safe }}');

});