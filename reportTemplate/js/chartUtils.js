function drawSeverityChart(infoStat, lowStat, mediumStat, highStat, criticalStat){
    const data = {
        labels: [
          'Info',
          'Low',
          'Medium',
          'High',
          'Critical',
        ],
        datasets: [{
          label: '',
          data: [infoStat, lowStat, mediumStat, highStat, criticalStat],
          backgroundColor: [
            'grey',
            'green',
            'yellow',
            'orange',
            'red',
          ],
          hoverOffset: 4
        }]
    };
    
    const options = {
        plugins: {
            title: {
                display: true,
                text: 'Severity Assessment',
                align: 'center',
                position: 'bottom',
                font: {
                    size: 26
                },
            },
            legend:{
                display: false
            }
        }
    
    }
    
    const config = {
        type: 'bar',
        data: data,
        options: options
    };
    
    
    const myChart = new Chart(
    document.getElementById("myChart"), config
    );
    
}


