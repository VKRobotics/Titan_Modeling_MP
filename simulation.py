import math
import constants
import helper_func
import numpy as np
import matplotlib.pyplot as plt

V= 6100.0
gamma = np.radians(-65.0)
h= 1270000.0
t= 0.0

t_list = [t]
V_list = [V]
gamma_list=[gamma]
h_list=[h]
dt=5

def derivs(V, gamma, h):
    """Returns (dV/dt, dgamma/dt, dh/dt) at the given state."""
    return (
        helper_func.dV_dt(V, gamma, h),
        helper_func.dgamma_dt(V, gamma, h),
        helper_func.dh_dt(V, gamma),
    )

while h > 0:
    
    k1V, k1g, k1h = derivs(V, gamma, h)

   
    k2V, k2g, k2h = derivs(
        V+ 0.5 * dt * k1V,
        gamma+0.5 * dt * k1g,
        h+0.5 * dt * k1h,
    )

    
    k3V, k3g, k3h = derivs(
        V+0.5*dt*k2V,
        gamma + 0.5*dt*k2g,
        h     + 0.5 * dt * k2h,
    )

    
    k4V, k4g, k4h = derivs(
        V+dt*k3V,
        gamma+dt *k3g,
        h+dt*k3h,
    )

    # Weighted average: (k1 + 2k2 + 2k3 + k4) / 6
    V+= (dt / 6.0) * (k1V + 2*k2V + 2*k3V + k4V)
    gamma+= (dt / 6.0) * (k1g + 2*k2g + 2*k3g + k4g)
    h+= (dt / 6.0) * (k1h + 2*k2h + 2*k3h + k4h)
    t+= dt

    V_list.append(V)
    gamma_list.append(gamma)
    h_list.append(h)
    t_list.append(t)

    if V < 0.1:
        V = 0.1
        break
if h_list[-1] < 0:
    t_list.pop(); V_list.pop(); gamma_list.pop(); h_list.pop()
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





