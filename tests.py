from kmeans import vectorSubtract, computeNormals
import unittest
import numpy
import kmeans

class MyTest(unittest.TestCase):


    def test_vectorsSubtract(self):
        vertexA = [3,6,4]
        vertexB = [3,3,3]
        self.assertEqual(vectorSubtract(vertexA, vertexB), [0,3,1])

    def test_computeNormals(self):
        triangles = [[[3, 2, 1], [3, 3, 3], [5, 7, -1]],[[17, 3, 5], [6, -1, -7], [5, 18, 3]]]
        numpy.testing.assert_almost_equal(computeNormals(triangles), [[-12,4,-2], [188,122,-213]])

    def test_angleBetweenVectors(self):
        vectorA = [3, 6, 4]
        vectorB = [3, 3, 3]
        numpy.testing.assert_almost_equal(kmeans.angleBetweenVectors(vectorA,vectorB), 0.9622504486493763)

    # def test_mapTextures(self):
    #     clusters = [0, 1, 3, 3, 2]
    #     num_k = 4
    #     triangles =
