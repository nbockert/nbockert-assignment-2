import numpy as np
from PIL import Image as im
import matplotlib.pyplot as plt
import sklearn.datasets as datasets

# centers = [[0, 0], [2, 2], [-3, 2], [2, -4]]
# X, _ = datasets.make_blobs(n_samples=300, centers=centers, cluster_std=1, random_state=0)

class KMeans():

    def __init__(self, data, k):
        self.data = data
        self.k = k
        self.assignment = [-1 for _ in range(len(data))]
        self.snaps = []
    
    def snap(self, centers):
        TEMPFILE = "temp.png"
        fig, ax = plt.subplots()
        ax.scatter(self.data[:, 0], self.data[:, 1], c=self.assignment)
        ax.scatter(centers[:, 0], centers[:, 1], c='r')
        fig.savefig(TEMPFILE)
        plt.close()
        self.snaps.append(im.fromarray(np.asarray(im.open(TEMPFILE))))
    
    def lloyds(self, init_method):
        centers = self.initialize(init_method)
        print("init centers")
        self.make_clusters(centers)
        print("made clusters")
        new_centers = self.compute_centers()
        print("got new centers")
        self.snap(new_centers)
        print("snap of new centers")
        while self.are_diff(centers, new_centers):
            self.unassign()
            centers = new_centers
            self.make_clusters(centers)
            new_centers = self.compute_centers()
            self.snap(new_centers)
        return
    def initialize(self, method):
        if method == 'random':
            return self.random_initialization()
        elif method == 'farthest_first':
            return self.farthest_first_initialization()
        elif method == 'kmeans++':
            return self.kmeans_plus_plus_initialization()
        ##need to fix this so that the user can manually pick k centers
        elif method == 'manual':
            raise NotImplementedError("Manual initialization needs user input.")
        
    def random_initialization(self):
        return self.data[np.random.choice(len(self.data), size=self.k, replace=False)]

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
        print(np.array(centers))
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
            print(np.mean(np.array(cluster)),axis=0)
            centers.append(np.mean(np.array(cluster)),axis=0)
        return centers
    
    def unassign(self):
        self.assignment = [-1 for _ in range(len(self.data))]
    
    def are_diff(self,centers,new_centers):
        for i in range(self.k):
            if self.dist(centers[i],new_centers[i]) == 0:
                #if distances between centers is 0 then they are not dif
                 return True
    def is_unassigned(self,i):
        self.assignments[i] == -1

    def dist(self,x,y):
        return sum((x-y)**2)**(1/2)

# Example usage


if __name__ == "__main__":
    centers = [[0, 0], [2, 2], [-3, 2], [2, -4]]
    X, _ = datasets.make_blobs(n_samples=300, centers=centers, cluster_std=1, random_state=0)
    
    kmeans = KMeans(X, 4)
    kmeans.lloyds('kmeans++')  # Example with KMeans++ initialization
    images = kmeans.snaps

    images[0].save(
        'kmeans.gif',
        optimize=False,
        save_all=True,
        append_images=images[1:],
        loop=0,
        duration=500
    )