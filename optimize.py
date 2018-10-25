import kmeans
import processDAE
import numpy
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


path = "input.xml"

def getSSD(path):
    triangles = processDAE.getTriangles(path)
    normals = kmeans.computeNormals(triangles)

    possibleK = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ssdArr = [0,0,0,0,0,0,0,0,0,0]

    for k in range (len(possibleK)):
        numpy.random.seed(5)
        k_means = KMeans(n_clusters=possibleK[k], max_iter=400)
        k_means.fit(normals)
        centroids = k_means.cluster_centers_
        labels = k_means.labels_

        for x in range(len(normals)):
            clusterCenter = centroids[labels[x]]
            dist = ((normals[x][0] - clusterCenter[0])**2) + ((normals[x][1] - clusterCenter[0])**1) + ((normals[x][2] - clusterCenter[2])**2)
            ssdArr[k]+=dist
    return ssdArr

def plot(ssdArr):
    possibleK = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # plt.plot(possibleK, ssdArr)
    # plt.show()
    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])  # left, bottom, width, height (range 0 to 1)
    axes.plot(possibleK, ssdArr, 'r')

    axes.set_xlabel('K value')
    axes.set_ylabel('Sum Squared Error ')
    axes.set_title('SSE Plot');
    plt.show()

def run_optimization(path):
    ssd = getSSD(path)
    plot(ssd)


