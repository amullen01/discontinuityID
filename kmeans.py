import numpy
import math
from sklearn.cluster import KMeans

#subtracts two 3D vectors
#inputs: two vectors in format [x, y, z]
#outputs: subtracted vector in [x, y, z]
def vectorSubtract(v1, v2):
    subtracted = []
    for i in range(0, 3):
        subtracted.append(v1[i] - v2[i])
    return subtracted

#computes normals to triangles in triangle arra
#input: 3D triangle array in format [[[x0, y0, z0], [x1, y1, z1], [x2, y2, z2]], ..., ...]
#outputs: 2D array of normal vectors to each triangle
def computeNormals(triangles):
    normals = []
    for triangle in triangles:
        u = vectorSubtract(triangle[1], triangle[0])

        v = vectorSubtract(triangle[2], triangle[0])

        normals.append(numpy.cross(u, v))
    return normals

def angleBetweenVectors(v1, v2):
    if (v1 == v2).all():
        return 0
    dot = (v1[0]*v2[0])+(v1[1]*v2[1])+(v1[2]*v2[2])

    mag = math.sqrt((v1[0]**2)+(v1[1]**2)+(v1[2]**2))*math.sqrt((v2[0]**2)+(v2[1]**2)+(v2[2]**2))

    return math.acos(dot/mag)

#runs kmeans clustering on normal vectors
#inputs: normal vector array, value of k clusters
#outputs: array corresponding to normal vector array of the cluster that normal vector belongs to
def clusterNormals(normals, k):
    angles = numpy.array([[angleBetweenVectors([0, 0, 0], normal)] for normal in normals])

    for x in range(len(angles)):
        if not numpy.isfinite(angles[x]):
            angles[x] = 0
    numpy.random.seed(5)

    kmeans = KMeans(n_clusters=k, max_iter=300)
    kmeans.fit(angles)
    labels = kmeans.labels_
    return labels



#generates texture coordinate array based on k value and output.png texture map
#input: k value
#output: texcoord array
def getTextureCoords(numK):
    #one square = 0.33203125 X 0.33203125
    #center of sqaure 1 = 0.166015625, 0.166015625
    colors = []
    x=0
    while x < numK:
        for j in range(0,3):
            for i in range(0,3):
                colors.append([(i+1)*0.33203125-0.166015625, (j+1)*0.33203125-0.166015625])
                x+=1
                if (x >= numK):
                    break
            if (x >= numK):
                break
    return colors

def kmeansDot(normals, k, iterations):
    labels = []
    # initial centroids
    centroids = [normals[numpy.random.randint(0, len(normals))] for i in range(0, k)];
    for it in range(0, iterations):
        #create array for assigning data to clusters
        data_clustered = [[] for q in range (0,k)]

        #assign points to nearest cluster
        for normal in normals:
            minAngle = 1000000000
            cluster = 0
            for x in range(0, k):
                angle = angleBetweenVectors(centroids[x], normal)
                if angle<minAngle:
                    minAngle = angle
                    cluster = x
            labels.append(cluster)
            data_clustered[cluster].append(normal)

        #mean of each cluster
        means = [[] for q in range (0,k)]

        #calculate means
        for j in range(0,k):
            mean_x = numpy.mean([w[0] for w in data_clustered[j]])
            mean_y = numpy.mean([w[1] for w in data_clustered[j]])
            mean_z = numpy.mean([w[2] for w in data_clustered[j]])
            means[j]=[mean_x, mean_y, mean_z]
        # check tolerance
        diff = 0
        for p in range(0, k):
            diff+=angleBetweenVectors(numpy.array(means[p]), centroids[p])
        if diff==0:
            print "converged on iteration ", it
            break
        else:
            centroids = means



    return labels

#shell function
def runProcessing(triangles, k):
    normals = computeNormals(triangles)
    #clusters = clusterNormals(normals, k)
    clusters = kmeansDot(normals, k, 10)
    return clusters