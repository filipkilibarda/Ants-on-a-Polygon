import numpy as np
from math import pi,cos,sin
import matplotlib.pyplot as plt
import matplotlib.animation as animation

if __name__ == '__main__':
    curr = np.array([[0,1],[0,1]])
    # set up figure and animation
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=(-3, 3), ylim=(-3, 3))
    ax.grid()
    # dots to go on the plot
    dots, = ax.plot([], 'bo', ms=6)

    def init():
        """initialize animation"""
        dots.set_data([], [])
        return dots, 

    def animate(i):
        """perform animation step"""
        dots.set_data(curr[0][i], curr[1][i])
        return dots,

    # choose the interval based on dt and the time to animate one step
    from time import time
    t0 = time()
    animate(0)
    t1 = time()
    # interval = 1000 * dt - (t1 - t0)
    interval = 2*(t1 - t0)

    ani = animation.FuncAnimation(fig, animate, frames=2,
                                  interval=interval, 
                                  blit=True, 
                                  init_func=init)

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    #ani.save('double_pendulum.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()

