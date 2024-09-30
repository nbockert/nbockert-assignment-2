import numpy as np
from PIL import Image as im
import matplotlib.pyplot as plt
import sklearn.datasets as datasets
import os

class KMeans():

    def __init__(self, data, k):
        self.data = data
        self.k = k
        self.assignment = [-1 for _ in range(len(data))]
        self.snaps = []
        self.centroids = []
    
    def snap(self, centers):
        print("at snap")
        filename = f"snapshot_{len(self.snaps)}.png"
        filepath = os.path.join("static", filename)
        fig, ax = plt.subplots()
        ax.scatter(self.data[:, 0], self.data[:, 1], c=self.assignment)
        for center in centers:
            ax.scatter(center[0], center[1], c='r')
        fig.savefig(filepath)
        plt.close()
        self.snaps.append(filename)
        # self.snaps.append(im.fromarray(np.asarray(im.open(TEMPFILE))))

    
    def lloyds(self,init_method,centroids):
        print(init_method)
        if init_method == 'manual':
            self.centroids = centroids
            self.snap(centroids)
            self.make_clusters(self.centroids)
        else:
            self.centroids = self.initialize(init_method)
            self.make_clusters(self.centroids)
            self.snap(self.centroids)
        # self.snap(centers)
            print("made clusters")
        new_centers = self.compute_centers()
        print("got new centers")
        self.snap(new_centers)
        print("snap of new centers")
        while self.are_diff(self.centroids, new_centers):
            self.unassign()
            self.centroids = new_centers
            self.make_clusters(self.centroids)
            new_centers = self.compute_centers()
            self.snap(new_centers)
        return self.snaps
    
    def initialize(self, method):
        if method == 'random':
            return self.random_initialization()
        elif method == 'farthest_first':
            return self.farthest_first_initialization()
        elif method == 'kmeans++':
            return self.kmeans_plus_plus_initialization()

        
    # def manual_init(self):
    #     # Set up the plot for manual centroid selection
    #     fig, ax = plt.subplots()
    #     ax.scatter(self.data[:, 0], self.data[:, 1])
    #     plt.title("Click to select initial centroids")

    #     # Connect mouse click event to function
    #     cid = fig.canvas.mpl_connect('button_press_event', self.on_click)
    #     plt.show()

    #     # Wait until the user has selected the centroids
    #     while len(self.manual_centroids) < self.k:
    #         plt.pause(0.1)

    #     return np.array(self.manual_centroids)

    # def on_click(self, event):
    #     # Handle the mouse click
    #     if event.button == MouseButton.LEFT:
    #         x, y = event.xdata, event.ydata
    #         if len(self.manual_centroids) < self.k:
    #             self.manual_centroids.append([x, y])
    #             print(f"Centroid {len(self.manual_centroids)}: ({x}, {y})")
    #             # Update plot with the selected centroid
    #             plt.scatter(x, y, c='r', marker='X')
    #             plt.draw()

    def random_initialization(self):
        # centroids = self.data[np.random.choice(len(self.data), size=self.k, replace=False)]
        # print("Randomly initialized centroids:", centroids)
        # return centroids
        indices = self.data[np.random.choice(len(self.data), size=self.k, replace=False)]
        return indices
    
    def farthest_first_initialization(self):
        centers = [self.data[np.random.randint(len(self.data))]]  # Choose the first center randomly
        for _ in range(1, self.k):
            dist = np.array([min([self.dist(x, center) for center in centers]) for x in self.data])
            new_center = self.data[np.argmax(dist)]  # Choose the farthest point
            centers.append(new_center)
        return np.array(centers)
    
    def kmeans_plus_plus_initialization(self):
        print("in kmeans++")
        centers = [self.data[np.random.randint(len(self.data))]]  # Choose the first center randomly
        print("got new centers")
        for _ in range(1, self.k):
            dist = np.array([min([self.dist(x, center) for center in centers]) for x in self.data])
            probs = dist / dist.sum()  # Probability based on distance
            new_center = self.data[np.random.choice(len(self.data), p=probs)]
            centers.append(new_center)
        return np.array(centers)

    def make_clusters(self, centers):
        for i in range(len(self.assignment)):
            distances = [self.dist(self.data[i], center) for center in centers]
            self.assignment[i] = np.argmin(distances)

    def compute_centers(self):
        centers=[]
        #number of clusters we want 
        for i in range(self.k):
            cluster=[]
            #look at the assignments 
            for j in range(len(self.assignment)):
                #are you part of cluster i 
                if self.assignment[j] == i:
                    #add to cluster
                    cluster.append(self.data[j])
            #take mean of cluster

            cluster = np.array(cluster)
            mean_center = np.mean(cluster, axis=0)  # Mean along each column (x, y)
            centers.append(mean_center)
            print(mean_center)
            # centers.append(np.mean(np.array(cluster)))
        return np.array(centers)
    
    def unassign(self):
        self.assignment = [-1 for _ in range(len(self.data))]
    
    def are_diff(self,centers,new_centers):
        for i in range(self.k):
            if self.dist(centers[i],new_centers[i]) != 0:
                #if distances between centers is 0 then they are not dif
                 return True
        return False
        
    def is_unassigned(self,i):
        self.assignments[i] == -1

    def dist(self, x, y):
        return np.linalg.norm(x - y) 

# Example usage


# if __name__ == "__main__":
#     centers = [[0, 0], [2, 2], [-3, 2], [2, -4]]
#     X, _ = datasets.make_blobs(n_samples=300, centers=centers, cluster_std=1, random_state=0)
#     centroids = []
#     kmeans = KMeans(X, 4)
#     kmeans.lloyds('random',centroids)  # Example with KMeans++ initialization
    # images = kmeans.snaps

    # images[0].save(
    #     'kmeans.gif',
    #     optimize=False,
    #     save_all=True,
    #     append_images=images[1:],
    #     loop=0,
    #     duration=500
    # )