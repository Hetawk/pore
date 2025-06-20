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

        # Create sand/dust particles with varying sizes and density
        # More particles for samples with different characteristics
        base_particles = 15000  # Increased for better coverage of the larger 160×160×40mm volume
        particle_count = int(base_particles * (1 + total_porosity /
                             np.max([np.sum(intr1), np.sum(intr2), np.sum(intr3)])))

        print(f"Creating {particle_count} sand/dust particles for {name}...")

        # Generate particle positions throughout the entire volume - fill completely
        # Use the exact bounds of the orange prism: X: [-2.0, 2.0], Y: [-2.0, 2.0], Z: [-0.5, 0.5]
        # Fill the entire 160×160×40mm space uniformly
        # Slightly inside the frame
        x_positions = np.random.uniform(-1.95, 1.95, particle_count)
        # Full Y range for 160mm width
        y_positions = np.random.uniform(-1.95, 1.95, particle_count)
        # Full Z range for 40mm height
        z_positions = np.random.uniform(-0.45, 0.45, particle_count)

        # Create particle sizes - very small like sand/dust
        # Vary sizes based on intrusion characteristics
        norm_intrusion = intrusion / np.max(intrusion)

        # Create size distribution based on pore characteristics
        particle_sizes = []
        particle_colors = []

        for j in tqdm(range(particle_count), desc=f"Generating {name} particles"):
            # Map particle position to intrusion characteristics
            # Use distance from center to determine particle properties
            # Updated for 160mm length (normalized to [-1.95, 1.95])
            dist_x_norm = abs(x_positions[j]) / 1.95
            # Updated for 160mm width (normalized to [-1.95, 1.95])
            dist_y_norm = abs(y_positions[j]) / 1.95
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

        # Add sample label
        ax.text2D(0.05, 0.95, name, transform=ax.transAxes, fontsize=12,
                  fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Sand/dust-filled visualization saved to {output_file}")
    plt.close()
