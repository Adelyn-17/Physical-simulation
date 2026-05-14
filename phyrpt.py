import numpy as np
import matplotlib.pyplot as plt

# Parameters
m = 0.05  # kg
W_total = 10000  # Joules (10kJ)
x_max = 2.0  # 2 meters track
dt = 0.0001  # time step

# 1. Railgun Simulation
v_r, x_r = [0], [0]
L_prime = 0.5e-6  # H/m
I_r = 200000  # 200kA (Simplified constant current pulse)
efficiency_r = []

for t in np.arange(0, 0.05, dt):
    F_mag = 0.5 * L_prime * I_r ** 2
    F_fric = 0.1 * F_mag  # 10% friction loss
    accel = (F_mag - F_fric) / m

    new_v = v_r[-1] + accel * dt
    new_x = x_r[-1] + new_v * dt

    v_r.append(new_v)
    x_r.append(new_x)
    efficiency_r.append((0.5 * m * new_v ** 2) / W_total)
    if new_x >= x_max: break

# 2. Coilgun Simulation (Simplified Single Stage)
v_c, x_c = [0], [0]


# Coilgun force depends on dL/dx, which is peaked near coil entrance
def dL_dx(x): return 1e-4 * np.exp(-(x - 0.5) ** 2 / 0.1)  # Peak at 0.5m


for t in np.arange(0, 0.05, dt):
    I_c = 50000 * np.exp(-t / 0.01)  # Pulsed discharge
    F_mag = 0.5 * I_c ** 2 * dL_dx(x_c[-1])
    F_loss = 0.05 * v_c[-1] ** 2  # Eddy current loss proportional to v^2
    accel = (F_mag - F_loss) / m

    new_v = v_c[-1] + accel * dt
    new_x = x_c[-1] + new_v * dt

    v_c.append(new_v)
    x_c.append(new_x)
    if new_x >= x_max: break

# Plotting
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(x_r, v_r, label='Railgun')
plt.plot(x_c, v_c, label='Coilgun')
plt.title('Velocity vs. Position')
plt.xlabel('Position (m)');
plt.ylabel('Velocity (m/s)');
plt.legend()

plt.subplot(1, 2, 2)
# Efficiency trend (Conceptual)
v_range = np.linspace(50, 2000, 100)
eff_r = 0.35 * (1 - 80/v_range)  # Efficiency increases with v
eff_c = 0.40 / (1 + (v_range/800)**2) # Efficiency drops slightly at extreme v
plt.plot(v_range, eff_r, label='Railgun Efficiency')
plt.plot(v_range, eff_c, label='Coilgun Efficiency')
plt.title('Energy Efficiency vs. Velocity')
plt.xlabel('Velocity (m/s)');
plt.ylabel('Efficiency');
plt.legend()
plt.tight_layout()
plt.show()
