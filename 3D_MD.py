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

def write_xyz_file(filename, positions, atom_type='Ar', comment='This is a comment'):
    """
    Write positions to an XYZ file.

    Parameters:
    - filename: str, the file name to write to.
    - positions: ndarray, the positions of the particles.
    - atom_type: str, the type of atoms, default is 'Ar' for argon.
    - comment: str, a comment for the XYZ file, often used to store additional data like the timestep.
    """
    N = positions.shape[0]
    with open(filename, 'a') as file:  # 'a' mode to append to the file at each call
        # Write the number of atoms
        file.write(f"{N}\n")
        # Write the comment
        file.write(f"{comment}\n")
        # Write positions
        for i in range(N):
            x, y, z = positions[i]
            file.write(f"{atom_type} {x:.8f} {y:.8f} {z:.8f}\n")

# Define save interval and filename
save_interval = 10
xyz_filename = 'simulation.xyz'

# Main simulation loop
for step in range(num_steps):
    # Integrate the equations of motion
    positions, velocities, forces = integrate(positions, velocities, forces, dt)
    
    if step % save_interval == 0:
        # Optional comment, e.g., could be used to write the current timestep
        comment = f"Step {step}"
        write_xyz_file(xyz_filename, positions, atom_type='Ar', comment=comment)
    
    # Other operations like calculating observables
    # Optionally, add code to compute observables like temperature or energy here
    # and save results to a file for later analysis    