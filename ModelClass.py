import os
import pyface.qt
import processOBJ
from mayavi.mlab import *
from xml.etree import ElementTree as ET
import numpy as np
import math
import matplotlib.pyplot as plt
import mplstereonet
import operator

class Model:

    directory_path = ''
    xyz = []
    normals = []
    poles = []
    vertices = []
    faces = []


    def __init__(self, model_dir_path):

        print "processing .obj data"
        self.directory_path = model_dir_path

        mapOffset = -1
        for filename in os.listdir(self.directory_path):
            model_data = processOBJ.getTriangles(self.directory_path+"/"+filename)
            self.xyz += model_data[0]
            self.vertices += model_data[1]
            self.faces += [np.array(face)+mapOffset for face in model_data[2]]
            mapOffset = len(self.vertices)-1

        self.normals = self.computeNormals(self.xyz)


    def computeNormals(self, triangles):
        n = []
        for triangle in triangles:
            u = np.subtract(triangle[1], triangle[0])
            v = np.subtract(triangle[2], triangle[0])
            n.append(np.cross(u, v))
        return n
