import matplotlib.pyplot as plt
import numpy as np
import csv
class Points:
    def __init__(self):
        self.x = []
        self.y = []
        self.z = []

    def add(self, x: float, y: float, z: float) -> None:
        self.x .append(x)
        self.y.append(y)
        self.z.append(z)

def addPointsToAxis(axis, points:Points, color):
    colors = np.tile(color, len(points.x)).reshape(len(points.x), 3)
    axis.scatter(points.x, points.z, points.y, c=colors)

def zoom_factory(ax, base_scale=2.):
    def zoom_fun(event):
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0]) * .5
        cur_yrange = (cur_ylim[1] - cur_ylim[0]) * .5
        xdata = event.xdata  # get event x location
        ydata = event.ydata  # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print
            event.button
        # set new limits
        ax.set_xlim([xdata - cur_xrange * scale_factor,
                     xdata + cur_xrange * scale_factor])
        ax.set_ylim([ydata - cur_yrange * scale_factor,
                     ydata + cur_yrange * scale_factor])
        plt.draw()  # force re-draw

    fig = ax.get_figure()  # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event', zoom_fun)

    # return the function
    return zoom_fun

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

points0 = Points()
points1 = Points()

with open('points.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        points0.add(float(row[0]), float(row[1]), float(row[2]))
        points1.add(float(row[5]), float(row[6]), float(row[7]))

addPointsToAxis(ax, points0, [1.0, 0.0, 0.0])
addPointsToAxis(ax, points1, [0.0, 1.0, 0.0])


scale = 1.5
f = zoom_factory(ax, base_scale=scale)

plt.show()