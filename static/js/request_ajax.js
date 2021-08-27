var charts_list = []
document.body.addEventListener('click', function (event) {
    if (event.target.className === 'form-check-input dataset') {
        const form = event.target.form;
        const data = new FormData(form);

        const request = new XMLHttpRequest();
        request.responseType = 'json';

        request.open(form.method, form.action, true);

        if (document.getElementById("spinner--loading")){
            document.getElementById("spinner--loading").className = "d-flex";
        }

        request.send(data);


        request.addEventListener("load", function () {
            if (this.readyState === 4 && this.status === 200) {

                // catch JsonResponse from Django
                // const response = JSON.parse(this.responseText); // double check
                var resp = this.response;
                // console.log(resp)

                // load content
                // const element = document.getElementById("graphs-content");
                // const section = element.parentNode;
                // section.removeChild(element);
                // // section.innerHTML = response.all_series;

                var data_series = resp.all_series;
                // console.log(data_series)


                const datasets = []
                for (var key of Object.keys(data_series)) {
                    // console.log(key + " -> " + data_series[key].name)
                    //here create datasetes
                    datasets.push(
                        {
                            label: data_series[key].name,
                            data: data_series[key].data,
                            backgroundColor: data_series[key].color,
                            borderColor: data_series[key].color,
                            borderWidth: 1
                        })
                    //do list of canvas names here, pull up ctx_list definition
                    // ctx_list.push(document.getElementById('myChart1'))
                    //
                }

                console.log(charts_list)
                //destroy canvas if exists
                for (let i=0; i < charts_list.length; i++){
                        charts_list[i].destroy()
                        console.log("destroying")
                    }
                charts_list = []
                console.log(charts_list)


                //plot one graph with many
                async function create_graphs() {
                    var ctx = document.getElementById('myChart')
                    var mychart = setChart(datasets, ctx)
                    charts_list.push(mychart)

                    var canvas_name = ['myChart1', 'myChart2', 'myChart3', 'myChart4']
                    var ctx_list = [document.getElementById('myChart1'), document.getElementById('myChart2'),
                        document.getElementById('myChart3'), document.getElementById('myChart4')]


                    //
                    // var mychart = null;

                    for (let i = 0; i < datasets.length; i++) { //plot many graphs
                        // console.log(document.getElementById(canvas_name[i]))
                        //create canvas
                        // if(mychart!=null){
                        //    mychart.destroy();
                        // }

                        let ctx = document.getElementById(canvas_name[i]);
                        var mychart = setChart([datasets[i]], ctx)
                        console.log(mychart)
                        charts_list.push(mychart)
                        console.log(charts_list)
                        // console.log(document.getElementById(canvas_name[i]))
                    }
                }

                async function remove_spinner(){
                    await create_graphs();
                    document.getElementById("spinner--loading").className = "d-none";
                }

                remove_spinner()

            } else {
                // We reached our target server, but it returned an error
            }

        });

    }


});

    // Simulate a click on radio-button so that the data are load
var hatEvalData = document.getElementById("dataset_hum");
hatEvalData.click();
console.log("hatEvalData")
