import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import pi,cos,sin,sqrt
import numpy as np
import ants

def calcAnalyticalSolution():
    ngon = ants.Ngon(NUMBER_OF_ANTS)
    phi = ngon.getInteriorAngle()
    intialDistanceAnts = 2*INITIAL_DISTANCE_ORIGIN*sin(2*pi/NUMBER_OF_ANTS/2)
    return intialDistanceAnts/(SPEED*(1-sin(phi-pi/2)))

"""
ALPHA: float
    REQUIRES: 0 < alpha < 1
    What percentage of the distance between the ant in front of it
    should the ants move with the next step. E.g. alpha = 1/10, then
    with each step, the ants move forward 10% of the distance between
    the ant infront of it.
"""
NUMBER_OF_ANTS = 4
SPEED = 1
INITIAL_DISTANCE_ORIGIN = 1

if __name__ == "__main__":
    kwargs = {
        "antGroup": ants.AntGroup(NUMBER_OF_ANTS),
        "maxFrames": 2**20,
        "frameReductionFactor": 2**6, 
        "alpha": 1/1000,
        }
    simulationManager = ants.SimulationManager(**kwargs)
    simulationManager.runSimulation()

    def init():
        """initialize animation"""
        analy_text.set_text('Expected time = %.10f' % 
                calcAnalyticalSolution())
        return (time_text,)

    def animate(i):
        """perform animation step"""
        if i >= simulationManager.getNumFramesUsedAfterReduction():
            i = simulationManager.getNumFramesUsedAfterReduction()
        dots.set_data(
            simulationManager.getIthXPositions(i),
            simulationManager.getIthYPositions(i)
            )
        time_text.set_text('Elapsed time   = %.10f' % 
                simulationManager.getIthTimeElapsed(i))
        distance_text.set_text('Distance between ants = %.10f' % 
                simulationManager.getIthDistanceBetweenAnts(i))
        return (dots, time_text, distance_text,)

    ###########################################################
    # Setup plot
    ###########################################################
    # set up figure and animation
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=(-INITIAL_DISTANCE_ORIGIN, 
                             INITIAL_DISTANCE_ORIGIN), 
                         ylim=(-INITIAL_DISTANCE_ORIGIN, 
                             INITIAL_DISTANCE_ORIGIN))
    # dots to go on the plot
    dots, = ax.plot([], 'bo', ms=.3)
    # declare the text that indicates elapsed time
    time_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
    # text that idicates the analytical solution
    analy_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    # text that indicates the distance between each ant
    distance_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)

    """
    Interval is the length of time that the animation should pause
    in between each frame. The amount of time it takes to calculate
    each frame depends on how complicated the calcualation is, but there's
    this extra `interval` length of time where the animation pauses
    before calculating the next frame.
    """
    interval = 100
    # number of frame steps to rest on the last frame
    pause = 100

    ani = animation.FuncAnimation(fig, animate, 
        frames=simulationManager.getNumFramesUsedAfterReduction()+pause,
        interval=interval, 
        blit=True, 
        init_func=init,
        repeat=False)

    # ani.save('ani.gif', writer='imagemagick', fps=50)

    plt.show()
