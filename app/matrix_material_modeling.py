#!/usr/bin/env python3
"""
Matrix-filled pore space modeling module for CSA cement-based insulating boards.

Generates computational models representing dense granular material matrix
filling the board volume, simulating the packing of cement particles, 
expanded vermiculite, rice husk ash, and bamboo fiber components.
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from .utils import plot_orange_prism_frame, setup_clean_axes
from . import config


def create_matrix_filled_visualization(diam1, intr1, diam2, intr2, diam3, intr3, output_file):
    """
    Create computational models with dense matrix material filling the board volume.

    Generates 3D visualization representing the granular material matrix composed
    of cement, vermiculite, and agricultural waste components, providing context
    for understanding the material structure surrounding the pore spaces.

    Parameters:
    -----------
    diam1, diam2, diam3 : array_like
        Pore diameter data for boards T1, T2, T3 (influences particle distribution)
    intr1, intr2, intr3 : array_like  
        Intrusion data for boards T1, T2, T3 (influences particle density)
    output_file : str
        Path for saving the generated visualization
    """
    fig = plt.figure(figsize=(20, 8))

    # Create comparative visualization layout for three board compositions
    ax1 = fig.add_subplot(131, projection='3d')
    ax2 = fig.add_subplot(132, projection='3d')
    ax3 = fig.add_subplot(133, projection='3d')

    axes = [ax1, ax2, ax3]
    sample_names = ["T1", "T2", "T3"]
    diameters_list = [diam1, diam2, diam3]
    intrusion_list = [intr1, intr2, intr3]
    cmaps = [plt.cm.Reds, plt.cm.Blues, plt.cm.Oranges]

    # Process each sample
    for i, (ax, name, diameters, intrusion, cmap) in enumerate(zip(
            axes, sample_names, diameters_list, intrusion_list, cmaps)):

        print(f"\nGenerating sand/dust fill for {name}...")

        # Setup clean axes
        setup_clean_axes(ax)

        # Draw orange prism frame
        plot_orange_prism_frame(ax)

        # Calculate particle characteristics based on pore data
        total_porosity = np.sum(intrusion)
        mean_pore_size = np.mean(diameters)

        # Get matrix parameters from configuration
        current_config = config.get_config()
        matrix_params = current_config.get_matrix_parameters()
        dimension_scales = current_config.get_dimension_scale_factors()

        # Create sand/dust particles with varying sizes and density
        # More particles for samples with different characteristics
        base_particles = matrix_params['base_particles']
        particle_count = int(base_particles * dimension_scales['volume_scale'] * (1 + total_porosity /
                             np.max([np.sum(intr1), np.sum(intr2), np.sum(intr3)])))

        print(f"Creating {particle_count} sand/dust particles for {name}...")

        # Generate particle positions throughout the entire volume - fill completely
        # Use bounds from configuration
        x_min, x_max = matrix_params['x_bounds']
        y_min, y_max = matrix_params['y_bounds']
        z_min, z_max = matrix_params['z_bounds']

        x_positions = np.random.uniform(x_min, x_max, particle_count)
        y_positions = np.random.uniform(y_min, y_max, particle_count)
        z_positions = np.random.uniform(z_min, z_max, particle_count)

        # Create particle sizes - very small like sand/dust
        # Vary sizes based on intrusion characteristics
        norm_intrusion = intrusion / np.max(intrusion)

        # Create size distribution based on pore characteristics
        particle_sizes = []
        particle_colors = []

        for j in tqdm(range(particle_count), desc=f"Generating {name} particles"):
            # Map particle position to intrusion characteristics
            # Use distance from center to determine particle properties
            dist_x_norm = abs(x_positions[j]) / matrix_params['length_norm']
            dist_y_norm = abs(y_positions[j]) / matrix_params['width_norm']
            dist_from_center = np.sqrt((dist_x_norm**2 + dist_y_norm**2) / 2)

            # Map to intrusion data
            data_idx = min(
                int(dist_from_center * len(intrusion)), len(intrusion)-1)

            # Particle size based on local pore characteristics
            # Use configurable sizing parameters
            base_size = matrix_params['base_particle_size'] + \
                matrix_params['particle_size_variation'] * \
                norm_intrusion[data_idx]
            size_variation = np.random.uniform(0.7, 1.3)  # Random variation
            final_size = base_size * size_variation

            particle_sizes.append(final_size)

            # Color based on density and position - use config parameters
            color_intensity = matrix_params['color_intensity_base'] + \
                matrix_params['color_intensity_variation'] * \
                norm_intrusion[data_idx]
            particle_colors.append(cmap(color_intensity))

        # Render particles efficiently using scatter plot
        print(
            f"Rendering {len(x_positions)} sand/dust particles for {name}...")

        # Sort particles by depth for proper rendering
        distances = np.sqrt(x_positions**2 + y_positions**2 + z_positions**2)
        sort_indices = np.argsort(-distances)  # Back to front

        # Apply sorting
        x_sorted = x_positions[sort_indices]
        y_sorted = y_positions[sort_indices]
        z_sorted = z_positions[sort_indices]
        sizes_sorted = np.array(particle_sizes)[sort_indices]
        colors_sorted = np.array(particle_colors)[sort_indices]

        # Render particles in batches for better performance
        batch_size = matrix_params['batch_size']
        for batch_start in tqdm(range(0, len(x_sorted), batch_size), desc=f"Rendering {name} batches"):
            batch_end = min(batch_start + batch_size, len(x_sorted))

            ax.scatter(x_sorted[batch_start:batch_end],
                       y_sorted[batch_start:batch_end],
                       z_sorted[batch_start:batch_end],
                       s=sizes_sorted[batch_start:batch_end],
                       c=colors_sorted[batch_start:batch_end],
                       alpha=matrix_params['particle_alpha'],
                       edgecolors='none')

        # Add sample label
        ax.text2D(0.05, 0.95, name, transform=ax.transAxes, fontsize=12,
                  fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

    plt.tight_layout()
    plt.savefig(output_file, dpi=current_config.dpi, bbox_inches='tight')
    print(f"Sand/dust-filled visualization saved to {output_file}")
    plt.close()


def create_sand_dust_visualization(diam, intr, sample_name, output_file, sample_color='jet'):
    """
    Create a detailed visualization of sand/dust filling the pore spaces of a single board sample.

    This function generates a 3D representation of how sand and dust particles occupy
    the voids in the board material, based on the specified pore diameter and intrusion data.
    The visualization helps in understanding the packing and distribution of fine particles
    within the board structure.

    Parameters:
    -----------
    diam : array_like
        Pore diameter data for the board sample (influences particle distribution)
    intr : array_like  
        Intrusion data for the board sample (influences particle density)
    sample_name : str
        Name of the sample (e.g., "T1", "T2", "T3") for labeling the visualization
    output_file : str
        Path for saving the generated visualization
    sample_color : str
        Color map name for visualizing particle density (default is 'jet')
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Setup clean axes
    setup_clean_axes(ax)

    # Draw orange prism frame
    plot_orange_prism_frame(ax)

    # Calculate particle characteristics based on pore data
    total_porosity = np.sum(intr)
    mean_pore_size = np.mean(diam)

    # Get matrix parameters from configuration
    current_config = config.get_config()
    matrix_params = current_config.get_matrix_parameters()
    dimension_scales = current_config.get_dimension_scale_factors()

    # Create sand/dust particles with varying sizes and density
    base_particles = matrix_params['base_particles']
    particle_count = int(base_particles * dimension_scales['volume_scale'] * (1 + total_porosity /
                         np.max([np.sum(intr)])))

    print(
        f"Creating {particle_count} sand/dust particles for {sample_name}...")

    # Generate particle positions throughout the entire volume - fill completely
    x_min, x_max = matrix_params['x_bounds']
    y_min, y_max = matrix_params['y_bounds']
    z_min, z_max = matrix_params['z_bounds']

    x_positions = np.random.uniform(x_min, x_max, particle_count)
    y_positions = np.random.uniform(y_min, y_max, particle_count)
    z_positions = np.random.uniform(z_min, z_max, particle_count)

    # Create particle sizes - very small like sand/dust
    norm_intrusion = intr / np.max(intr)

    # Create size distribution based on pore characteristics
    particle_sizes = []
    particle_colors = []

    for j in tqdm(range(particle_count), desc=f"Generating {sample_name} particles"):
        # Map particle position to intrusion characteristics
        dist_x_norm = abs(x_positions[j]) / matrix_params['length_norm']
        dist_y_norm = abs(y_positions[j]) / matrix_params['width_norm']
        dist_from_center = np.sqrt((dist_x_norm**2 + dist_y_norm**2) / 2)

        # Map to intrusion data
        data_idx = min(
            int(dist_from_center * len(intr)), len(intr)-1)

        # Particle size based on local pore characteristics
        base_size = matrix_params['base_particle_size'] + \
            matrix_params['particle_size_variation'] * \
            norm_intrusion[data_idx]
        size_variation = np.random.uniform(0.7, 1.3)  # Random variation
        final_size = base_size * size_variation

        particle_sizes.append(final_size)

        # Color based on density and position - use config parameters
        color_intensity = matrix_params['color_intensity_base'] + \
            matrix_params['color_intensity_variation'] * \
            norm_intrusion[data_idx]
        particle_colors.append(plt.get_cmap(sample_color)(color_intensity))

    # Sort particles by depth for proper rendering
    distances = np.sqrt(x_positions**2 + y_positions**2 + z_positions**2)
    sort_indices = np.argsort(-distances)  # Back to front

    # Apply sorting
    x_sand_sorted = x_positions[sort_indices]
    y_sand_sorted = y_positions[sort_indices]
    z_sand_sorted = z_positions[sort_indices]
    sizes_sand_sorted = np.array(particle_sizes)[sort_indices]
    colors_sand_sorted = np.array(particle_colors)[sort_indices]

    # Particle rendering - ensure proper visibility
    batch_size = matrix_params['batch_size']
    for batch_start in range(0, len(x_sand_sorted), batch_size):
        batch_end = min(batch_start + batch_size, len(x_sand_sorted))

        # Force edgecolor to None and ensure alpha is respected
        ax.scatter(
            x_sand_sorted[batch_start:batch_end],
            y_sand_sorted[batch_start:batch_end],
            z_sand_sorted[batch_start:batch_end],
            s=sizes_sand_sorted[batch_start:batch_end],
            c=colors_sand_sorted[batch_start:batch_end],
            alpha=matrix_params['particle_alpha'],
            edgecolors='none',
            linewidth=0
        )

    # Add a white background to make colors stand out
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    # Add sample label
    ax.text2D(0.05, 0.95, sample_name, transform=ax.transAxes, fontsize=12,
              fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

    plt.tight_layout()
    plt.savefig(output_file, dpi=current_config.dpi, bbox_inches='tight')
    print(
        f"Sand/dust-filled visualization for {sample_name} saved to {output_file}")
    plt.close()
