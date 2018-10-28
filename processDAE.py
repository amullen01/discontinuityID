from xml.etree import ElementTree as ET
import kmeans
import numpy

#retrieves texture coordinate array from DAE file
#input: path to xml file in DAE format
#output: array of floats
def getInputTexCoords(input):
    xml = ET.parse(input)
    root = xml.getroot()
    texcoord = []
    for child in root.find("{http://www.collada.org/2005/11/COLLADASchema}library_geometries/{http://www.collada.org/2005/11/COLLADASchema}geometry/{http://www.collada.org/2005/11/COLLADASchema}mesh"):
        if child.attrib.get('id') == 'geometry-texcoord_0':
            tx = child.find("{http://www.collada.org/2005/11/COLLADASchema}float_array")
            texcoord = str.split(tx.text)
            return texcoord
    return texcoord

#retrieves array of vertices in format [[x,y,z], [x1,y1,z1], ...]
#input: path to xml file in DAE format
#output: 2 dimensional array of floars
def getVertices(input):
    xml = ET.parse(input)
    root = xml.getroot()

    vertices = root.find(
        "{http://www.collada.org/2005/11/COLLADASchema}library_geometries/{http://www.collada.org/2005/11/COLLADASchema}geometry/{http://www.collada.org/2005/11/COLLADASchema}mesh/{http://www.collada.org/2005/11/COLLADASchema}source/{http://www.collada.org/2005/11/COLLADASchema}float_array")

    arr_VerticesStr = str.split(vertices.text)
    arr_Verticies = [float(i) for i in arr_VerticesStr]
    arr_Verticies_Grouped = [arr_Verticies[x:x + 3] for x in range(0, len(arr_Verticies), 3)]
    return arr_Verticies_Grouped

#retrieves triangle array from DAE file
#input: path to xml file in DAE format
#output: 3d array of floats
def getTriangles(input):
    vertices = getVertices(input)
    xml = ET.parse(input)
    root=xml.getroot()

    triangles = root.find("{http://www.collada.org/2005/11/COLLADASchema}library_geometries/{http://www.collada.org/2005/11/COLLADASchema}geometry/{http://www.collada.org/2005/11/COLLADASchema}mesh/{http://www.collada.org/2005/11/COLLADASchema}triangles/{http://www.collada.org/2005/11/COLLADASchema}p")



    arr_TrianglesTemp = [int(i) for i in str.split(triangles.text)]
    arr_Triangles = []

    for x in range(0, len(arr_TrianglesTemp)):
        if x%2==0:
            arr_Triangles.append(vertices[arr_TrianglesTemp[x]])
    arr_Triangles_Grouped = [arr_Triangles[x:x+3] for x in range(0, len(arr_Triangles),3)]
    return arr_Triangles_Grouped

#rewrites dae file to output.dae to update texcoords
#inputs: path to input xml, new texcoord array, cluster array
#outputs: res/output.dae file with updated texcoord field
def reWriteTexCoords(input, newTexcoords, clusters):
    xml = ET.parse(input)
    root = xml.getroot()

    for child in root.find("{http://www.collada.org/2005/11/COLLADASchema}library_geometries/{http://www.collada.org/2005/11/COLLADASchema}geometry/{http://www.collada.org/2005/11/COLLADASchema}mesh"):
        if child.attrib.get('id') == 'geometry-texcoord_0':
            tx = child.find("{http://www.collada.org/2005/11/COLLADASchema}float_array")
            tx.text = str(newTexcoords)
            tx.set('updated', 'yes')
            break

    triangles = root.find("{http://www.collada.org/2005/11/COLLADASchema}library_geometries/{http://www.collada.org/2005/11/COLLADASchema}geometry/{http://www.collada.org/2005/11/COLLADASchema}mesh/{http://www.collada.org/2005/11/COLLADASchema}triangles/{http://www.collada.org/2005/11/COLLADASchema}p")
    arr_Triangles = [int(i) for i in str.split(triangles.text)]

    triNum = 0
    vertexCount = 0

    returnText = ''
    for x in range(0, len(arr_Triangles)):
        if x%2!=0:
            if vertexCount<3:
                vertexCount+=1
                returnText += str(clusters[triNum]) + " "
            else:
                triNum += 1
                vertexCount = 0
        else:
            returnText += str(arr_Triangles[x]) + " "
    triangles.text = returnText[:-1]
    triangles.set('updated', 'yes')
    xml.write('res/outputCollada/output.dae')

def processTiles(inputDirectory):
    dict = {'normals':[],'vertices':[], 'triangleMap':[]}

    mapOffset = 0

    for x in range(0,10):
        file = inputDirectory+'Tile_'+str(x+1)+'.dae'

        for normal in kmeans.computeNormals(getTriangles(file)):
            dict['normals'].append(normal)

        for vertex in getVertices(file):
            dict['vertices'].append(vertex )

        for map in getTriangleMap(file):
            mapping = numpy.array(map)
            dict['triangleMap'].append(mapping+mapOffset)
        mapOffset=(len(dict['vertices']))

    return dict

def getTriangleMap(path):
    xml = ET.parse(path)
    root = xml.getroot()
    tri = root.find(
        "{http://www.collada.org/2005/11/COLLADASchema}library_geometries/{http://www.collada.org/2005/11/COLLADASchema}geometry/{http://www.collada.org/2005/11/COLLADASchema}mesh/{http://www.collada.org/2005/11/COLLADASchema}triangles/{http://www.collada.org/2005/11/COLLADASchema}p")
    arr_TrianglesTemp = [int(i) for i in str.split(tri.text)]
    arr_Triangles = []
    for j in range(0, len(arr_TrianglesTemp)):
        if j % 2 == 0:
            arr_Triangles.append(arr_TrianglesTemp[j])
    triangleMap = [arr_Triangles[i:i + 3] for i in range(0, len(arr_Triangles), 3)]
    return triangleMap