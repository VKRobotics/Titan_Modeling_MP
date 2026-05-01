import math
import constants
import helper_func
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

V= 6100.0
gamma = np.radians(65.0)
h= 1270000.0
t= 0.0

t_list = [t]
V_list = [V]
gamma_list=[gamma]
h_list=[h]
dt=0.1

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







#------------------------------


import pandas as pd
entry_data   = pd.read_csv('compiled_entry_data.csv')
descent_data = pd.read_csv('compiled_descent_data.csv')

# Use entry data start as t=0 reference
t0 = entry_data['et_epoch (seconds past J2000)'].iloc[0]

# Entry phase real data (heatshield, 150–1246 km)
entry_t_min  = (entry_data['et_epoch (seconds past J2000)'].values - t0) / 60.0
entry_h_km   = entry_data['ref_alt (kilometers)'].values
entry_V      = np.abs(entry_data['entry_inertial_vel (m/s)'].values)
entry_gamma  = np.abs(entry_data['flight_path_angle_deg (deg)'].values)

# Descent phase real data (parachutes, 0–144 km)
descent_t_min  = (descent_data['et_epoch (seconds past J2000)'].values - t0) / 60.0
descent_h_km   = descent_data['ref_alt (kilometers)'].values
descent_V      = np.abs(descent_data['desc_vel (m/s)'].values)
descent_gamma  = np.abs(descent_data['flight_path_angle_deg (deg)'].values)

# Convert sim gamma from radians to degrees for plotting
gamma_deg_arr = np.degrees(np.array(gamma_list))

# ---- 2x2 plot grid ----
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Titan Entry/Descent Simulation vs Huygens Data", fontsize=14, fontweight='bold')
plt.subplots_adjust(wspace=0.3, hspace=0.35)

# Altitude vs Time
ax = axes[0, 0]
ax.invert_yaxis()
ax.plot(entry_t_min, entry_h_km, color='red', linewidth=1.3, alpha=0.7, label='Huygens (entry)')
ax.plot(descent_t_min, descent_h_km, color='darkred', linewidth=1.3, alpha=0.7, label='Huygens (descent)')
ax.plot(t_arr/60, h_arr, color='steelblue', linewidth=2, label='Simulation', zorder=10)
ax.axhline(constants.H_DEPLOY_MAIN/1000, color='orange', linewidth=1, linestyle='--',
           label=f'Main chute ({constants.H_DEPLOY_MAIN//1000} km)')
ax.axhline(constants.H_DEPLOY_DROGUE/1000, color='green', linewidth=1, linestyle='--',
           label=f'Drogue ({constants.H_DEPLOY_DROGUE//1000} km)')
ax.set_xlabel("Time (min)")
ax.set_ylabel("Altitude (km)")
ax.set_title("Altitude vs Time")
ax.legend(fontsize=8, loc='upper right')
ax.grid(True, alpha=0.3)

# Speed vs Time
ax = axes[0, 1]
ax.plot(entry_t_min, entry_V, color='red', linewidth=1.3, alpha=0.7, label='Huygens (entry)')
ax.plot(descent_t_min, descent_V, color='darkred', linewidth=1.3, alpha=0.7, label='Huygens (descent)')
ax.plot(t_arr/60, V_arr, color='coral', linewidth=2, label='Simulation',zorder=10)
ax.set_xlabel("Time (min)")
ax.set_ylabel("Speed (m/s)")
ax.set_title("Speed vs Time")
ax.set_yscale('log')
ax.set_ylim(bottom=1)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, which='both')

# Altitude vs Speed
ax = axes[1, 0]
ax.invert_yaxis()
ax.plot(entry_V, entry_h_km, color='red', linewidth=1.3, alpha=0.7, label='Huygens (entry)')
ax.plot(descent_V, descent_h_km, color='darkred', linewidth=1.3, alpha=0.7, label='Huygens (descent)')
ax.plot(V_arr, h_arr, color='seagreen', linewidth=2, label='Simulation',zorder=10)
ax.set_xlabel("Speed (m/s)")
ax.set_ylabel("Altitude (km)")
ax.set_title("Altitude vs Speed")
ax.set_xscale('log')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, which='both')


# Flight Path Angle vs Time
ax = axes[1, 1]
ax.plot(entry_t_min, entry_gamma, color='red', linewidth=1.3, alpha=0.7, label='Huygens (entry)')
ax.plot(descent_t_min, descent_gamma, color='darkred', linewidth=1.3, alpha=0.7, label='Huygens (descent)')
ax.plot(t_arr/60, gamma_deg_arr, color='purple', linewidth=2, label='Simulation',zorder=10)
ax.set_xlabel("Time (min)")
ax.set_ylabel("Flight path angle |γ| (deg)")
ax.set_title("Flight Path Angle vs Time")
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("titan_entry_simulation.png", dpi=150, bbox_inches='tight')
plt.show()
print("Plot saved as 'titan_entry_simulation.png'")


#-----------------------------
#Benchmarking
def percent_error(experimental, theoretical):
    return ((experimental-theoretical)/theoretical) *100
def val_alt(h_arr, val_arr, target_h_km):
    """Interpolate val_arr to find its value when altitude crosses target."""
    h_m = h_arr * 1000  # h_arr is in km here
    return np.interp(target_h_km*1000, h_m[::-1], val_arr[::-1])

# Total descent time
real_total_min = descent_t_min[-1]
sim_total_min = t_arr[-1] / 60
print(f"\n[1] TOTAL Mission TIME")
print(f"    Real:  {real_total_min:7.2f} min")
print(f"    Sim:   {sim_total_min:7.2f} min")
print(f"    Error: {abs(sim_total_min - real_total_min):7.2f} min ")
print(f"    % Error: {percent_error(real_total_min,sim_total_min):7.2f} % ")

# Velocity at main chute deployment (h=160km)
sim_V_at_160 = val_alt(h_arr, V_arr, 160)
real_V_at_160 = np.interp(160000, entry_h_km[::-1]*1000, entry_V[::-1])
print(f"\n[2] VELOCITY AT MAIN CHUTE (h=160 km)")
print(f"    Real:  {real_V_at_160:7.1f} m/s")
print(f"    Sim:   {sim_V_at_160:7.1f} m/s")
print(f"    Error: {abs(sim_V_at_160-real_V_at_160):7.1f} m/s")
print(f"    % Error: {percent_error(real_V_at_160,sim_V_at_160):7.2f} % ")

# Landing velocity
print(f"\n[3] LANDING VELOCITY")
print(f"    Real:  {descent_V[-1]:7.2f} m/s")
print(f"    Sim:   {V_arr[-1]:7.2f} m/s")
print(f"    Error: {abs(V_arr[-1] - descent_V[-1]):7.2f} m/s")
print(f"    % Error: {percent_error(descent_V[-1],V_arr[-1]):7.2f} %")

# Velocity RMSE
mask = (h_arr*1000 > 150000) & (h_arr*1000 < 1250000)
sim_V_interp = np.interp(entry_h_km*1000, (h_arr[mask]*1000)[::-1], V_arr[mask][::-1])
rmse_entry = np.sqrt(np.mean((sim_V_interp - entry_V)**2))
print(f"\n[4] VELOCITY RMSE")
print(f"    {rmse_entry:7.1f} m/s")




# Tryna find rmse for the descent and entry altitude graphs
def calculate_rmse(sim_values, real_values):
    """Calculates Root Mean Square Error: sqrt(mean((sim - real)^2))"""
    return np.sqrt(np.mean((sim_values - real_values)**2))


H_BOUNDARY = constants.H_DEPLOY_MAIN / 1000.0  # 160 km


entry_mask = h_arr >= H_BOUNDARY
descent_mask = h_arr < H_BOUNDARY


h_sim_entry = h_arr[entry_mask]
t_sim_entry = t_arr[entry_mask] / 60.0


h_sim_descent = h_arr[descent_mask]
t_sim_descent = t_arr[descent_mask] / 60.0



interp_h_entry = np.interp(entry_t_min, t_sim_entry, h_sim_entry)
interp_h_descent = np.interp(descent_t_min, t_sim_descent, h_sim_descent)

rmse_h_entry = calculate_rmse(interp_h_entry, entry_h_km)
rmse_h_descent = calculate_rmse(interp_h_descent, descent_h_km)

print("RMSE Entry Altitude: "+str(rmse_h_entry)+"km RMSE Descent Altitude"+str(rmse_h_descent)+"km")



