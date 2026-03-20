let chartInstance = null;

document.getElementById('go-button').addEventListener('click', async () => {
    const textInput = document.getElementById('text-input').value;
    
    if (!textInput.trim()) {
        alert('Please enter some text to analyze.');
        return;
    }

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: textInput })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Output the Kevin Index string
        document.getElementById('kevin-index-display').innerText = `Your Kevin Index is: ${data.index}`;

        // Render the bar chart with the list of numbers
        renderChart(data.stats);
        
    } catch (error) {
        console.error('Error fetching data:', error);
        alert('Failed to calculate Kevin Index. Check the console for details.');
    }
});

function renderChart(statsList) {
    const ctx = document.getElementById('statsChart').getContext('2d');
    
    // If we've already generated a chart before, destroy it so we don't overlap
    if (chartInstance) {
        chartInstance.destroy();
    }

    // Dynamically create generic labels for each returned number [Stat 1, Stat 2...]
    const labels = statsList.map((_, i) => `Stat ${i + 1}`);

    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Grammar Measure Statistics',
                data: statsList,
                backgroundColor: '#3498db',
                borderColor: '#2980b9',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}
