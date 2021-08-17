 function setChart(data, ctx){

    var myChart =  new Chart(ctx, {
        type: 'scatter',
        data: {
            labels: [],  //labels
            datasets: data //data come in [ ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                },
              x:{
                  type: 'time',
                  time: {
                    // unit: 'hour',
                    displayFormats: {
                        hour: 'H a Do'
                    }
                  },
              }
            }
        }
    });
    return myChart
}
