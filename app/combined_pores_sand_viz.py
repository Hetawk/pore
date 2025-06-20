#!/usr/bin/env python3
"""
Combined pores and sand/dust visualization module.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from tqdm import tqdm
from .utils import plot_orange_prism_frame, setup_clean_axes, generate_realistic_pores


def create_combined_pores_sand_visualization(diam, intr, sample_name, output_file, sample_color='jet'):
    """Create visualization combining realistic pores with sand/dust fill"""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    print(
        f"\nCreating combined pores + sand visualization for {sample_name}...")

    # Setup clean axes
    setup_clean_axes(ax)

    # Draw orange prism frame
    plot_orange_prism_frame(ax)

    # 1. First, add sand/dust fill with high visibility
    print(f"Adding sand/dust background for {sample_name}...")

    # Generate more sand particles for better visibility (similar to sand_dust_viz.py)
    total_porosity = np.sum(intr)
    base_particles = 6000  # Increased for better visibility
    sand_particle_count = int(base_particles * (1 + total_porosity / 10))

    # Use full bounds like in sand_dust_viz.py
    x_sand = np.random.uniform(-2.0, 2.0, sand_particle_count)
    y_sand = np.random.uniform(-0.5, 0.5, sand_particle_count)
    z_sand = np.random.uniform(-0.5, 0.5, sand_particle_count)

    # Create particle characteristics based on intrusion data (like sand_dust_viz.py)
    norm_intrusion = intr / np.max(intr)

    # Generate sand particle properties
    sand_sizes = []
    sand_colors = []

    colormap = plt.get_cmap(sample_color)

    for j in range(sand_particle_count):
        # Map particle position to intrusion characteristics
        dist_x_norm = abs(x_sand[j]) / 2.0
        dist_y_norm = abs(y_sand[j]) / 0.5
        dist_from_center = np.sqrt((dist_x_norm**2 + dist_y_norm**2) / 2)

        # Map to intrusion data
        data_idx = min(int(dist_from_center * len(intr)), len(intr)-1)

        # Particle size based on pore characteristics (same as sand_dust_viz.py)
        base_size = 0.8 + 1.5 * norm_intrusion[data_idx]
        size_variation = np.random.uniform(0.7, 1.3)
        final_size = base_size * size_variation
        sand_sizes.append(final_size)

        # Color intensity (same as sand_dust_viz.py)
        color_intensity = 0.3 + 0.7 * norm_intrusion[data_idx]
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

    # Render sand particles with high visibility (same alpha as sand_dust_viz.py)
    batch_size = 1000
    for batch_start in range(0, len(x_sand_sorted), batch_size):
        batch_end = min(batch_start + batch_size, len(x_sand_sorted))

        ax.scatter(x_sand_sorted[batch_start:batch_end],
                   y_sand_sorted[batch_start:batch_end],
                   z_sand_sorted[batch_start:batch_end],
                   s=sizes_sand_sorted[batch_start:batch_end],
                   c=colors_sand_sorted[batch_start:batch_end],
                   alpha=0.7,  # Same high alpha as sand_dust_viz.py
                   edgecolors='none')

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

    # Render pores as spheres (with higher alpha to stand out from sand)
    print(f"Rendering {len(pore_positions)} pores for {sample_name}...")
    for i in tqdm(range(len(pore_positions)), desc="Rendering pores"):
        radius = scaled_radii[i]
        # Higher intensity for visibility
        color = colormap(0.8 + 0.2 * norm(radius))

        # Create a sphere for each pore
        u = np.linspace(0, 2 * np.pi, 10)  # Lower resolution for performance
        v = np.linspace(0, np.pi, 6)
        x = pore_positions[i, 0] + radius * np.outer(np.cos(u), np.sin(v))
        y = pore_positions[i, 1] + radius * np.outer(np.sin(u), np.sin(v))
        z = pore_positions[i, 2] + radius * \
            np.outer(np.ones(np.size(u)), np.cos(v))

        ax.plot_surface(x, y, z, color=color, shade=True, alpha=0.95,
                        rstride=1, cstride=1, linewidth=0)

    # Set title
    ax.set_title(f"{sample_name}: Pores + Sand/Dust Fill",
                 fontsize=12, color='#333333', weight='bold')

    # Add sample information
    ax.text2D(0.05, 0.95, sample_name, transform=ax.transAxes, fontsize=12,
              fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

    # Add information text
    info_text = (f"Combined visualization: Realistic pores within sand/dust-filled {sample_name} board.\n"
                 f"Shows both major pore structures and fine granular material matrix.")
    plt.figtext(0.5, 0.02, info_text, ha='center', fontsize=9,
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Combined pores + sand visualization saved to {output_file}")
    plt.close()


def create_combined_three_samples_pores_sand_visualization(diam1, intr1, diam2, intr2, diam3, intr3, output_file):
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

        # Add sand/dust background with high visibility
        total_porosity = np.sum(intrusion)
        base_particles = 4000  # Fewer for combined view but still visible
        sand_particle_count = int(base_particles * (1 + total_porosity / 15))

        x_sand = np.random.uniform(-2.0, 2.0, sand_particle_count)
        y_sand = np.random.uniform(-0.5, 0.5, sand_particle_count)
        z_sand = np.random.uniform(-0.5, 0.5, sand_particle_count)

        # Create particle characteristics like sand_dust_viz.py
        norm_intrusion = intrusion / np.max(intrusion)

        sand_sizes = []
        sand_colors = []
        colormap = plt.get_cmap(cmap_name)

        for j in range(sand_particle_count):
            # Map particle position to intrusion characteristics
            dist_x_norm = abs(x_sand[j]) / 2.0
            dist_y_norm = abs(y_sand[j]) / 0.5
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
            color_intensity = 0.25 + 0.6 * norm_intrusion[data_idx]
            sand_colors.append(colormap(color_intensity))

        # Sort and render with high visibility
        sand_distances = np.sqrt(x_sand**2 + y_sand**2 + z_sand**2)
        sand_sort_indices = np.argsort(-sand_distances)

        x_sand_sorted = x_sand[sand_sort_indices]
        y_sand_sorted = y_sand[sand_sort_indices]
        z_sand_sorted = z_sand[sand_sort_indices]
        sizes_sand_sorted = np.array(sand_sizes)[sand_sort_indices]
        colors_sand_sorted = np.array(sand_colors)[sand_sort_indices]

        # Render with higher alpha for visibility
        ax.scatter(x_sand_sorted, y_sand_sorted, z_sand_sorted,
                   s=sizes_sand_sorted, c=colors_sand_sorted,
                   alpha=0.6, edgecolors='none')  # Increased from 0.3 to 0.6

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

        # Set title
        ax.set_title(
            f"{name}: {descriptions[i]}", fontsize=10, color='#333333', weight='bold')

    # Add overall title
    plt.suptitle('Combined Pores + Sand/Dust Visualization',
                 fontsize=16, fontweight='bold', color='#333333', y=0.95)

    # Add information text
    info_text = ("Combined visualization showing realistic pores within sand/dust-filled thermal boards.\n"
                 "Demonstrates both macro-pore structures and fine granular material composition.")
    plt.figtext(0.5, 0.02, info_text, ha='center', fontsize=10,
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))

    plt.tight_layout()
    plt.subplots_adjust(top=0.88, bottom=0.12)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(
        f"Combined three-sample pores + sand visualization saved to {output_file}")
    plt.close()
