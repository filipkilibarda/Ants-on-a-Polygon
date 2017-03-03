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

NUMBER_OF_ANTS = 4
SPEED = 1
INITIAL_DISTANCE_ORIGIN = 1
ALPHA = 1/100

if __name__ == "__main__":
    frames = 2**14 # max number of frames to compute
    frameCountFactor = 2**3 # the factor for how many frames to cut out
    simulationManager = ants.simulationManager(ants.AntGroup(NUMBER_OF_ANTS))

    positions = np.zeros((NUMBER_OF_ANTS*frames,2))
    elapsedTimes = np.zeros(frames)
    distances = np.zeros(frames)
    for i in range(frames):
        x,y = simulationManager.getPositions()
        positions[i*NUMBER_OF_ANTS:(i+1)*NUMBER_OF_ANTS,0] = x
        positions[i*NUMBER_OF_ANTS:(i+1)*NUMBER_OF_ANTS,1] = y
        elapsedTimes[i] = simulationManager.getTimeElapsed()
        distances[i] = simulationManager.getDistanceBetweenAnts()
        try:
            simulationManager.step()
        except ants.AntsReachedEndException:
            print("Reached end of simulation")
            numFramesUsed = i+1
            break

    def init():
        """initialize animation"""
        analy_text.set_text('expected time = %.10f' % 
                calcAnalyticalSolution())
        return (time_text,)

    def animate(i):
        """perform animation step"""
        i = frameCountFactor*i
        print(i)
        dots.set_data(
            positions[:i*NUMBER_OF_ANTS,0],
            positions[:i*NUMBER_OF_ANTS,1],
            )
        time_text.set_text('time = %.10f' % elapsedTimes[i])
        distance_text.set_text('distance = %.10f' % distances[i])
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
    ax.grid()
    # dots to go on the plot
    dots, = ax.plot([], 'bo', ms=.3)
    # declare the text that indicates elapsed time
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    # text that idicates the analytical solution
    analy_text = ax.text(0.5, 0.95, '', transform=ax.transAxes)
    # text that indicates the distance between each ant
    distance_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)

    # choose the interval based on dt and the time to animate one step
    from time import time
    t0 = time()
    animate(0)
    t1 = time()
    """
    Interval is the length of time that the animation should pause
    in between each frame. The amount of time it takes to calculate
    each frame depends on how complicated the calcualation is, but there's
    this extra `interval` length of time where the animation pauses
    before calculating the next frame.
    """
    # interval = 1000 * dt - (t1 - t0)
    interval = 0

    ani = animation.FuncAnimation(fig, animate, 
            frames=int(frames/frameCountFactor),
            interval=interval, 
            blit=True, 
            init_func=init,
            repeat=False)

    # ani.save('ani.gif', writer='imagemagick', fps=50)

    plt.show()
