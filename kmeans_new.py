import random
import math
import scipy
import numpy as np

class Kmeans:

    clustering_data=None
    seed =0
    max_iterations = 0
    k=0
    runs = 5
    final_centers = None
    final_labels = None
    tolerance = 3
    ssd = 100000000
    data_clustered = []


    def __init__(self, data, max_iterations, k, tolerance, runs):
        self.clustering_data = data
        self.max_iterations = max_iterations
        self.k = k
        self.tolerance = tolerance
        self.runs = runs



    def run_kmeans(self):
        for run in range(0, self.runs):
            print "seeding initial centroids"

            centroids = self.choose_initial_centroids()

            k=self.k
            iterations = 0
            oldCentroids = None
            labels = None
            dataSet = self.clustering_data

            print "running kmeans"
            # Run the main k-means algorithm
            while not self.shouldStop(oldCentroids, centroids, iterations):
                # Save old centroids for convergence test. Book keeping.
                oldCentroids = centroids
                iterations += 1

                # Assign labels to each datapoint based on centroids
                labels = [self.get_closest_centroid(centroids, x) for x in dataSet]

                # Assign centroids based on datapoint labels
                centroids = self.update_centroids(dataSet, labels, k)
            self.return_best(self.data_clustered, centroids, labels)

            print "run ", run+1, " converged in", iterations, "iterations"
        return
    def return_best(self, data_clustered, centroids, labels):
        new_ssd = 0
        for d in data_clustered:
            new_ssd += np.std(d)
        if new_ssd<self.ssd:
            self.final_centers = centroids
            self.final_labels = labels
            self.ssd = new_ssd

    def update_centroids(self, dataset, labels, k):

        arr = [[] for i in range(0,k)]
        for j in range(len(labels)):
            arr[labels[j]].append(dataset[j])
        self.data_clustered = arr
        for a in range(0,k):
            arr[a] = np.mean(arr[a], axis = 0)
        return arr


    def get_closest_centroid(self, centroids, x):
        min_angle = 100000
        closest_centroid = 0
        for i in range(len(centroids)):
            angle = self.angleBetweenVectors(centroids[i], x)
            if angle<min_angle:
                min_angle = angle
                closest_centroid = i
        return closest_centroid


    def shouldStop(self, oldCentroids, centroids, iterations):
        if iterations == 0:
            return False
        if iterations > self.max_iterations:
            return True
        angles = [self.angleBetweenVectors(oldCentroids[x],centroids[x]) for x in range(len(centroids))]

        return np.mean(np.degrees(angles)) < self.tolerance



    def angleBetweenVectors(self, v1, v2):
        if (v1 == v2).all():
            return 0
        dot = (v1[0] * v2[0]) + (v1[1] * v2[1]) + (v1[2] * v2[2])
        mag = math.sqrt((v1[0] ** 2) + (v1[1] ** 2) + (v1[2] ** 2)) * math.sqrt(
            (v2[0] ** 2) + (v2[1] ** 2) + (v2[2] ** 2))
        if math.isnan(math.acos(dot / mag)):
            return 0
        return math.acos(dot / mag)

    #kmeans++ selection of initial centroids
    def choose_initial_centroids(self):
        centroids = [random.choice(self.clustering_data)]
        for i in range(1,self.k):
            D2 = scipy.array([min(self.angleBetweenVectors(d,c)**2 for c in centroids) for d in self.clustering_data])
            probs = D2 / D2.sum()
            cumprobs = probs.cumsum()
            r = scipy.rand()
            for j, p in enumerate(cumprobs):
                if r < p:
                    i = j
                    break
            centroids.append(self.clustering_data[i])
        return centroids

    def choice(self, p):
        '''
        Generates a random sample from [0, len(p)),
        where p[i] is the probability associated with i.
        '''
        random = np.random.random()
        r = 0.0
        for idx in range(len(p)):
            r = r + p[idx]
            if r > random:
                return idx
        assert (False)

    def get_clustering_centers(self):
        return self.final_centers

    def get_labels(self):
        return self.final_labels
