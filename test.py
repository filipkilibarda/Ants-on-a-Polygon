import unittest
from numpy.testing import assert_almost_equal 
import numpy as np
from math import pi,sqrt,sin,cos
import matplotlib.pyplot as plt
import math

import ants
import simulation as sim

"""
d: int
    Distance from origin which all the ants should start on... I don't
    see why I would change this to any other number.
speed: int
    Speed ants should move with.
"""
d = sim.INITIAL_DISTANCE_ORIGIN
speed = sim.SPEED

class AntTest(unittest.TestCase):
    def setUp(self):
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
        positions = [[d,0],[0,d],[-d,0],[0,-d]]
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
        expected = [[d,0], [0,d], [-d,0], [0,-d]]
        assert_almost_equal(points, expected)
        # 3 sided
        points = self.ngon3.getVerticies()
        expected = [[d,0], [-d/2,d*sqrt(3)/2], [-d/2,-d*sqrt(3)/2]]
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

class SimulationManagerTest(unittest.TestCase):
    def testCreateSimulationManager(self):
        kwargs = {
            "antGroup":ants.AntGroup(sim.NUMBER_OF_ANTS),
            "maxFrames":2**14,
            "alpha": 1/100,
            }
        simManager = ants.SimulationManager(**kwargs)

    def testRunSim(self):
        kwargs = {
            "antGroup":ants.AntGroup(sim.NUMBER_OF_ANTS),
            "maxFrames":2**14,
            "alpha": 1/100,
            }
        simManager = ants.SimulationManager(**kwargs)
        simManager.runSimulation()

    def testRunSim2(self):
        kwargs = {
            "antGroup":ants.AntGroup(4),
            "maxFrames":4,
            "alpha": 1/1000,
            }
        simManager = ants.SimulationManager(**kwargs)
        simManager.runSimulation()
        shape = np.array(simManager.getAllPositions()).shape
        self.assertEqual((4*4,2),shape)
        self.assertEqual(4,len(simManager.getAllTimeElapsed()))
        self.assertEqual(4,len(simManager.getAllDistanceBetweenAnts()))

    def testRunSim3(self):
        n = 4
        kwargs = {
            "antGroup":ants.AntGroup(n),
            "maxFrames":2**14,
            "alpha": 1/1000,
            }
        simManager = ants.SimulationManager(**kwargs)
        simManager.runSimulation()
        framesUsed = simManager.getNumFramesUsedAfterReduction()
        positions = simManager.getAllPositions()
        times = simManager.getAllTimeElapsed()
        distances = simManager.getAllDistanceBetweenAnts()
        self.assertEqual(n*framesUsed, len(positions))
        self.assertEqual(framesUsed, len(times))
        self.assertEqual(framesUsed, len(distances))
        self.assertGreater(distances[framesUsed-1],0)
        self.assertGreater(times[framesUsed-1],0)

    def testRunSim4(self):
        n = 4
        factor = 2**3
        kwargs = {
            "antGroup":ants.AntGroup(n),
            "maxFrames":2**14,
            "frameReductionFactor":factor,
            "alpha": 1/1000,
            }
        simManager = ants.SimulationManager(**kwargs)
        simManager.runSimulation()
        framesUsed = simManager.getNumFramesUsedAfterReduction()
        positions = simManager.getAllPositions()
        times = simManager.getAllTimeElapsed()
        distances = simManager.getAllDistanceBetweenAnts()

        self.assertEqual(n*framesUsed, len(positions))
        self.assertEqual(framesUsed, len(times))
        self.assertEqual(framesUsed, len(distances))
        self.assertGreater(distances[framesUsed-1],0)
        self.assertGreater(times[framesUsed-1],0)

    def testRunSim5(self):
        n = 4
        factor = 2
        maxFrames = 4
        kwargs = {
            "antGroup":ants.AntGroup(n),
            "maxFrames":maxFrames,
            "frameReductionFactor":factor,
            "alpha": 1/1000,
            }
        simManager = ants.SimulationManager(**kwargs)
        simManager.runSimulation()
        positions = simManager.getIthPositions(2)
        xPositions = simManager.getIthXPositions(2)
        yPositions = simManager.getIthYPositions(2)
        times = simManager.getIthTimeElapsed(2)
        distances = simManager.getIthDistanceBetweenAnts(2)
        
        self.assertEqual((8,),xPositions.shape)
        self.assertEqual((8,),yPositions.shape)
        self.assertGreater(distances,0)
        self.assertGreater(times,0)
        self.assertEqual(2,simManager.getNumFramesUsedAfterReduction())

    def testRunSim6(self):
        n = 4
        factor = 8
        maxFrames = 2**5
        antGroup = ants.AntGroup(n)
        kwargs = {
            "antGroup":antGroup,
            "maxFrames":maxFrames,
            "frameReductionFactor":factor,
            "alpha": 1/100,
            }
        simManager = ants.SimulationManager(**kwargs)
        origPositions = antGroup.getPositions()
        simManager.runSimulation()
        xPositions = simManager.getIthXPositions(0)
        yPositions = simManager.getIthYPositions(0)
        assert_almost_equal(origPositions[0],xPositions)
        assert_almost_equal(origPositions[1],yPositions)

if __name__ == '__main__':
    unittest.main()
