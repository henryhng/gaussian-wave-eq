import numpy as np
from scipy.ndimage import laplace

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
import init

# setting up mesh
nx, ny = (50,50)
x = np.linspace(-1,1,nx)
y = np.linspace(-1,1,ny)
X, Y = np.meshgrid(x, y)

# initial condition for gaussian, time step
image = init.gaussian(X,Y,0.5,0,0.15,2)
dt = 0.1

# params for wave eq
c = np.zeros([nx,ny])

# defining values where the wave is allowed to propagate
c[:,27:] = 1
c[:,:23] = 1
c[17:22,23:27]=1
c[28:33,23:27]=1

v=0

# figure, initial surface, RdBu colormap
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
surf = ax.plot_surface(X,Y,image,cmap='RdBu',vmin=-0.1, vmax=0.1)

def animate(i,ax,fig):
    # calculate d2u/dt2
    ax.cla()
    global image
    global v
    a = laplace(image,mode='constant')*np.power(c,2)
    v += a*dt
    image += v*dt

    surf = ax.plot_surface(X,Y,image,cmap='RdBu',vmin=-0.25, vmax=0.25)
    ax.set_zlim(-1, 1)
    return surf


anim = FuncAnimation(fig,animate,interval=1,cache_frame_data=False,fargs=(ax,fig),frames=500)
#plt.show()
anim.save('wave-eq-RdBu.gif', writer='ffmpeg',fps=30)