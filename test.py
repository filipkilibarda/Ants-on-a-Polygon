import unittest
import ants
from numpy.testing import assert_almost_equal 
import numpy as np
from math import pi,sqrt,sin,cos
import matplotlib.pyplot as plt
import math

"""
d: int
    Distance from origin which all the ants should start on... I don't
    see why I would change this to any other number.
speed: int
    Speed ants should move with.
"""
d = 1
speed = 1

class AntTest(unittest.TestCase):
    def setUp(self):
        speed = 1
        self.dt = 1
        self.a1 = ants.Ant([0,0], speed)
        self.a2 = ants.Ant([1,0], speed)
        self.a3 = ants.Ant([1,1], speed)
        self.a1.setNextAnt(self.a2)

    def testNextPosition(self):
        # set the next position of the ant
        self.a1.setNextPosition(self.dt)
        # get the next position
        newPos = self.a1.getNextPosition()
        expected = [1,0]
        assert_almost_equal(newPos, expected)
        # test the step function
        self.a1.step()
        assert_almost_equal(self.a1.getPosition(), expected)

    def testNoNextAnt(self):
        self.assertRaises(ants.NoNextAntException, 
                self.a2.setNextPosition, self.dt)

    def testStepNoNextAnt(self):
        self.assertRaises(ants.NoNextPosException, self.a1.step)

class AntGroupTest(unittest.TestCase):
    numAnts = 4
    dt = 1/100
    
    def setUp(self):
        self.group = ants.AntGroup(self.numAnts)

    def testGroup(self):
        # define the expected positions for the ants
        positions = [[1,0],[0,1],[-1,0],[0,-1]]
        # get the ants
        ants = self.group.getAnts()
        # loop through the ants
        for ant, pos in zip(ants, positions):
            assert_almost_equal(ant.getPosition(),pos)

    def testGetInitialDistanceBetweenAnts(self):
        # the angle between each ant vector at the origin
        phi = self._calcInternalAngle()
        expected = 2 * d * sin(phi/2)
        actual = self.group.getDistanceBetweenAnts()
        self.assertAlmostEqual(actual, expected)

    def testGetFinalDistanceBetweenAnts(self):
        # step the ants forward x times
        for _ in range(300):
            self.group.step(self.dt)
        # since the ants went forward so many times expected that
        # they're approx. 0 distance from each other
        expected = 0
        actual = self.group.getDistanceBetweenAnts()
        self.assertAlmostEqual(actual, expected, places=1)

    def _calcInternalAngle(self):
        return 2*pi/self.numAnts

class NgonTest(unittest.TestCase):
    def setUp(self):
        self.ngon3 = ants.Ngon(3)
        self.ngon4 = ants.Ngon(4)
        self.ngon5 = ants.Ngon(5)

    def testNgon(self):
        self.interiorAngle(self.ngon4, pi/2)
        self.interiorAngle(self.ngon5, 3/5*pi)

    def testPoints(self):
        # 4 sided
        points = self.ngon4.getVerticies()
        expected = [[1,0], [0,1], [-1,0], [0,-1]]
        assert_almost_equal(points, expected)
        # 3 sided
        points = self.ngon3.getVerticies()
        expected = [[1,0], [-1/2,sqrt(3)/2], [-1/2,-sqrt(3)/2]]
        assert_almost_equal(points, expected)

    def interiorAngle(self, ngon, expected):
        angle = ngon.getInteriorAngle()
        self.assertAlmostEqual(angle, expected)

class PlotTest(unittest.TestCase):
    def setUp(self):
        self.numAnts = 4
        self.ants = ants.AntGroup(self.numAnts)
        self.dt = 1./100
        self.runTime = math.sqrt(2) - .1
        self.numSteps = math.floor(self.runTime/self.dt)

    def test1(self):
        for i in range(0,10000):
            self.ants.step(self.dt)
        for pos in self.ants.getPositions():
            self.assertLess(pos[0], d)
            self.assertLess(pos[1], d)
            self.assertAlmostEqual(pos[0],0,places=1) 
            self.assertAlmostEqual(pos[1],0,places=1) 
    
    def test2(self):
        for i in range(0,100):
            self.ants.step(self.dt)
        pos = self.ants.getPositions()
        shape = np.array(pos).shape
        expected = (2, self.numAnts)
        self.assertTupleEqual(shape, expected)

class AnimationManagerTest(unittest.TestCase):
    numAnts = 4
    alpha = 1/10

    def setUp(self):
        antGroup = ants.AntGroup(self.numAnts)
        self.animationManager = ants.AnimationManager(self.alpha, antGroup)

    def testGetPositions(self):
        self.animationManager.step()
        positions = self.animationManager.getPositionsWithHistory()

if __name__ == '__main__':
    unittest.main()
