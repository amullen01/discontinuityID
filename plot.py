import pyface.qt
import processDAE
from mayavi.mlab import *
from xml.etree import ElementTree as ET


#plots triangular mesh using clusters as scalar for shading
#inputs: path to xml collada file, clusters array generated by kmeans
#outputs: shaded 3d model
def plt(path, clusters):
    vertices = processDAE.getVertices(path)
    x = [vertices[i][0] for i in range(0, len(vertices))]
    y = [vertices[i][1] for i in range(0, len(vertices))]
    z = [vertices[i][2] for i in range(0, len(vertices))]


    xml = ET.parse(path)
    root = xml.getroot()
    tri = root.find("{http://www.collada.org/2005/11/COLLADASchema}library_geometries/{http://www.collada.org/2005/11/COLLADASchema}geometry/{http://www.collada.org/2005/11/COLLADASchema}mesh/{http://www.collada.org/2005/11/COLLADASchema}triangles/{http://www.collada.org/2005/11/COLLADASchema}p")
    arr_TrianglesTemp = [int(i) for i in str.split(tri.text)]
    arr_Triangles= []
    for j in range(0, len(arr_TrianglesTemp)):
        if j%2==0:
            arr_Triangles.append(arr_TrianglesTemp[j])
    triangles = [arr_Triangles[i:i + 3] for i in range(0, len(arr_Triangles), 3)]

    mesh = triangular_mesh(x, y, z, triangles,representation='wireframe',opacity=0)
    mesh.mlab_source.dataset.cell_data.scalars = clusters
    mesh.mlab_source.dataset.cell_data.scalars.name = 'Clusters'
    mesh.mlab_source.update()
    mesh.parent.update()

    mesh2 = pipeline.set_active_attribute(mesh, cell_scalars='Clusters')
    pipeline.surface(mesh2)
    show()
