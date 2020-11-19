"""
===========
Slider Demo
===========

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from pwem.emlib import metadata as md

mdfile = md.MetaData('volumes.xmd')
deformations = []
cross_corr = []
for objId in mdfile:
    deformations.append(mdfile.getValue(md.MDL_NMA,objId))
    cross_corr.append(mdfile.getValue(md.MDL_MAXCC, objId))
# print(deformations)
# print(cross_corr)
x = np.array(deformations)[:, 0]
y = np.array(deformations)[:, 2]
weight = np.array(cross_corr)
new_x = x
new_y = y
new_c = weight
alpha = 0.25
disk = 150

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
cax = ax.scatter(x, y, c=np.ones(weight.shape) - weight, vmin=0.67, vmax=0.9)
ax.set_xlim([-200,250])
ax.set_ylim([-100,150])
cb = ax.figure.colorbar(cax)
cb.set_label('1- Cross Correlation(CC)')

axcolor = 'lightgoldenrodyellow'
bar1 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
bar2 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
bar3 = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

cc_min = 1- np.max(weight)
cc_max = 1- np.min(weight)
cc_slider = Slider(bar1, '1-CC', cc_min, cc_max, valinit=cc_max, valstep=0.001)
dsize = Slider(bar2, 'disk size', 1, 1000, valinit=150,valstep=0.001)
dtrans = Slider(bar3, 'disk transparency', 0, 1, valinit=0.25,valstep=0.001)

def update1(val):
    indexes = np.argwhere(weight > 1 - val)
    # print(np.argwhere(weight > 1 - val))
    global new_x, new_y, new_c
    new_x = x[indexes]
    new_y = y[indexes]
    new_c = weight[indexes]
    cax = ax.clear()
    cax = ax.scatter(new_x, new_y, c=np.ones(new_c.shape) - new_c, vmin=0.65, vmax=0.9)
    ax.set_xlim([-200, 250])
    ax.set_ylim([-100, 150])

cc_slider.on_changed(update1)

def update2(val):
    global disk
    disk = val
    plot_kwds = {'alpha': alpha, 's': disk, 'linewidths': 0}
    cax = ax.clear()
    cax = ax.scatter(new_x, new_y, c='b', **plot_kwds)
    ax.set_xlim([-200, 250])
    ax.set_ylim([-100, 150])

dsize.on_changed(update2)

def update3(val):
    global alpha
    alpha = val
    plot_kwds = {'alpha': alpha, 's': disk, 'linewidths': 0}
    cax = ax.clear()
    cax = ax.scatter(new_x, new_y, c='b', **plot_kwds)
    ax.set_xlim([-200, 250])
    ax.set_ylim([-100, 150])

dtrans.on_changed(update3)


rax = plt.axes([0.025, 0.5, 0.13, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('1-CC', 'disks'), active=0)


def plot_opi(label):
    print(label)
    if label=='disks':
        plot_kwds = {'alpha': alpha, 's': disk, 'linewidths': 0}
        cax = ax.clear()
        cax = ax.scatter(new_x, new_y, c='b',**plot_kwds)
        ax.set_xlim([-200, 250])
        ax.set_ylim([-100, 150])
    else:
        cax = ax.clear()
        cax = ax.scatter(new_x, new_y, c=np.ones(new_c.shape) - new_c, vmin=0.65, vmax=0.9)
        ax.set_xlim([-200, 250])
        ax.set_ylim([-100, 150])
        pass

radio.on_clicked(plot_opi)

resetax = plt.axes([0.8, 0.005, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    cc_slider.reset()
    dsize.reset()
    dtrans.reset()

button.on_clicked(reset)

plt.show()
