import math
import constants
import helper_func
import numpy as np
import matplotlib.pyplot as plt

V= 6100.0
gamma = np.radians(-65.0)
h= 2575000.0
t= 0.0

t_list     = [t]
V_list     = [V]
gamma_list = [gamma]
h_list     = [h]
dt=0.5
while h>0:
    V_rate=helper_func.dV_dt(V, gamma, h)
    gamma_rate=helper_func.dgamma_dt(V, gamma, h)
    h_rate=helper_func.dh_dt(V, gamma)
    #Eulers
    V+=(V_rate*dt) 
    V_list.append(V)
    gamma+=(gamma_rate*dt)
    gamma_list.append(gamma)
    h+=(h_rate*dt)
    h_list.append(h)
    t+=dt
    t_list.append(t)
    #ts threshold is set to velocity=0.1m/s
    if V < 0.1:
        V = 0.1
        break
t_arr=np.array(t_list)
V_arr=np.array(V_list)
gamma_arr=np.degrees(np.array(gamma_list))
h_arr=np.array(h_list)/1000



fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Titan Entry Simulation — Huygens Probe", fontsize=14, fontweight='bold')
plt.subplots_adjust(wspace=0.38)

#alt vs t
ax = axes[0]
ax.plot(t_arr / 60, h_arr, color='steelblue', linewidth=2)
ax.axhline(constants.H_DEPLOY_MAIN / 1000,   color='orange', linewidth=1.3,
           linestyle='--', label=f'Main chute  ({constants.H_DEPLOY_MAIN//1000} km)')
ax.axhline(constants.H_DEPLOY_DROGUE / 1_000, color='green',  linewidth=1.3,
           linestyle='--', label=f'Drogue  ({constants.H_DEPLOY_DROGUE//1000} km)')
ax.set_xlabel("Time (min)")
ax.set_ylabel("Altitude (km)")
ax.set_title("Altitude vs Time")
ax.invert_yaxis()   # put ground (0 km) at the bottom
ax.legend(fontsize=9, loc='lower left')
ax.grid(True, alpha=0.3)

#speed vs t
ax = axes[1]
ax.plot(t_arr / 60, V_arr, color='coral', linewidth=2)
ax.set_xlabel("Time (min)")
ax.set_ylabel("Speed (m/s)")
ax.set_title("Speed vs Time")
ax.set_yscale('log')   # log scale because speed varies from ~6000 to ~5 m/s
ax.grid(True, alpha=0.3, which='both')
ax.set_ylim(bottom=1)

#alt vs speed
ax = axes[2]
ax.plot(V_arr, h_arr, color='seagreen', linewidth=2)
ax.set_xlabel("Speed (m/s)")
ax.set_ylabel("Altitude (km)")
ax.set_title("Altitude vs Speed")
ax.invert_yaxis()   # ground at bottom
ax.set_xscale('log')
ax.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.savefig("titan_entry_simulation.png", dpi=150, bbox_inches='tight')
plt.show()
print("Plot saved as  'titan_entry_simulation.png'")





