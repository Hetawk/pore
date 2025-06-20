#!/usr/bin/env python3
"""
Individual thermal insulating board pore structure modeling module.

Generates detailed 3D computational models of pore architecture for individual
CSA cement-based board compositions, based on experimental mercury intrusion
porosimetry characterization data.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from tqdm import tqdm
from .utils import plot_orange_prism_frame, setup_clean_axes, generate_realistic_pores


def create_clean_pore_visualization(ax, diameters, intrusion_values, sample_name,
                                    sample_color='jet'):
    """
    Create a detailed 3D pore structure model for individual board composition.

    Generates computational visualization of pore architecture within the geometric
    framework of the insulating board, using experimental MIP data to determine
    pore size distribution and spatial arrangement.

    Parameters:
    -----------
    ax : matplotlib 3D axis
        The 3D plotting axis for rendering the pore structure
    diameters : array_like
        Experimental pore diameter data from MIP testing
    intrusion_values : array_like
        Mercury intrusion volume data for pore characterization
    sample_name : str
        Board composition identifier (T1, T2, or T3)
    sample_color : str, default='jet'
        Colormap for pore size visualization
    """

    # Configure axes for scientific visualization
    setup_clean_axes(ax)

    # Render the geometric framework representing board boundaries
    plot_orange_prism_frame(ax)

    # Generate realistic pores
    pore_positions, scaled_radii, selected_diameters = generate_realistic_pores(
        diameters, intrusion_values, sample_name, n_pores=600)

    # Set up camera position for depth sorting (adjusted for rectangular shape)
    camera_pos = np.array([3.0, 1.0, 1.0])

    # Define colormap and norm for pore coloring
    colormap = plt.get_cmap(sample_color)
    norm = colors.Normalize(vmin=np.min(scaled_radii),
                            vmax=np.max(scaled_radii))

    # Sort pores by distance from camera for proper rendering
    distances = np.linalg.norm(
        pore_positions - camera_pos.reshape(1, 3), axis=1)
    # Add z-height bonus to keep high pores visible
    z_bonus = pore_positions[:, 2] / 0.4 * 0.2 * np.max(distances)
    adjusted_distances = distances - z_bonus

    # Sort indices based on adjusted distances (back to front)
    sort_indices = np.argsort(-adjusted_distances)
    pore_positions = pore_positions[sort_indices]
    scaled_radii = scaled_radii[sort_indices]

    # Render pores as spheres
    print(f"Rendering {len(pore_positions)} pores for {sample_name}...")
    for i in tqdm(range(len(pore_positions)), desc="Rendering pores"):
        radius = scaled_radii[i]
        color = colormap(norm(radius))

        # Create a sphere for each pore
        u = np.linspace(0, 2 * np.pi, 12)  # Lower resolution for performance
        v = np.linspace(0, np.pi, 8)
        x = pore_positions[i, 0] + radius * np.outer(np.cos(u), np.sin(v))
        y = pore_positions[i, 1] + radius * np.outer(np.sin(u), np.sin(v))
        z = pore_positions[i, 2] + radius * \
            np.outer(np.ones(np.size(u)), np.cos(v))

        ax.plot_surface(x, y, z, color=color, shade=True, alpha=0.9,
                        rstride=1, cstride=1, linewidth=0)

    # Add sample information in clean format
    ax.text2D(0.05, 0.95, sample_name, transform=ax.transAxes, fontsize=12,
              fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))


def create_individual_sample_visualization(diam, intr, sample_name, output_file,
                                           sample_color='jet'):
    """
    Create computational model for individual insulating board composition.

    Generates a detailed 3D visualization of pore structure based on experimental
    mercury intrusion porosimetry data for a single board composition.

    Parameters:
    -----------
    diam : array_like
        Experimental pore diameter measurements
    intr : array_like  
        Mercury intrusion volume data
    sample_name : str
        Board identifier (T1, T2, or T3)
    output_file : str
        Path for saving the generated model
    sample_color : str, default='jet'
        Colormap for visualization
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create the clean visualization
    create_clean_pore_visualization(ax, diam, intr, sample_name, sample_color)

    # Configure viewing angle for optimal visualization
    ax.view_init(elev=30, azim=60)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Individual board model saved to {output_file}")
    plt.close()
