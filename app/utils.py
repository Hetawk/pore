#!/usr/bin/env python3
"""
Common utilities and shared functions for 3D pore structure modeling in 
calcium sulfoaluminate cement-based thermal insulating boards.

This module provides geometric framework and pore generation algorithms 
for computational modeling of experimental mercury intrusion porosimetry data.
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def plot_orange_prism_frame(ax, color='#FF8C00', linewidth=1.5, alpha=0.8):
    """
    Draw the geometric framework representing the CSA cement-based insulating board boundaries.

    Creates a 3D wireframe representation of the experimental board dimensions
    for visualization of pore structures within the material volume.

    Parameters:
    -----------
    ax : matplotlib 3D axis
        The 3D plotting axis for rendering the board frame
    color : str, default='#FF8C00'
        Frame color (orange for visual clarity)
    linewidth : float, default=1.5
        Line thickness for frame edges
    alpha : float, default=0.8
        Transparency level for frame visibility
    """
    # Define the 8 vertices of the rectangular prism representing the insulating board
    # Physical dimensions: 160mm length (X), 160mm width (Y), 40mm thickness (Z)
    # Normalized coordinate system: 160mm → 2.0, 40mm → 0.5
    x_half = 2.0  # Half-length in normalized coordinates (80mm actual)
    y_half = 2.0  # Half-width in normalized coordinates (80mm actual)
    z_half = 0.5  # Half-thickness in normalized coordinates (20mm actual)

    # Vertex coordinates for the insulating board geometry
    corners = np.array([
        [-x_half, -y_half, -z_half], [x_half, -y_half, -z_half],
        [x_half, y_half, -z_half], [-x_half, y_half, -z_half],
        [-x_half, -y_half, z_half], [x_half, -y_half, z_half],
        [x_half, y_half, z_half], [-x_half, y_half, z_half]
    ])

    # Define the 12 edges of the rectangular prism
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
             (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
             (0, 4), (1, 5), (2, 6), (3, 7)]  # Connecting edges

    # Plot the edges with increased line width for better visibility
    for edge in edges:
        ax.plot([corners[edge[0], 0], corners[edge[1], 0]],
                [corners[edge[0], 1], corners[edge[1], 1]],
                [corners[edge[0], 2], corners[edge[1], 2]],
                color=color, linewidth=linewidth, alpha=alpha)

    # Set visualization boundaries to encompass the entire board geometry
    ax.set_xlim(-2.2, 2.2)  # X-axis range (length dimension)
    ax.set_ylim(-2.2, 2.2)  # Y-axis range (width dimension)
    ax.set_zlim(-0.7, 0.7)  # Z-axis range (thickness dimension)


def setup_clean_axes(ax):
    """
    Configure 3D axes for scientific visualization without visual clutter.

    Removes background grids, tick marks, and axis labels to create clean
    scientific figures suitable for research publication and analysis.

    Parameters:
    -----------
    ax : matplotlib 3D axis
        The 3D plotting axis to configure for clean visualization
    """
    # Remove all default axes elements for clean scientific presentation
    ax.set_axis_off()

    # Create transparent background for professional appearance
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # Disable grid lines for cleaner visualization
    ax.grid(False)

    # Remove tick marks for uncluttered scientific figures
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # Set aspect ratio matching physical board dimensions (160:160:40 = 4:4:1)
    ax.set_box_aspect([4, 4, 1])

    # Configure isometric viewing angle for optimal 3D perspective
    ax.view_init(elev=30, azim=60)


def generate_realistic_pores(diameters, intrusion_values, sample_name, n_pores=800):
    """
    Generate realistic 3D pore distribution based on experimental MIP data.

    Creates a spatial distribution of spherical pores within the insulating board
    volume, with pore sizes and frequencies derived from mercury intrusion 
    porosimetry measurements. Applies physical constraints to ensure realistic
    pore placement and avoid edge effects.

    Parameters:
    -----------
    diameters : array_like
        Experimental pore diameter data from MIP testing (micrometers)
    intrusion_values : array_like
        Mercury intrusion volume data corresponding to each diameter
    sample_name : str
        Board composition identifier (T1, T2, or T3)
    n_pores : int, default=800
        Target number of pores to generate for visualization

    Returns:
    --------
    tuple
        (pore_positions, scaled_radii, selected_diameters)
        - pore_positions: 3D coordinates of pore centers
        - scaled_radii: Visualization radii in normalized coordinates  
        - selected_diameters: Actual pore diameters from MIP data
    """
    print(f"Generating {n_pores} realistic pores for {sample_name}...")

    # Normalize intrusion data to create probability distribution
    norm_intrusion = intrusion_values / np.sum(intrusion_values)

    # Sample pore diameters based on experimental frequency distribution
    indices = np.random.choice(len(diameters), size=n_pores, p=norm_intrusion)
    selected_diameters = diameters[indices]

    # Convert diameters to μm for visualization and scale to fit in rectangular prism
    selected_diameters_um = selected_diameters / 1000.0  # nm to μm
    selected_radii = selected_diameters_um / 2.0

    # Scale radii for visualization within the rectangular orange prism (smaller to fit better)
    # Adjusted for the smaller Y and Z dimensions
    min_radius, max_radius = 0.03, 0.08
    if np.max(selected_radii) != np.min(selected_radii):
        scaled_radii = min_radius + (max_radius - min_radius) * (
            selected_radii - np.min(selected_radii)) / (np.max(selected_radii) - np.min(selected_radii))
    else:
        scaled_radii = np.ones_like(
            selected_radii) * ((min_radius + max_radius) / 2)

    # Generate pore positions within the rectangular orange prism bounds
    # X: [-1.9, 1.9] (160mm), Y: [-1.9, 1.9] (160mm), Z: [-0.4, 0.4] (40mm)
    x_bound, y_bound, z_bound = 1.9, 1.9, 0.4  # Changed y_bound from 0.4 to 1.9
    pore_positions = []

    # Helper function to add a pore with small jitter
    def add_pore_at(x, y, z, jitter=0.05):
        jx = np.random.normal(0, jitter)
        # Same jitter in Y direction now (changed from jitter * 0.5)
        jy = np.random.normal(0, jitter)
        jz = np.random.normal(0, jitter * 0.5)  # Less jitter in Z direction
        # Ensure pore stays within rectangular prism bounds
        x = max(min(x + jx, x_bound), -x_bound)
        y = max(min(y + jy, y_bound), -y_bound)
        z = max(min(z + jz, z_bound), -z_bound)
        return [x, y, z]

    # 1. Add pores in the upper region (40%)
    top_pores = int(n_pores * 0.4)
    for _ in tqdm(range(top_pores), desc="Top pores"):
        # Use exponential distribution to concentrate toward top
        z_val = z_bound * (1 - np.random.exponential(0.3))
        z_val = min(z_bound, max(0.0, z_val))

        # Distribute across the x-y plane (now both X and Y are 160mm)
        x = np.random.uniform(-x_bound, x_bound)
        y = np.random.uniform(-y_bound, y_bound)

        pore_positions.append([x, y, z_val])

    # 2. Add pores in a diagonal pattern (25%)
    diag_pores = int(n_pores * 0.25)
    for i in tqdm(range(diag_pores), desc="Diagonal pores"):
        # Parametric position along diagonal (weighted toward top)
        t = np.random.beta(1.5, 1.0)

        # Create points along the diagonal - emphasize length direction
        x = x_bound * (1 - t * 0.9) * np.random.choice([-1, 1])
        y = y_bound * (1 - t * 0.9) * np.random.choice([-1, 1])
        z = z_bound * (1 - t * 0.5)

        pore_positions.append(add_pore_at(x, y, z, jitter=0.05))

    # 3. Add pores along the edges (15%)
    edge_pores = int(n_pores * 0.15)
    for _ in tqdm(range(edge_pores), desc="Edge pores"):
        edge = np.random.choice(['top-x', 'top-y', 'corner'])

        if edge == 'top-x':
            x = np.random.uniform(-x_bound, x_bound)
            y = y_bound * (0.9 + 0.1 * np.random.random()) * \
                np.random.choice([-1, 1])
            z = z_bound * (0.8 + 0.2 * np.random.random())
        elif edge == 'top-y':
            x = x_bound * (0.9 + 0.1 * np.random.random()) * \
                np.random.choice([-1, 1])
            y = np.random.uniform(-y_bound, y_bound)
            z = z_bound * (0.8 + 0.2 * np.random.random())
        else:  # corner
            x = x_bound * (0.85 + 0.15 * np.random.random()) * \
                np.random.choice([-1, 1])
            y = y_bound * (0.85 + 0.15 * np.random.random()) * \
                np.random.choice([-1, 1])
            z = z_bound * (0.85 + 0.15 * np.random.random())

        pore_positions.append(add_pore_at(x, y, z, jitter=0.03))

    # 4. Add remaining pores throughout the volume (20%)
    remaining = n_pores - len(pore_positions)
    for _ in tqdm(range(remaining), desc="Remaining pores"):
        x = np.random.uniform(-x_bound, x_bound)
        y = np.random.uniform(-y_bound, y_bound)
        z = np.random.uniform(-z_bound, z_bound)
        pore_positions.append([x, y, z])

    pore_positions = np.array(pore_positions)

    return pore_positions, scaled_radii, selected_diameters
