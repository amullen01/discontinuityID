import re
import os
import numpy



# print(os.listdir())
# print(os.getcwd())

#input: text file with .obj format
#output: list of length two where list[0] is a list of vertices with coordinates [x,y,z] and list[1] is a list of
# triangular faces with references [p1, p2, p3] = the points defining them.
def data_extractor(filepath):

    vertices = []
    faces = []
    vertexPattern = re.compile('v (?P<x>[-.+e\d]+) (?P<y>[-.+e\d]+) (?P<z>[-.+e\d]+)')
    facePattern = re.compile('f (?P<v1>\d+)\/.*?(?P<v2>\d+)\/.*?(?P<v3>\d+)\/.*')

    for line in enumerate(open(filepath)):
        if line[1][0] + line[1][1]=='v ':
            v=re.search(vertexPattern, line[1])
            vertices.append([v.group('x'), v.group('y'), v.group('z')])
        elif line[1][0] + line[1][1]=='f ':
            f=re.search(facePattern,line[1])
            faces.append([f.group('v1'), f.group('v2'), f.group('v3')])

    return [vertices, faces]



#input: list of length two where list[0] is a list of vertices and list[1] is a list of faces with vertice references
    #list[0][x] = [v1, v2, v3]
    #list[1][x] = [p1, p2, p3]
#output: list of triangular faces with their vertices in (x,y,z)
def getTriangles(filepath):

    modelAttributes = data_extractor(filepath)

    vertices = modelAttributes[0]
    faces = modelAttributes[1]
    faces_Coordinated = []
    for face in faces:
        p1 = [float(vertices[int(face[0])-1][0]), float(vertices[int(face[0])-1][1]), float(vertices[int(face[0])-1][2])]
        p2 = [float(vertices[int(face[1])-1][0]), float(vertices[int(face[1])-1][1]), float(vertices[int(face[1])-1][2])]
        p3 = [float(vertices[int(face[2])-1][0]), float(vertices[int(face[2])-1][1]), float(vertices[int(face[2])-1][2])]
        faces_Coordinated.append([p1,p2,p3])
    return faces_Coordinated












