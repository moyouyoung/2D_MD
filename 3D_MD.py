import numpy as np

# Number of particles
N = 100

# Simulation box size (assuming a cubic box)
box_size = 10.0  # in arbitrary units

# Time step
dt = 0.001  # in arbitrary time units

# Temperature
temperature = 300  # in Kelvin

# Initialize random particle positions within the simulation box
positions = np.random.uniform(0, box_size, size=(N, 3))

# Initialize random velocities from a Gaussian distribution
velocities = np.random.normal(0, 1, size=(N, 3))

# Lennard-Jones potential parameters
epsilon = 1.0  # depth of the potential well
sigma = 1.0  # distance at which potential is zero

def lennard_jones(r):
    # r: distance between particles
    r6 = (sigma / r) ** 6
    r12 = r6 ** 2
    return 4 * epsilon * (r12 - r6)

def compute_forces(positions):
    forces = np.zeros_like(positions)
    for i in range(N):
        for j in range(i + 1, N):
            # Vector from particle i to j
            r_ij = positions[j] - positions[i]
            
            # Minimum image convention (periodic boundary conditions)
            r_ij = r_ij - box_size * np.round(r_ij / box_size)
            
            # Distance between particles
            r = np.linalg.norm(r_ij)
            
            if r > 0:  # Avoid division by zero
                # Compute the force magnitude
                force_magnitude = -24 * epsilon * ((2 * (sigma / r) ** 12) - ((sigma / r) ** 6)) / r
                
                # Force vector
                force_vector = (r_ij / r) * force_magnitude
                
                # Update forces for both particles
                forces[i] += force_vector
                forces[j] -= force_vector
    
    return forces

def integrate(positions, velocities, forces, dt):
    # Update positions using the Velocity Verlet algorithm
    new_positions = positions + velocities * dt + 0.5 * forces * dt ** 2
    
    # Apply periodic boundary conditions
    new_positions = np.mod(new_positions, box_size)
    
    # Recompute forces with the updated positions
    new_forces = compute_forces(new_positions)
    
    # Update velocities
    new_velocities = velocities + 0.5 * (forces + new_forces) * dt
    
    return new_positions, new_velocities, new_forces

# Total simulation steps
num_steps = 1000

# Compute initial forces
forces = compute_forces(positions)

# Main simulation loop
for step in range(num_steps):
    # Integrate the equations of motion
    positions, velocities, forces = integrate(positions, velocities, forces, dt)
    
    # Optionally, add code to compute observables like temperature or energy here
    # and save results to a file for later analysis