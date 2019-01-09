import os
import pyface.qt
import processOBJ
from mayavi.mlab import *
from xml.etree import ElementTree as ET
import numpy as np
import math
import matplotlib.pyplot as plt
import mplstereonet

class Model:

    directory_path = ''
    triangles = []
    normals = []
    poles = []


    def __init__(self, model_dir_path):
        print "processing .obj data"
        self.directory_path = model_dir_path

        for filename in os.listdir(self.directory_path):
            self.triangles += processOBJ.getTriangles(model_dir_path+"/"+filename)

        self.normals = self.computeNormals(self.triangles)

        for normal in self.normals:
            self.poles += mplstereonet.normal2pole(normal[0], normal[1], normal[2])


    def computeNormals(self, triangles):
        n = []
        for triangle in triangles:
            u = np.subtract(triangle[1], triangle[0])
            v = np.subtract(triangle[2], triangle[0])
            n.append(np.cross(u, v))
        return n
