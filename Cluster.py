import pyface.qt
import kmeans
import processDAE
import processOBJ
import optimize
import plot

path = "res/Tile_+005_+001.xml"

opt = raw_input("find optimal k value using sum of squared errors? (y/n)")
if opt == "y":
    optimize.run_optimization(path)

k=int(input("K value?"))

triangles = processDAE.getTriangles(path)
clusters = kmeans.runProcessing(triangles, k)
mesh = plot.plt(path, clusters)
#texcoords = kmeans.getTextureCoords(k)
#processDAE.reWriteTexCoords(path, texcoords, clusters)



