# Modeling the Huygens Entry and Descent Through Titan’s Atmosphere

A numerical-modeling project that simulates the **Huygens probe’s atmospheric entry and descent to Titan**, Saturn’s largest moon.

Built for Linear Algebra and Multivariable Calculus, the project models how the probe’s velocity, altitude, and flight-path angle change under Titan’s gravity and atmospheric drag. The governing differential equations are solved numerically with fourth-order Runge–Kutta (RK4) integration.

[View the project presentation](https://docs.google.com/presentation/d/1hQUBHJ4mOcQx77lazStSN80AWv_ZXY0suKLBsXqRLYo/edit?usp=sharing)

## Overview

Titan is a compelling environment for atmospheric-entry modeling because it has a dense, nitrogen-rich atmosphere, strong high-altitude winds, and limited direct surface data. Huygens remains the only spacecraft to have landed on Titan, making its 2005 descent data a valuable reference for this project.

This model follows a simplified planar trajectory and represents three descent stages:

1. **Atmospheric entry** — capsule-only drag at high altitude  
2. **Main-parachute descent** — increased drag after main-chute deployment  
3. **Stabilizer/drogue descent** — lower-altitude descent configuration  

## Model

The simulation evolves three state variables over time:

- Velocity, `V`
- Flight-path angle, `γ`
- Altitude, `h`

The model includes:

- Titan’s altitude-dependent gravitational acceleration
- Exponential atmospheric-density model
- Aerodynamic drag proportional to `ρV²`
- Drag-area changes associated with parachute deployment
- Spherical Titan geometry
- Fourth-order Runge–Kutta integration with a 5-second timestep

The spacecraft begins at:

```text
Altitude: 1,270 km
Velocity: 6,100 m/s
Flight-path angle: −65°
Mass: 318 kg
