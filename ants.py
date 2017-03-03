import numpy as np
from math import pi,cos,sin,sqrt
import simulation as sim

class NoNextPosException(Exception):
    """
    Raised when program attempts to step the ant forward when
    there isn't defined next position.
    """
    pass

class NoNextAntException(Exception):
    """
    Raised when an ant has no following ant
    """
    pass

class AntsReachedEndException(Exception):
    """
    Raised when the ants have gone as close to the center as possible
    """

class Ant:
    """
    Represents one ant on a vertex of the N-gon

    position: list-type
        x,y position of ant on grid
    speed: int
        The speed that the ant should move with
    nextAnt: Ant
        A link to the ant infront of it.
    nextPos: list-type
        Next x,y that the ant should move to
    """
    def __init__(self, position, speed, nextAnt=None, nextPos=None):
        self.p = np.array(position)
        self.speed = speed
        self.nextAnt = nextAnt
        self.nextPos = nextPos
    
    def getPosition(self):
        """Return [x,y] position"""
        return self.p.tolist()
    
    def getNextPosition(self):
        return self.nextPos

    def step(self):
        """Advance the position of the ant"""
        if(self.nextPos is None):
            raise NoNextPosException
        # advance current position to the next one
        self.p = self.nextPos
        # set the next position to None - to be determined later
        self.nextPos = None

    def setNextAnt(self, ant):
        self.nextAnt = ant

    def setNextPosition(self, dt):
        """
        Compute the next position of the ant
        
        dt: int
            Indicates length of time step
        """
        if(self.nextAnt == None):
            raise NoNextAntException
        # get the position of this ant
        p = self.p
        # get the position of the ant in front
        p2 = self.nextAnt.getPosition()
        # compute the unit vector pointing in the direction of the
        # next ant
        u = (p2-p)/np.sqrt((p2[0]-p[0])**2 + (p2[1]-p[1])**2)
        # compute the next position
        newPos = p + self.speed*dt*u
        # set the next position
        self.nextPos = newPos

class AntGroup:
    """
    Represents a group of ants arranged on the verticies of an n
    sided polygon.

    SPEED: float/int
        Speed that the ants should move with.
    n: int
        Number of ants
    ants: list-type
        List of ants in this group.
    timeElapsed: float
        The amount of time that has passed since the beginning of 
        the simulation.
    """

    def __init__(self, n):
        self.n = n
        self.ants = []
        self.timeElapsed = 0.
        self.createAnts()

    def createAnts(self):
        """
        Creates n ants with each one placed on a different vertex of
        an n sided polygon
        """
        # first create the Ngon object
        ngon = Ngon(self.n)
        # loop through the verticies of the ngon
        for vertex in ngon.getVerticies():
            # add an ant to the group
            self.ants.append(Ant(vertex, sim.SPEED))
        # set the relationship between ant and next ant
        for ant,nextAnt in zip(self.ants[:-1], self.ants[1:]):
            ant.setNextAnt(nextAnt)
        self.ants[-1].setNextAnt(self.ants[0])
    
    def getAnts(self):
        return self.ants

    def getPositions(self):
        """
        Returns a matrix of x,y positions of ants

        row 1: the x positions
        row 2: the y positions
        """
        positions = [[],[]]
        for ant in self.ants:
            x,y = ant.getPosition()
            positions[0].append(x)
            positions[1].append(y)
        return positions

    def getDistanceBetweenAnts(self):
        """
        Would expect this to calculate an average distance between
        all the ants. However, since the problem is completely symmetrical
        I expect the distances between the ants to be approximately equal.
        So only compute the distance between two ants and return that.
        """
        x1,y1 = self.ants[0].getPosition();
        x2,y2 = self.ants[1].getPosition();
        # calculate the magnitude of the difference vector
        return sqrt((x1-x2)**2 + (y1-y2)**2)

    def step(self, dt):
        """
        Advances the ants one time step forward

        dt: float
            The interval of time that should pass in this timestep
        """
        # set the next positions of the ants
        for ant in self.ants:
            ant.setNextPosition(dt)
        # step all the ants forward
        for ant in self.ants:
            ant.step()
        # advance the time
        self.timeElapsed += dt

class Ngon:
    """
    Represents an N-sided polygon centered on `origin`
    
    n: int
        Number of sides this polygon has
    interiorAngle: float
        The interior angle between each side
    origin: int tuple
        Origin of N-gon
    d: int
        distance from origin each vertex of N-gon has
    """

    def __init__(self, n, origin=(0,0)):
        self.n = n
        self.origin = origin

    def getInteriorAngle(self):
        """
        Uses formula for interior angle: a = (n-2)*pi/2
        """
        return (self.n - 2)*pi/self.n

    def getVerticies(self):
        """
        Calculates the position of each vertex in the N-gon
        """
        phi = 0 # start the first point at phi=0
        points = []
        for phi in np.arange(0, 2*pi, 2*pi/self.n):
            points.append([sim.INITIAL_DISTANCE_ORIGIN*cos(phi), 
                sim.INITIAL_DISTANCE_ORIGIN*sin(phi)])

        return points

class AnimationManager:
    """
    Manages certain parameters of the animation.

    REQUIRES: All the ants are moving at the same speed.

    INVARIANTS:
        1. The distance between the ants is not aproximately equal 0

    alpha: float
        REQUIRES: 0 < alpha < 1
        What percentage of the distance between the ant in front of it
        should the ants move with the next step. E.g. alpha = 1/10, then
        with each step, the ants move forward 10% of the distance between
        the ant infront of it.
    antGroup: AntGroup
        The group of ants this manager is handling.
    antPositionsWithHistory: 2-d list
        Keeps track of the previous and the current positions of the
        ants.
    """
    def __init__(self, antGroup):
        self.antGroup = antGroup
        self.antPositionsWithHistory = {"x":[], "y":[]}

    def _getDtForNextStep(self):
        # distance between the ants
        distance = self.antGroup.getDistanceBetweenAnts()
        # ensure class invariant
        if(distance < 0.0001):
            raise AntsReachedEndException
        # return the timestep
        return sim.ALPHA/sim.SPEED*distance
    
    def step(self):
        dt = self._getDtForNextStep()
        self.antGroup.step(dt)
        # get the positions of the ants
        x,y = self.antGroup.getPositions()
        # add the new positions to the position history
        self.antPositionsWithHistory["x"].extend(x)
        self.antPositionsWithHistory["y"].extend(y)

    def getPositionsWithHistory(self):
        return (self.antPositionsWithHistory["x"],
                self.antPositionsWithHistory["y"])

    def getTimeElapsed(self):
        return self.antGroup.timeElapsed

    def getAntGroup(self):
        return self.antGroup

class simulationManager:
    """
    Manages the simulation. Basically, pre-computes the simulation 
    and stores it in an array to be used later for the animation.

    REQUIRES: All the ants are moving at the same speed.

    INVARIANTS:
        1. The distance between the ants is not aproximately equal 0

    alpha: float
        REQUIRES: 0 < alpha < 1
        What percentage of the distance between the ant in front of it
        should the ants move with the next step. E.g. alpha = 1/10, then
        with each step, the ants move forward 10% of the distance between
        the ant infront of it.
    antGroup: AntGroup
        The group of ants this manager is handling.
    """
    def __init__(self, antGroup):
        self.antGroup = antGroup

    def _getDtForNextStep(self):
        # distance between the ants
        distance = self.antGroup.getDistanceBetweenAnts()
        # ensure class invariant
        if(distance < 0.0001):
            raise AntsReachedEndException
        # return the timestep
        return sim.ALPHA/sim.SPEED*distance

    def step(self):
        dt = self._getDtForNextStep()
        self.antGroup.step(dt)

    def getTimeElapsed(self):
        return self.antGroup.timeElapsed

    def getAntGroup(self):
        return self.antGroup

    def getPositions(self):
        return self.antGroup.getPositions()

    def getDistanceBetweenAnts(self):
        return self.antGroup.getDistanceBetweenAnts()
