#!/usr/bin/env python3
"""
Advanced pore analysis visualization module.

Generates detailed statistical visualizations of pore properties including
3D distribution with volume-based coloring and diameter/sphericity histograms.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import os
from tqdm import tqdm
from . import config
from .utils import setup_clean_axes, generate_realistic_pores, plot_orange_prism_frame
import matplotlib.lines as mlines


def calculate_pore_properties(positions, radii):
    """Calculate advanced properties of pores including volume and sphericity."""
    # Calculate volumes (4/3 * pi * r^3)
    volumes = (4/3) * np.pi * (radii**3)

    # Generate simulated sphericity values (normally ~0.6-0.7 with some variation)
    # In a real implementation, this would be calculated from actual pore shapes
    sphericity = 0.65 + 0.05 * np.random.randn(len(radii))
    sphericity = np.clip(sphericity, 0.1, 1.0)

    # Convert radii to equivalent diameters (2*r)
    diameters = 2 * radii * 1000  # Convert to μm for better visualization

    return volumes, sphericity, diameters


def create_advanced_pore_analysis(diam, intr, sample_name, output_file):
    """Create advanced pore analysis visualization with statistical distributions."""
    # Get configuration
    current_config = config.get_config()

    # Generate pore data
    pore_positions, scaled_radii, _ = generate_realistic_pores(
        # Use more pores for statistical significance
        diam, intr, sample_name, n_pores=800)

    # Calculate pore properties
    volumes, sphericity, diameters = calculate_pore_properties(
        pore_positions, scaled_radii)

    # Create figure with grid layout (3D view on top, histogram below)
    fig = plt.figure(figsize=(10, 12))
    gs = GridSpec(2, 1, height_ratios=[1.5, 1])

    # 3D pore visualization
    ax1 = fig.add_subplot(gs[0], projection='3d')
    setup_clean_axes(ax1)

    # Set white background for better contrast
    ax1.set_facecolor('white')
    fig.patch.set_facecolor('white')

    # Add orange prism frame to maintain consistency with other visualizations
    plot_orange_prism_frame(ax1)

    # Add matrix fill to match the style of pores_matrix_combined visualizations
    matrix_params = current_config.get_matrix_parameters()
    dimension_scales = current_config.get_dimension_scale_factors()
    particle_counts = current_config.get_particle_counts()

    x_min, x_max = matrix_params['x_bounds']
    y_min, y_max = matrix_params['y_bounds']
    z_min, z_max = matrix_params['z_bounds']
    length_norm = matrix_params['length_norm']
    width_norm = matrix_params['width_norm']

    # Generate matrix particles similar to hybrid_pore_matrix_modeling.py
    total_porosity = np.sum(intr)
    base_particles = int(
        particle_counts['hybrid_main'] * dimension_scales['volume_scale'])
    sand_particle_count = int(base_particles * (1 + total_porosity / 10))

    # Generate sand particle coordinates
    x_sand = np.random.uniform(x_min, x_max, sand_particle_count)
    y_sand = np.random.uniform(y_min, y_max, sand_particle_count)
    z_sand = np.random.uniform(z_min, z_max, sand_particle_count)

    # Create particle characteristics based on intrusion data
    norm_intrusion = intr / np.max(intr)

    # Generate sand particle properties
    sand_sizes = []
    sand_colors = []

    # Use a sample-specific colormap as in the original implementation
    sample_colormaps = {'T1': 'Reds', 'T2': 'Blues', 'T3': 'Oranges'}
    colormap = plt.get_cmap(sample_colormaps.get(sample_name, 'viridis'))

    for j in range(sand_particle_count):
        # Map particle position to intrusion characteristics
        dist_x_norm = abs(x_sand[j]) / length_norm
        dist_y_norm = abs(y_sand[j]) / width_norm
        dist_from_center = np.sqrt((dist_x_norm**2 + dist_y_norm**2) / 2)

        # Map to intrusion data
        data_idx = min(int(dist_from_center * len(intr)), len(intr)-1)

        # Particle size based on pore characteristics
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

    # Render sand particles with high visibility
    batch_size = matrix_params['batch_size']
    for batch_start in range(0, len(x_sand_sorted), batch_size):
        batch_end = min(batch_start + batch_size, len(x_sand_sorted))

        ax1.scatter(x_sand_sorted[batch_start:batch_end],
                    y_sand_sorted[batch_start:batch_end],
                    z_sand_sorted[batch_start:batch_end],
                    s=sizes_sand_sorted[batch_start:batch_end],
                    c=colors_sand_sorted[batch_start:batch_end],
                    alpha=matrix_params['particle_alpha'],
                    edgecolors='none')

    # Calculate average porosity for title
    total_volume = (current_config.board_length_mm/1000) * \
        (current_config.board_width_mm/1000) * \
        (current_config.board_thickness_mm/1000)
    porosity = np.sum(volumes) / total_volume * 100  # as percentage

    # Set title with porosity
    ax1.set_title(f"{sample_name}: Porosity {porosity:.1f}%", fontsize=14)

    # Setup 3D axes with labels
    ax1.set_xlabel(f"{current_config.board_length_mm/2} mm", labelpad=10)
    ax1.set_ylabel(f"{current_config.board_width_mm/2} mm", labelpad=10)
    ax1.set_zlabel(f"{current_config.board_thickness_mm} mm", labelpad=10)

    # Remove ticks for clean look
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_zticks([])

    # Set up camera position for depth sorting
    camera_pos = np.array([3.0, 1.0, 1.0])

    # Sort pores by distance from camera for proper rendering
    distances = np.linalg.norm(
        pore_positions - camera_pos.reshape(1, 3), axis=1)
    z_bonus = pore_positions[:, 2] / 0.4 * 0.2 * np.max(distances)
    adjusted_distances = distances - z_bonus

    # Sort indices based on adjusted distances (back to front)
    sort_indices = np.argsort(-adjusted_distances)
    pore_positions = pore_positions[sort_indices]
    scaled_radii = scaled_radii[sort_indices]
    volumes = volumes[sort_indices]

    # Get pore colors from config - same as in hybrid_pore_matrix_modeling.py
    pore_colors = current_config.get_pore_colors()

    # CHECK FOR SAMPLE-SPECIFIC COLOR OVERRIDE (for dim100color0advanced)
    if hasattr(current_config, 'sample_pore_colors') and sample_name in current_config.sample_pore_colors:
        # Use sample-specific color for all pore types (no size-based distinction)
        sample_color = current_config.sample_pore_colors[sample_name]
        micropore_color = sample_color
        mesopore_color = sample_color
        macropore_color = sample_color
        print(
            f"[DEBUG] Advanced analysis using sample-specific color for {sample_name}: {sample_color}")
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

    # Render pores using the same techniques as in hybrid_pore_matrix_modeling.py
    print(
        f"Rendering {len(pore_positions)} pores for analysis of {sample_name}...")
    for i in range(len(pore_positions)):
        radius = scaled_radii[i]

        # Use single color for all pores when sample-specific colors are enabled
        if hasattr(current_config, 'sample_pore_colors') and sample_name in current_config.sample_pore_colors:
            color = current_config.sample_pore_colors[sample_name]
        else:
            # Assign color based on pore size categories (original behavior)
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

        # Plot with same settings as hybrid visualization
        ax1.plot_surface(x, y, z, color=color, shade=True, alpha=1.0,
                         rstride=1, cstride=1, linewidth=0)

    # Get advanced visualization parameters from config
    advanced_params = current_config.get_advanced_analysis_params()

    # Create a colorbar for volume visualization
    # Check if custom colorbar is enabled
    if hasattr(current_config, 'use_custom_colorbar') and current_config.use_custom_colorbar:
        # Create smooth gradient colormap using pore colors
        from matplotlib.colors import LinearSegmentedColormap
        custom_colors = getattr(current_config, 'custom_colorbar_colors', ['#FF0000', '#00FF00', '#0000FF'])
        
        # Create a smooth gradient between the three colors
        # This creates transitions: Red -> Green -> Blue
        custom_cmap = LinearSegmentedColormap.from_list(
            'custom_pore_gradient', 
            custom_colors, 
            N=256  # Number of color steps for smooth gradient
        )
        
        volume_norm = Normalize(vmin=0, vmax=volumes.max())
        volume_sm = ScalarMappable(cmap=custom_cmap, norm=volume_norm)
        volume_sm.set_array([])
        
        print(f"[DEBUG] Using smooth gradient colorbar with colors: {custom_colors}")
    else:
        # Use 'jet' colormap for vibrant, distinct colors (original behavior)
        volume_norm = Normalize(vmin=0, vmax=volumes.max())
        volume_sm = ScalarMappable(cmap='jet', norm=volume_norm)
        volume_sm.set_array([])

    # Add colorbar that shows volume ranges
    cbar = plt.colorbar(volume_sm, ax=ax1, pad=0.1, shrink=0.7)
    cbar.set_label('Vol. mm³', rotation=270, labelpad=15, fontweight='bold')

    # Set 8 evenly spaced ticks with proper formatting
    tick_count = 8
    tick_values = np.linspace(0, volumes.max(), tick_count)
    cbar.set_ticks(tick_values)
    cbar.set_ticklabels([f"{v:.4f}" for v in tick_values])

    # Add legend for pore size categories - ONLY if not using advanced2 configuration
    if not (hasattr(current_config, 'use_custom_colorbar') and current_config.use_custom_colorbar):
        if not (hasattr(current_config, 'sample_pore_colors') and sample_name in current_config.sample_pore_colors):
            legend_handles = [
                mlines.Line2D([], [], color=micropore_color, marker='o', linestyle='None',
                              markersize=12, label='Micropore'),
                mlines.Line2D([], [], color=mesopore_color, marker='o', linestyle='None',
                              markersize=12, label='Mesopore'),
                mlines.Line2D([], [], color=macropore_color, marker='o', linestyle='None',
                              markersize=12, label='Macropore'),
            ]
            ax1.legend(handles=legend_handles, loc='upper right', title='Pore Types')
    # No legend for advanced2 configuration

    # Set viewing angle to match other visualizations
    ax1.view_init(elev=current_config.view_elevation,
                  azim=current_config.view_azimuth)

    # Plot diameter histogram with sphericity overlay
    ax2 = fig.add_subplot(gs[1])

    # Calculate statistics for text annotation
    avg_diameter = np.mean(diameters)
    avg_sphericity = np.mean(sphericity)

    # Create histogram with bins
    bins = np.linspace(0, 150, 30)  # 30 bins from 0 to 150μm
    counts, bin_edges = np.histogram(diameters, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Plot histogram bars
    bars = ax2.bar(bin_centers, counts, width=(bins[1]-bins[0])*0.9,
                   color='lightgray', edgecolor='black', alpha=0.7)

    # Add histogram envelope
    ax2.plot(bin_centers, counts, 'r-', lw=2)
    ax2.fill_between(bin_centers, counts, alpha=0.3, color='red')

    # Setup histogram labels with more frequent ticks (every 10 units)
    ax2.set_xlabel('Equivalent diameter (μm)', fontweight='bold')
    ax2.set_ylabel('Frequency Counts', fontweight='bold')
    ax2.grid(True, alpha=0.3)

    # Set x-ticks every 10 units instead of 20
    ax2.set_xticks(np.arange(0, 160, 10))

    # Add sphericity overlay on second y-axis
    ax2_right = ax2.twinx()

    # Sort diameters and corresponding sphericity for scatter plot
    sorted_indices = np.argsort(diameters)
    sorted_diameters = diameters[sorted_indices]
    sorted_sphericity = sphericity[sorted_indices]

    # Add jitter to points to avoid vertical alignment
    jitter = np.random.uniform(-1.5, 1.5, len(sorted_diameters))
    jittered_diameters = sorted_diameters + jitter

    # Plot sphericity scatter with jitter
    ax2_right.scatter(jittered_diameters, sorted_sphericity, s=10,
                      color='black', alpha=0.3, marker='o')
    ax2_right.set_ylabel('Sphericity', fontweight='bold')
    ax2_right.set_ylim(0, 1)

    # Add statistics text at the top center of the plot
    stats_text = f"Diameter: {avg_diameter:.2f} μm | Sphericity: {avg_sphericity:.2f}"
    ax2.text(0.5, 0.98, stats_text, transform=ax2.transAxes,
             fontsize=11, va='top', ha='center',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

    # Adjust layout
    plt.tight_layout()

    # # Save figure
    # plt.savefig(output_file, dpi=current_config.dpi, bbox_inches='tight')
    # print(f"Advanced pore analysis saved to {output_file}")
    # plt.close()
    # # Adjust layout
    # plt.tight_layout()

    # Save figure
    plt.savefig(output_file, dpi=current_config.dpi, bbox_inches='tight')
    print(f"Advanced pore analysis saved to {output_file}")
    plt.close()
