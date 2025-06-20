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
from .config import get_config


def plot_orange_prism_frame(ax, color=None, linewidth=None, alpha=None):
    """
    Draw the geometric framework representing the CSA cement-based insulating board boundaries.

    Creates a 3D wireframe representation of the experimental board dimensions
    for visualization of pore structures within the material volume.

    Parameters:
    -----------
    ax : matplotlib 3D axis
        The 3D plotting axis for rendering the board frame
    color : str, optional
        Frame color (defaults to config setting)
    linewidth : float, optional
        Line thickness for frame edges (defaults to config setting)
    alpha : float, optional
        Transparency level for frame visibility (defaults to config setting)
    """
    config = get_config()

    # Use config defaults if parameters not provided
    if color is None:
        color = config.frame_color
    if linewidth is None:
        linewidth = config.frame_linewidth
    if alpha is None:
        alpha = config.frame_alpha

    # Get board corner coordinates from config
    corners = config.get_board_corners()
    edges = config.get_board_edges()

    # Plot the edges with configured styling
    for edge in edges:
        ax.plot([corners[edge[0], 0], corners[edge[1], 0]],
                [corners[edge[0], 1], corners[edge[1], 1]],
                [corners[edge[0], 2], corners[edge[1], 2]],
                color=color, linewidth=linewidth, alpha=alpha)

    # Set visualization boundaries from config
    x_limits, y_limits, z_limits = config.x_limits, config.y_limits, config.z_limits
    ax.set_xlim(x_limits)
    ax.set_ylim(y_limits)
    ax.set_zlim(z_limits)


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
    config = get_config()

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

    # Set aspect ratio from config (matches physical board dimensions)
    ax.set_box_aspect(config.aspect_ratio)

    # Configure viewing angle from config for optimal 3D perspective
    ax.view_init(elev=config.view_elevation, azim=config.view_azimuth)


def generate_realistic_pores(diameters, intrusion_values, sample_name, n_pores=None):
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
    n_pores : int, optional
        Target number of pores to generate for visualization
        If None, uses config default for individual visualizations

    Returns:
    --------
    tuple
        (pore_positions, scaled_radii, selected_diameters)
        - pore_positions: 3D coordinates of pore centers
        - scaled_radii: Visualization radii in normalized coordinates  
        - selected_diameters: Actual pore diameters from MIP data
    """
    config = get_config()

    # Use config default if n_pores not specified
    if n_pores is None:
        n_pores = config.n_pores_individual

    print(f"Generating {n_pores} realistic pores for {sample_name}...")

    # Normalize intrusion data to create probability distribution
    norm_intrusion = intrusion_values / np.sum(intrusion_values)

    # Sample pore diameters based on experimental frequency distribution
    indices = np.random.choice(len(diameters), size=n_pores, p=norm_intrusion)
    selected_diameters = diameters[indices]

    # Convert diameters to μm for visualization and scale to fit in board geometry
    selected_diameters_um = selected_diameters / 1000.0  # nm to μm
    selected_radii = selected_diameters_um / 2.0

    # Scale radii for visualization using config parameters
    min_radius, max_radius = config.min_pore_radius, config.max_pore_radius
    if np.max(selected_radii) != np.min(selected_radii):
        scaled_radii = min_radius + (max_radius - min_radius) * (
            selected_radii - np.min(selected_radii)) / (np.max(selected_radii) - np.min(selected_radii))
    else:
        scaled_radii = np.ones_like(
            selected_radii) * ((min_radius + max_radius) / 2)

    # Apply global pore scaling factor from config
    scaled_radii *= config.pore_scale_factor

    # Generate pore positions within the board bounds from config
    positioning_params = config.get_positioning_parameters()
    # Configurable margin from edges
    x_bound = config.length_scale * positioning_params['edge_margin_factor']
    # Configurable margin from edges
    y_bound = config.width_scale * positioning_params['edge_margin_factor']
    # Configurable margin from top/bottom
    z_bound = config.thickness_scale * positioning_params['z_margin_factor']

    pore_positions = []

    # Helper function to add a pore with small jitter
    def add_pore_at(x, y, z, jitter=None):
        if jitter is None:
            jitter = positioning_params['jitter_strength']
        jx = np.random.normal(0, jitter)
        jy = np.random.normal(0, jitter)
        # Less jitter in Z direction
        jz = np.random.normal(
            0, jitter * positioning_params['z_jitter_factor'])
        # Ensure pore stays within board bounds
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

        # Distribute across the x-y plane
        x = np.random.uniform(-x_bound, x_bound)
        y = np.random.uniform(-y_bound, y_bound)

        pore_positions.append([x, y, z_val])

    # 2. Add pores in a diagonal pattern (configurable percentage)
    diag_pores = int(n_pores * positioning_params['diagonal_pore_ratio'])
    for i in tqdm(range(diag_pores), desc="Diagonal pores"):
        # Parametric position along diagonal (weighted toward top)
        t = np.random.beta(1.5, 1.0)

        # Create points along the diagonal
        edge_factor = positioning_params['edge_position_factor']
        x = x_bound * (1 - t * edge_factor) * np.random.choice([-1, 1])
        y = y_bound * (1 - t * edge_factor) * np.random.choice([-1, 1])
        z = z_bound * (1 - t * 0.5)

        pore_positions.append(add_pore_at(x, y, z))

    # 3. Add pores along the edges (15%)
    edge_pores = int(n_pores * 0.15)
    for _ in tqdm(range(edge_pores), desc="Edge pores"):
        edge = np.random.choice(['top-x', 'top-y', 'corner'])

        edge_factor = positioning_params['edge_position_factor']
        corner_factor = positioning_params['corner_position_factor']

        if edge == 'top-x':
            x = np.random.uniform(-x_bound, x_bound)
            y = y_bound * (edge_factor + (1-edge_factor) * np.random.random()) * \
                np.random.choice([-1, 1])
            z = z_bound * (0.8 + 0.2 * np.random.random())
        elif edge == 'top-y':
            x = x_bound * (edge_factor + (1-edge_factor) * np.random.random()) * \
                np.random.choice([-1, 1])
            y = np.random.uniform(-y_bound, y_bound)
            z = z_bound * (0.8 + 0.2 * np.random.random())
        else:  # corner
            x = x_bound * (corner_factor + (1-corner_factor) * np.random.random()) * \
                np.random.choice([-1, 1])
            y = y_bound * (corner_factor + (1-corner_factor) * np.random.random()) * \
                np.random.choice([-1, 1])
            z = z_bound * (corner_factor + (1-corner_factor)
                           * np.random.random())

        pore_positions.append(add_pore_at(x, y, z))

    # 4. Add remaining pores throughout the volume (20%)
    remaining = n_pores - len(pore_positions)
    for _ in tqdm(range(remaining), desc="Remaining pores"):
        x = np.random.uniform(-x_bound, x_bound)
        y = np.random.uniform(-y_bound, y_bound)
        z = np.random.uniform(-z_bound, z_bound)
        pore_positions.append([x, y, z])

    pore_positions = np.array(pore_positions)

    return pore_positions, scaled_radii, selected_diameters
