from flask import Flask, render_template, request, jsonify, send_file
from kmeans_init_methods import KMeans  # Import your KMeans class
import numpy as np
import sklearn.datasets as datasets
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import glob
import random

app = Flask(__name__)

# Global variables for centroids and KMeans object
graphs = []
kmeans = None
centroids = []




@app.route('/')
def index():
    global centers
    global X
    centers = [[0, 0], [2, 2], [-3, 2], [2, -4]]
    random_seed = random.randint(0, 10000)
    X, _ = datasets.make_blobs(n_samples=300, centers=centers, cluster_std=1,random_state=random_seed)
    TEMPFILE = "static/snapinit.png" 
    fig, ax = plt.subplots()
    print("made it here")
    ax.scatter(X[:, 0], X[:, 1])
    ax.set_title("Data Points")
    fig.savefig(TEMPFILE)
    plt.close()
    return render_template('index.html', snap_init="snapinit.png")


# Route to return data for Plotly.js plot
@app.route('/get_data', methods=['GET'])
def get_data():
    print("at get data")
    dataX = X[:, 0].tolist()
    dataY = X[:, 1].tolist()
    return jsonify({'dataX': dataX, 'dataY': dataY})

#for printing last one that matters 
# @app.route('/start_clustering', methods=['POST'])
# def start_clustering():
#     global kmeans
#     global graphs
#     init_method = request.json.get('init_method')
#     k = request.json.get("num_clusters")
#     kmeans = KMeans(X, k)
#     graphs = kmeans.lloyds(init_method,centroids)
#     return jsonify(graphs)
#     # last_snapshot = graphs[-1] if graphs else None
#     # if last_snapshot:
#     #     return jsonify({"snap_file": last_snapshot})
#     # else:
#     #     return jsonify({"error": "No snapshots generated"}), 500

@app.route('/add_centroids', methods=['POST'])
def add_centroids():
    print("at add centroid")
    k = request.json.get("num_clusters")
    global centroids, kmeans
    
    data = request.json
    centroids.append([data['x'],data['y']])

    # If you have `k` as a global variable or passed from the frontend
    if len(centroids) == k:  # Ensure `k` is defined globally or passed
        kmeans = KMeans(X, k)
        kmeans.lloyds('manual', centroids)

        # Send back the final cluster image
        image_path = update_plot_with_clusters(kmeans.centers)
        return jsonify({'status': 'done', 'image_url': image_path})

    # Otherwise, continue the process of selecting centroids
    return jsonify({'status': 'ok'})
    
#create one that color codes assignments too
def update_plot_with_clusters(centroids):
    TEMPFILE = "final_clusters_plot.png"
    fig, ax = plt.subplots()
    ax.scatter(X[:, 0], X[:, 1])
    for center in centroids:
        ax.scatter(center[0], center[1], c='g', marker='X')
    fig.savefig(TEMPFILE)
    plt.close()
    return TEMPFILE

@app.route('/steps', methods=['POST'])
def steps():
    global kmeans
    global graphs
    init_method = request.json.get('init_method')
    k = request.json.get("num_clusters")
    kmeans = KMeans(X, k)
    graphs = kmeans.lloyds(init_method,centroids)
    return jsonify({"graphs":graphs})
    
    # Send the centroids snapshots to the frontend

@app.route('/regenerate', methods=['POST'])
def regenerate():
    global kmeans
    global graphs
    global centroids
    graphs = []
    kmeans = None
    centroids = []
    try:
        reset_snapshots()
        global centers
        global X
        centers = [[0, 0], [2, 2], [-3, 2], [2, -4]]
        random_seed = random.randint(0, 10000)
        X, _ = datasets.make_blobs(n_samples=300, centers=centers, cluster_std=1,random_state=random_seed)
        TEMPFILE = "static/snapinit1.png" 
        fig, ax = plt.subplots()
        print("made it here")
        ax.scatter(X[:, 0], X[:, 1])
        ax.set_title("Data Points")
        fig.savefig(TEMPFILE)
        plt.close()
        return jsonify({'new_snap':'snapinit1.png'})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/converge', methods=['POST'])
def converge():
    global kmeans
    global graphs
    global centroids 
    
    if kmeans==None:
        init_method = request.json.get('init_method')
        print(init_method)
        k = request.json.get("num_clusters")
        kmeans = KMeans(X, k)
        graphs = kmeans.lloyds(init_method,centroids)
        last_snapshot = graphs[-1] if graphs else None
        if last_snapshot:
            return jsonify({"snap_file": last_snapshot})
        else:
            return jsonify({"error": "No snapshots generated"}), 500
    else:
        last_snapshot = graphs[-1] if graphs else None
        if last_snapshot:
            return jsonify({"snap_file": last_snapshot})
        else:
            return jsonify({"error": "No snapshots generated"}), 500



    
def reset_snapshots():
    print("in reset snapshots")
    snapshot_pattern = os.path.join("static", "snapshot_*.png")
    snapshot_files = glob.glob(snapshot_pattern)
    for snapshot_file in snapshot_files:
        try:
            print(f"Deleted: {snapshot_file}")
        except Exception as e:
            print(f"Error deleting {snapshot_file}: {e}")





if __name__ == '__main__':
    app.run(port=5000, debug=True)