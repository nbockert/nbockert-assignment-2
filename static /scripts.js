

var isManual = false;
var selectedCentroids = [];
var k = 0;
var stepnum = 0;
var press = false;
var snapshots = []; 
var method = '';

// Function to send selected centroids to the backend
function displayMessage(message) {
    document.getElementById('output').innerText = message;
}

// Event listener for button click
let clusterPlot = document.getElementById('clusterPlot');
    clusterPlot.on('plotly_click', function(data) {
    // Call the Flask endpoint

});
function sendCentroid(x, y) {
    fetch('/add_centroid', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ x: x, y: y })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            updatePlot(data.image_url);
        }
    });
}

// Plot initial data and allow interaction
function plotData(dataX, dataY,data) {
    k = parseInt(document.getElementById("num_clusters").value);
    let trace = {
        x: dataX,
        y: dataY,
        mode: 'markers',
        type: 'scatter',
        marker: { color: 'blue' }
    };
    let centroidTrace = {
        x: selectedCentroids.map(c => c[0]),
        y: selectedCentroids.map(c => c[1]),
        mode: 'markers',
        type: 'scatter',
        marker: { color: 'red', symbol: 'x', size: 12 }
    };

  
    let layout = {
        title: 'Select Initial Centroids by Clicking',
        clickmode: 'event+select'
    };

    Plotly.newPlot('clusterPlot', [trace, centroidTrace], layout);
    // while(count<=k){
    let clusterPlot = document.getElementById('clusterPlot');
    clusterPlot.on('plotly_click', function(data) {
        let x = data.points[0].x;
        let y = data.points[0].y;
        selectedCentroids.push([x, y]);

        updateCentroidPlot(dataX, dataY);

     
    });
}

// Function to update the plot with selected centroids
function updateCentroidPlot(dataX, dataY) {
    // print("selected centroids:", selectedCentroids)
    // Clear the existing plot
    Plotly.purge('clusterPlot');


    let trace = {
        x: dataX,
        y: dataY,
        mode: 'markers',
        type: 'scatter',
        marker: { color: 'blue' }
    };
    // selectedCentroids.map(c => c[0])
    let centroidTrace = {
        x: selectedCentroids.map(c => c[0]),
        y: selectedCentroids.map(c => c[1]),
        mode: 'markers',
        type: 'scatter',
        marker: { color: 'red', symbol: 'x', size: 12 }
    };

    Plotly.newPlot('clusterPlot', [trace, centroidTrace], {
        title: 'Select Initial Centroids by Clicking',
        clickmode: 'event+select'
    });
    sendCentroids(selectedCentroids.map(c => c[0]),selectedCentroids.map(c => c[1])); 
}

// Function to update the plot with the selected centroids
function updatePlot(imageUrl) {
    let snapshotDiv = document.getElementById("clusterPlot");
    snapshotDiv.innerHTML = '';  // Clear previous snapshots
    let img = document.createElement('img');
    img.src = imageUrl;
}

// When the user selects "Manual"
function onInitMethodChange() {
    let snapshotDiv = document.getElementById("clusterPlot");
    snapshotDiv.innerHTML = ''; 
    k = parseInt(document.getElementById("num_clusters").value);
    let method = document.getElementById('init_method').value;
    if (method === 'manual') {
 // Clear previous snapshots
        isManual = true;
        fetch('/get_data')
            .then(response => response.json())
            .then(data => {
                plotData(data.dataX, data.dataY,data);
            });
    } else {
        isManual = false;
    //     fetch('/start_clustering', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify({
    //             num_clusters: k,
    //             init_method: method
    //         })
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data);  // Use this to debug
    //         if (data) {
    //             let snapshotDiv = document.getElementById("clusterPlot");
    //             // snapshotDiv.innerHTML = '';
    //             let img = document.createElement('img');
    //             img.src = `${data.snap_file}`;  
    //             // img.style.width = '300px';  
    //             snapshotDiv.appendChild(img);


    //         } else if (data.error) {
    //             console.error(data.error);
    //         }
    //     })
    //     .catch(error => console.error('Error:', error));
    // }
}
}

function StepThrough(){
    let method = document.getElementById('init_method').value;

    if(press===false){
        onInitMethodChange()
        fetch('/steps', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                num_clusters: k,
                init_method: method
            })
        })
        .then(response => response.json())
        .then(data => {
            snapshots = data.graphs;
            displaySnapshots(stepnum);
            press=true;
            stepnum++;
        })
        
    }else{
        if (stepnum < snapshots.length) {
            displaySnapshots(stepnum)
            stepnum++;
        } else {
            alert("KMeans has converged");
        }
}
}
function displaySnapshots(stepIndex) {
    let snapshotDiv = document.getElementById("clusterPlot");
    snapshotDiv.innerHTML = '';  // Clear previous snapshots
    let img = document.createElement('img');
    img.src = `/static/${snapshots[stepIndex]}`;  // Use the current snapshot
    img.alt = `Snapshot ${stepIndex}`;
    snapshotDiv.appendChild(img);
    
}

function Regenerate(){
    let snapshotDiv = document.getElementById("clusterPlot");
    snapshotDiv.innerHTML = ''; 
    fetch('/regenerate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        isManual = false;
        selectedCentroids = [];
        k = 0;
        stepnum = 0;
        press = false;
        snapshots = []; 
        let img = document.createElement('img');
        img.src = `/static/${data.new_snap}`;  // Use the current snapshot from Flask
        img.style.width = '500px';  // You can adjust the width if needed
        snapshotDiv.appendChild(img);
        
    })
    .catch(error => console.error('Error:', error));
}

function Convergence(){
    k = parseInt(document.getElementById("num_clusters").value);
    let method = document.getElementById('init_method').value;
    fetch('/converge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            num_clusters: k,
            init_method: method
        })
    })
        .then(response => response.json())
        .then(data => {
            let snapshotDiv = document.getElementById("clusterPlot");
            snapshotDiv.innerHTML = '';  // Clear previous snapshots
            let img = document.createElement('img');
            img.src = `/static/${data.snap_file}`;  // Use the current snapshot
            snapshotDiv.appendChild(img);
        })
        .catch(error => console.error('Error:', error));

}
