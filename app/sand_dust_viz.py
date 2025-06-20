#!/usr/bin/env python3
"""
Sand/dust-filled visualization module.
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from .utils import plot_orange_prism_frame, setup_clean_axes


def create_sand_dust_filled_visualization(diam1, intr1, diam2, intr2, diam3, intr3, output_file):
    """Create visualization with sand/dust-like particle fill inside orange prism frames"""
    fig = plt.figure(figsize=(20, 8))

    # Create subplots
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

        # Create sand/dust particles with varying sizes and density
        # More particles for samples with different characteristics
        base_particles = 12000  # Increased base number of particles for complete fill
        particle_count = int(base_particles * (1 + total_porosity /
                             np.max([np.sum(intr1), np.sum(intr2), np.sum(intr3)])))

        print(f"Creating {particle_count} sand/dust particles for {name}...")

        # Generate particle positions throughout the entire volume - fill completely
        # Use the exact bounds of the orange prism: X: [-2.0, 2.0], Y: [-0.5, 0.5], Z: [-0.5, 0.5]
        x_positions = np.random.uniform(-2.0, 2.0, particle_count)
        y_positions = np.random.uniform(-0.5, 0.5, particle_count)
        z_positions = np.random.uniform(-0.5, 0.5, particle_count)

        # Create particle sizes - very small like sand/dust
        # Vary sizes based on intrusion characteristics
        norm_intrusion = intrusion / np.max(intrusion)

        # Create size distribution based on pore characteristics
        particle_sizes = []
        particle_colors = []

        for j in tqdm(range(particle_count), desc=f"Generating {name} particles"):
            # Map particle position to intrusion characteristics
            # Use distance from center to determine particle properties
            dist_x_norm = abs(x_positions[j]) / 2.0  # Updated for full bounds
            dist_y_norm = abs(y_positions[j]) / 0.5  # Updated for full bounds
            dist_from_center = np.sqrt((dist_x_norm**2 + dist_y_norm**2) / 2)

            # Map to intrusion data
            data_idx = min(
                int(dist_from_center * len(intrusion)), len(intrusion)-1)

            # Particle size based on local pore characteristics
            # Very small particles
            base_size = 0.8 + 1.5 * norm_intrusion[data_idx]
            size_variation = np.random.uniform(0.7, 1.3)  # Random variation
            final_size = base_size * size_variation

            particle_sizes.append(final_size)

            # Color based on density and position
            color_intensity = 0.3 + 0.7 * norm_intrusion[data_idx]
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
        batch_size = 1000
        for batch_start in tqdm(range(0, len(x_sorted), batch_size), desc=f"Rendering {name} batches"):
            batch_end = min(batch_start + batch_size, len(x_sorted))

            ax.scatter(x_sorted[batch_start:batch_end],
                       y_sorted[batch_start:batch_end],
                       z_sorted[batch_start:batch_end],
                       s=sizes_sorted[batch_start:batch_end],
                       c=colors_sorted[batch_start:batch_end],
                       alpha=0.7,
                       edgecolors='none')

        # Set title
        ax.set_title(f"{name}: Sand/Dust-Filled Board", fontsize=11,
                     color='#333333', weight='bold')

    # Add overall title and info
    plt.suptitle('Sand/Dust-Filled Thermal Board Visualization',
                 fontsize=16, fontweight='bold', color='#333333', y=0.95)

    # Add information text
    info_text = ("Dense sand/dust-like particle fill representing material composition.\n"
                 "Particle density and size variation based on pore distribution characteristics.")
    plt.figtext(0.5, 0.02, info_text, ha='center', fontsize=10,
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))

    plt.tight_layout()
    plt.subplots_adjust(top=0.88, bottom=0.12)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Sand/dust-filled visualization saved to {output_file}")
    plt.close()
