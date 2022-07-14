function drawSeverityChart(infoStat, lowStat, mediumStat, highStat){
    const data = {
        labels: [
          'Info',
          'Low',
          'Medium',
          'High'
        ],
        datasets: [{
          label: '',
          data: [infoStat, lowStat, mediumStat, highStat],
          backgroundColor: [
            'grey',
            'blue',
            'orange',
            'red'
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


