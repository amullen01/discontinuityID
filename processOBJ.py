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
            vertices.append([float(v.group('x')), float(v.group('y')), float(v.group('z'))])
        elif line[1][0] + line[1][1]=='f ':
            f=re.search(facePattern,line[1])
            faces.append([int(f.group('v1')), int(f.group('v2')), int(f.group('v3'))])

    return [vertices, faces]



#input: list of length two where list[0] is a list of vertices and list[1] is a list of faces with vertice references
    #list[0][x] = [v1, v2, v3]
    #list[1][x] = [p1, p2, p3]
#output: list of triangular faces with their vertices in (x,y,z)
def getTriangles(filepath):


    vertices = []
    faces = []
    xyz = []

    vertexPattern = re.compile('v (?P<x>[-.+e\d]+) (?P<y>[-.+e\d]+) (?P<z>[-.+e\d]+)')
    facePattern = re.compile('f (?P<v1>\d+)\/.*?(?P<v2>\d+)\/.*?(?P<v3>\d+)\/.*')

    for line in enumerate(open(filepath)):
        if line[1][0] + line[1][1] == 'v ':
            v = re.search(vertexPattern, line[1])
            vertices.append([float(v.group('x')), float(v.group('y')), float(v.group('z'))])
        elif line[1][0] + line[1][1] == 'f ':
            f = re.search(facePattern, line[1])
            faces.append([int(f.group('v1')), int(f.group('v2')), int(f.group('v3'))])


    for face in faces:
        p1 = [vertices[face[0]-1][0], vertices[face[0]-1][1], vertices[face[0]-1][2]]
        p2 = [vertices[face[1]-1][0], vertices[face[1]-1][1], vertices[face[1]-1][2]]
        p3 = [vertices[face[2]-1][0], vertices[face[2]-1][1], vertices[face[2]-1][2]]
        xyz.append([p1,p2,p3])
    return [xyz, vertices, faces]












