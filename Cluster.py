import pyface.qt
import kmeans
import processDAE
import processOBJ
import optimize
import plot
import numpy

#path = "res/Tile_+005_+001.xml"
path = "res/cube.xml"


print "processing data"
data = processDAE.processTiles('res/inputCollada/')
print len(data['triangleMap']), " triangles"

k=int(input("K value?"))
print "kmeans clustering"
clusters = kmeans.kmeansDot(data['normals'], k, 6, 3)

print "plotting"
mesh = plot.plt(data['vertices'], data['triangleMap'], clusters)

# vertices = processDAE.getVertices(path)
# triangles = processDAE.getTriangles(path)
# triangleMap = processDAE.getTriangleMap(path)
# clusters = kmeans.runProcessing(triangles, k)
# print len(triangleMap)
# print len(vertices)
# mesh = plot.plt(vertices, triangleMap, clusters)
#texcoords = kmeans.getTextureCoords(k)
#processDAE.reWriteTexCoords(path, texcoords, clusters)



