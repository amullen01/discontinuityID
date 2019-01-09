import pyface.qt
import kmeans
import processDAE
import plot



print "processing data"
data = processDAE.processTiles('res/inputCollada/')
print len(data['triangleMap']), " triangles"

k=int(input("K value?"))
print "kmeans clustering"
clusters = kmeans.kmeansDot(data['normals'], k, 5, 3)

print "plotting"

mesh = plot.colored_model(data['vertices'], data['triangleMap'], clusters['all_labels'])
plot.plot_stereonet(data['normals'], clusters['centers'])





