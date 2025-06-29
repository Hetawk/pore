#!/usr/bin/env python3
"""
Hybrid pore-matrix computational modeling module for CSA cement-based insulating boards.

Generates advanced computational models combining discrete pore structures with
surrounding matrix material, providing comprehensive representation of both
macro-porosity and fine-scale material composition.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Patch
from tqdm import tqdm
from .utils import plot_orange_prism_frame, setup_clean_axes, generate_realistic_pores
from . import config


def create_combined_pores_matrix_visualization(
    diam, intr, sample_name, output_file, sample_color='jet'
):
    """
    Create hybrid computational model combining discrete pores with matrix material.

    Generates advanced 3D visualization showing both major pore structures and
    the surrounding granular material matrix, providing comprehensive understanding
    of the thermal insulating board microstructure.

    Parameters:
    -----------
    diam : array_like
        Experimental pore diameter data from MIP testing
    intr : array_like
        Mercury intrusion volume data for pore characterization
    sample_name : str
        Board composition identifier (T1, T2, or T3)
    output_file : str
        Path for saving the generated hybrid model
    sample_color : str, default='jet'
        Colormap for pore visualization
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    print(f"\nCreating hybrid pore-matrix model for {sample_name}...")

    # Setup clean axes
    setup_clean_axes(ax)

    # Draw orange prism frame
    plot_orange_prism_frame(ax)

    # 1. First, add sand/dust fill with high visibility
    print(f"Adding sand/dust background for {sample_name}...")

    # Get matrix parameters from configuration (same as matrix_material_modeling.py)
    current_config = config.get_config()
    matrix_params = current_config.get_matrix_parameters()
    dimension_scales = current_config.get_dimension_scale_factors()
    particle_counts = current_config.get_particle_counts()
    # Still needed for pore coloring
    size_params = current_config.get_particle_size_parameters()

    # Use matrix parameters from configuration
    x_min, x_max = matrix_params['x_bounds']
    y_min, y_max = matrix_params['y_bounds']
    z_min, z_max = matrix_params['z_bounds']
    length_norm = matrix_params['length_norm']
    width_norm = matrix_params['width_norm']

    # Generate more sand particles for better visibility - scale with volume
    total_porosity = np.sum(intr)
    base_particles = int(
        particle_counts['hybrid_main'] * dimension_scales['volume_scale'])
    sand_particle_count = int(base_particles * (1 + total_porosity / 10))

    # Use bounds from matrix configuration
    x_sand = np.random.uniform(x_min, x_max, sand_particle_count)
    y_sand = np.random.uniform(y_min, y_max, sand_particle_count)
    z_sand = np.random.uniform(z_min, z_max, sand_particle_count)

    # Create particle characteristics based on intrusion data (like sand_dust_viz.py)
    norm_intrusion = intr / np.max(intr)

    # Generate sand particle properties
    sand_sizes = []
    sand_colors = []

    colormap = plt.get_cmap(sample_color)

    for j in range(sand_particle_count):
        # Map particle position to intrusion characteristics
        dist_x_norm = abs(x_sand[j]) / length_norm
        dist_y_norm = abs(y_sand[j]) / width_norm
        dist_from_center = np.sqrt((dist_x_norm**2 + dist_y_norm**2) / 2)

        # Map to intrusion data
        data_idx = min(int(dist_from_center * len(intr)), len(intr)-1)

        # Particle size based on pore characteristics (using matrix parameters)
        base_size = matrix_params['base_particle_size'] + \
            matrix_params['particle_size_variation'] * norm_intrusion[data_idx]
        size_variation = np.random.uniform(0.7, 1.3)
        final_size = base_size * size_variation
        sand_sizes.append(final_size)

        # Color intensity (using matrix parameters)
        color_intensity = matrix_params['color_intensity_base'] + \
            matrix_params['color_intensity_variation'] * \
            norm_intrusion[data_idx]
        sand_colors.append(colormap(color_intensity))

    # Sort sand particles by depth for proper rendering
    sand_distances = np.sqrt(x_sand**2 + y_sand**2 + z_sand**2)
    sand_sort_indices = np.argsort(-sand_distances)

    # Apply sorting
    x_sand_sorted = x_sand[sand_sort_indices]
    y_sand_sorted = y_sand[sand_sort_indices]
    z_sand_sorted = z_sand[sand_sort_indices]
    sizes_sand_sorted = np.array(sand_sizes)[sand_sort_indices]
    colors_sand_sorted = np.array(sand_colors)[sand_sort_indices]

    # Render sand particles with enhanced visibility (using matrix parameters)
    batch_size = matrix_params['batch_size']
    for batch_start in range(0, len(x_sand_sorted), batch_size):
        batch_end = min(batch_start + batch_size, len(x_sand_sorted))

        ax.scatter(x_sand_sorted[batch_start:batch_end],
                   y_sand_sorted[batch_start:batch_end],
                   z_sand_sorted[batch_start:batch_end],
                   s=sizes_sand_sorted[batch_start:batch_end],
                   c=colors_sand_sorted[batch_start:batch_end],
                   alpha=matrix_params['particle_alpha'],
                   edgecolors='none',
                   linewidth=0)  # Force no lines

    # 2. Then, add realistic pores on top
    print(f"Adding realistic pores for {sample_name}...")

    # Generate realistic pores (fewer than individual viz to avoid overcrowding)
    pore_positions, scaled_radii, selected_diameters = generate_realistic_pores(
        diam, intr, sample_name, n_pores=400)

    # Set up camera position for depth sorting
    camera_pos = np.array([3.0, 1.0, 1.0])

    # Define colormap and norm for pore coloring
    norm = colors.Normalize(vmin=np.min(scaled_radii),
                            vmax=np.max(scaled_radii))

    # Sort pores by distance from camera for proper rendering
    distances = np.linalg.norm(
        pore_positions - camera_pos.reshape(1, 3), axis=1)
    z_bonus = pore_positions[:, 2] / 0.4 * 0.2 * np.max(distances)
    adjusted_distances = distances - z_bonus

    # Sort indices based on adjusted distances (back to front)
    sort_indices = np.argsort(-adjusted_distances)
    pore_positions = pore_positions[sort_indices]
    scaled_radii = scaled_radii[sort_indices]

    # Get pore colors from config
    pore_colors = current_config.get_pore_colors()

    # CHECK FOR SAMPLE-SPECIFIC COLOR OVERRIDE
    if hasattr(current_config, 'sample_pore_colors') and sample_name in current_config.sample_pore_colors:
        # Use sample-specific color for all pore types (no size-based distinction)
        sample_color = current_config.sample_pore_colors[sample_name]
        micropore_color = sample_color
        mesopore_color = sample_color
        macropore_color = sample_color
        print(
            f"[DEBUG] Using sample-specific color for {sample_name}: {sample_color}")
    else:
        # Use default size-based colors
        micropore_color = pore_colors["micropore_color"]
        mesopore_color = pore_colors["mesopore_color"]
        macropore_color = pore_colors["macropore_color"]

    # Determine pore size ranges for color assignment
    min_radius = np.min(scaled_radii)
    max_radius = np.max(scaled_radii)
    radius_range = max_radius - min_radius

    # Create size boundaries for the three pore categories
    micropore_max = min_radius + radius_range * 0.33
    mesopore_max = min_radius + radius_range * 0.66

    # Render pores as spheres (with higher alpha to stand out from sand)
    print(f"Rendering {len(pore_positions)} pores for {sample_name}...")
    for i in tqdm(range(len(pore_positions)), desc="Rendering pores"):
        radius = scaled_radii[i]

        # Assign color based on pore size
        if radius <= micropore_max:
            color = micropore_color
        elif radius <= mesopore_max:
            color = mesopore_color
        else:
            color = macropore_color

        # Create a sphere for each pore
        u = np.linspace(0, 2 * np.pi, 12)
        v = np.linspace(0, np.pi, 8)
        x = pore_positions[i, 0] + radius * np.outer(np.cos(u), np.sin(v))
        y = pore_positions[i, 1] + radius * np.outer(np.sin(u), np.sin(v))
        z = pore_positions[i, 2] + radius * \
            np.outer(np.ones(np.size(u)), np.cos(v))

        # Plot with maximum opacity but NO edge lines
        ax.plot_surface(x, y, z, color=color, shade=True, alpha=1.0,
                        rstride=1, cstride=1, linewidth=0)

    # Add sample information
    ax.text2D(0.05, 0.95, sample_name, transform=ax.transAxes, fontsize=12,
              fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

    # Add legend for pore size categories - ONLY if not using sample-specific colors
    if not (hasattr(current_config, 'sample_pore_colors') and sample_name in current_config.sample_pore_colors):
        pore_colors = current_config.get_pore_colors()
        micropore_color = pore_colors["micropore_color"]
        mesopore_color = pore_colors["mesopore_color"]
        macropore_color = pore_colors["macropore_color"]

        # Define the actual size ranges for legend (replace with your actual values or get from config)
        micropore_range = current_config.micropore_range if hasattr(
            current_config, "micropore_range") else (0.03, 0.05)
        mesopore_range = current_config.mesopore_range if hasattr(
            current_config, "mesopore_range") else (0.05, 0.08)
        macropore_range = current_config.macropore_range if hasattr(
            current_config, "macropore_range") else (0.08, 0.15)

        # Use marker size proportional to the mean of each range (scaled for legend visibility)
        def legend_marker_size(r):
            return 800 * (r ** 2)  # scale factor for visibility

        micropore_mean = np.mean(micropore_range)
        mesopore_mean = np.mean(mesopore_range)
        macropore_mean = np.mean(macropore_range)

        legend_elements = [
            Patch(facecolor=micropore_color, edgecolor='k',
                  label=f'Micropores ({micropore_range[0]:.2f}-{micropore_range[1]:.2f})', linewidth=1),
            Patch(facecolor=mesopore_color, edgecolor='k',
                  label=f'Mesopores ({mesopore_range[0]:.2f}-{mesopore_range[1]:.2f})', linewidth=1),
            Patch(facecolor=macropore_color, edgecolor='k',
                  label=f'Macropores ({macropore_range[0]:.2f}-{macropore_range[1]:.2f})', linewidth=1),
        ]

        # Legend: show a circle marker for each pore type, colored as in the plot
        import matplotlib.lines as mlines
        legend_handles = [
            mlines.Line2D([], [], color=micropore_color, marker='o', linestyle='None',
                          markersize=12, label='Micropore'),
            mlines.Line2D([], [], color=mesopore_color, marker='o', linestyle='None',
                          markersize=12, label='Mesopore'),
            mlines.Line2D([], [], color=macropore_color, marker='o', linestyle='None',
                          markersize=12, label='Macropore'),
        ]
        ax.legend(handles=legend_handles,
                  loc='upper right', title='Pore Types')
    # If using sample-specific colors, don't show legend

    plt.tight_layout()
    plt.savefig(output_file, dpi=current_config.dpi, bbox_inches='tight')
    print(f"Combined pores + sand visualization saved to {output_file}")
    plt.close()


def create_combined_three_samples_pores_matrix_visualization(diam1, intr1, diam2, intr2, diam3, intr3, output_file):
    """Create combined visualization with all three samples showing pores + sand"""
    fig = plt.figure(figsize=(18, 7))

    # Create subplots for each sample
    ax1 = fig.add_subplot(131, projection='3d')
    ax2 = fig.add_subplot(132, projection='3d')
    ax3 = fig.add_subplot(133, projection='3d')

    axes = [ax1, ax2, ax3]
    sample_names = ["T1", "T2", "T3"]
    diameters_list = [diam1, diam2, diam3]
    intrusion_list = [intr1, intr2, intr3]
    cmaps = ['Reds', 'Blues', 'Oranges']

    # Sample descriptions
    descriptions = [
        "CSA cement with expanded vermiculite",
        "CSA cement with expanded vermiculite and rice husk ash",
        "CSA cement with vermiculite, rice husk ash and bamboo fiber"
    ]

    # Process each sample
    for i, (ax, name, diameters, intrusion, cmap_name) in enumerate(zip(
            axes, sample_names, diameters_list, intrusion_list, cmaps)):

        print(f"\nCreating combined pores + sand for {name}...")

        # Setup clean axes
        setup_clean_axes(ax)

        # Draw orange prism frame
        plot_orange_prism_frame(ax)

        # Get matrix parameters from configuration (same approach as other functions)
        current_config = config.get_config()
        matrix_params = current_config.get_matrix_parameters()
        dimension_scales = current_config.get_dimension_scale_factors()
        particle_counts = current_config.get_particle_counts()
        size_params = current_config.get_particle_size_parameters()

        # Use matrix parameters from configuration
        x_min, x_max = matrix_params['x_bounds']
        y_min, y_max = matrix_params['y_bounds']
        z_min, z_max = matrix_params['z_bounds']
        length_norm = matrix_params['length_norm']
        width_norm = matrix_params['width_norm']

        total_porosity = np.sum(intrusion)
        base_particles = int(
            particle_counts['hybrid_combined'] * dimension_scales['volume_scale'])
        sand_particle_count = int(base_particles * (1 + total_porosity / 15))

        x_sand = np.random.uniform(x_min, x_max, sand_particle_count)
        y_sand = np.random.uniform(y_min, y_max, sand_particle_count)
        z_sand = np.random.uniform(z_min, z_max, sand_particle_count)

        # Create particle characteristics like sand_dust_viz.py
        norm_intrusion = intrusion / np.max(intrusion)

        sand_sizes = []
        sand_colors = []
        colormap = plt.get_cmap(cmap_name)

        for j in range(sand_particle_count):
            # Map particle position to intrusion characteristics
            dist_x_norm = abs(x_sand[j]) / length_norm
            dist_y_norm = abs(y_sand[j]) / width_norm
            dist_from_center = np.sqrt((dist_x_norm**2 + dist_y_norm**2) / 2)

            # Map to intrusion data
            data_idx = min(
                int(dist_from_center * len(intrusion)), len(intrusion)-1)

            # Particle size and color (same approach as sand_dust_viz.py)
            # Slightly smaller for combined view
            base_size = 0.6 + 1.0 * norm_intrusion[data_idx]
            size_variation = np.random.uniform(0.7, 1.3)
            final_size = base_size * size_variation
            sand_sizes.append(final_size)

            # Higher color intensity for visibility
            color_intensity = size_params['color_intensity_base'] + \
                size_params['color_intensity_variation'] * \
                norm_intrusion[data_idx]
            sand_colors.append(colormap(color_intensity))

        # Sort and render with high visibility
        sand_distances = np.sqrt(x_sand**2 + y_sand**2 + z_sand**2)
        sand_sort_indices = np.argsort(-sand_distances)

        x_sand_sorted = x_sand[sand_sort_indices]
        y_sand_sorted = y_sand[sand_sort_indices]
        z_sand_sorted = z_sand[sand_sort_indices]
        sizes_sand_sorted = np.array(sand_sizes)[sand_sort_indices]
        colors_sand_sorted = np.array(sand_colors)[sand_sort_indices]

        # Render with matrix parameters
        ax.scatter(x_sand_sorted, y_sand_sorted, z_sand_sorted,
                   s=sizes_sand_sorted, c=colors_sand_sorted,
                   alpha=matrix_params['particle_alpha'], edgecolors='none')

        # Add realistic pores
        pore_positions, scaled_radii, _ = generate_realistic_pores(
            diameters, intrusion, name, n_pores=300)  # Fewer pores for combined view

        # Sort and render pores
        camera_pos = np.array([3.0, 1.0, 1.0])
        distances = np.linalg.norm(
            pore_positions - camera_pos.reshape(1, 3), axis=1)
        sort_indices = np.argsort(-distances)
        pore_positions = pore_positions[sort_indices]
        scaled_radii = scaled_radii[sort_indices]

        # Render pores with higher visibility
        norm = colors.Normalize(vmin=np.min(
            scaled_radii), vmax=np.max(scaled_radii))
        for j in tqdm(range(len(pore_positions)), desc=f"Rendering {name} pores"):
            radius = scaled_radii[j]
            color = colormap(0.7 + 0.3 * norm(radius))

            u = np.linspace(0, 2 * np.pi, 8)
            v = np.linspace(0, np.pi, 5)
            x = pore_positions[j, 0] + radius * np.outer(np.cos(u), np.sin(v))
            y = pore_positions[j, 1] + radius * np.outer(np.sin(u), np.sin(v))
            z = pore_positions[j, 2] + radius * \
                np.outer(np.ones(np.size(u)), np.cos(v))

            ax.plot_surface(x, y, z, color=color, shade=True, alpha=0.9,
                            rstride=1, cstride=1, linewidth=0)

        # Add sample label
        ax.text2D(0.05, 0.95, name, transform=ax.transAxes, fontsize=12,
                  fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

    plt.tight_layout()
    plt.savefig(output_file, dpi=current_config.dpi, bbox_inches='tight')
    print(
        f"Combined three-sample pores + sand visualization saved to {output_file}")
    plt.close()
    print(
        f"Combined three-sample pores + sand visualization saved to {output_file}")
    plt.close()
    print(
        f"Combined three-sample pores + sand visualization saved to {output_file}")
    plt.close()
    print(
        f"Combined three-sample pores + sand visualization saved to {output_file}")
    plt.close()
    plt.close()
