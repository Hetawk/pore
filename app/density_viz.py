#!/usr/bin/env python3
"""
Density-filled visualization module.
"""

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from .utils import plot_orange_prism_frame, setup_clean_axes


def create_density_filled_visualization(diam1, intr1, diam2, intr2, diam3, intr3, output_file):
    """Create visualization with realistic density fill inside orange prism frames"""
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

        print(f"\nGenerating density fill for {name}...")

        # Setup clean axes
        setup_clean_axes(ax)

        # Draw orange prism frame
        plot_orange_prism_frame(ax)

        # Calculate overall porosity metric for this sample
        total_porosity = np.sum(intrusion)
        mean_pore_size = np.mean(diameters)

        # Create multiple horizontal layers with varying density
        n_layers = 25
        # Updated for new Z dimension
        layer_heights = np.linspace(-0.4, 0.4, n_layers)

        # Create density variation based on pore characteristics
        # Normalize intrusion data for color mapping
        norm_intrusion = intrusion / np.max(intrusion)

        # Create a density profile that varies with height and radial distance
        for layer_idx in tqdm(range(n_layers-1), desc=f"Creating {name} density layers"):
            z_bottom = layer_heights[layer_idx]
            z_top = layer_heights[layer_idx + 1]
            z_mid = (z_bottom + z_top) / 2

            # Create a gradient based on height (more pores at certain levels)
            height_factor = 0.5 + 0.5 * np.sin(np.pi * (z_mid + 0.4) / 0.8)

            # Create mesh grid for this layer (rectangular shape)
            resolution_x = 40  # More resolution in X direction (160mm)
            resolution_y = 15  # Less resolution in Y direction (40mm)
            # Length dimension
            x_layer = np.linspace(-1.85, 1.85, resolution_x)
            # Width dimension
            y_layer = np.linspace(-0.35, 0.35, resolution_y)
            X_layer, Y_layer = np.meshgrid(x_layer, y_layer)

            # Create density values for this layer
            density_values = np.zeros_like(X_layer)

            for i_y in range(resolution_y):
                for i_x in range(resolution_x):
                    # Calculate distance from center (considering rectangular shape)
                    # Normalize distances based on the actual dimensions
                    # Normalize by length
                    dist_x_norm = abs(X_layer[i_y, i_x]) / 1.85
                    # Normalize by width
                    dist_y_norm = abs(Y_layer[i_y, i_x]) / 0.35

                    # Combined distance metric for rectangular shape
                    dist_from_center = np.sqrt(
                        (dist_x_norm**2 + dist_y_norm**2) / 2)

                    # Map distance to intrusion data index
                    data_idx = min(
                        int(dist_from_center * len(intrusion)), len(intrusion)-1)

                    # Create density based on intrusion value, height, and some randomness
                    base_density = norm_intrusion[data_idx]

                    # Add height variation and some turbulence
                    turbulence = 0.8 + 0.4 * np.random.random()
                    radial_factor = 1.0 - 0.3 * dist_from_center  # More dense toward center

                    final_density = base_density * height_factor * radial_factor * turbulence
                    density_values[i_y, i_x] = final_density

            # Only show regions with significant density
            mask = density_values > 0.3

            if np.any(mask):
                # Create the filled surface for this layer
                Z_bottom = np.full_like(X_layer, z_bottom)
                Z_top = np.full_like(X_layer, z_top)

                # Apply mask to coordinates
                X_masked = X_layer[mask]
                Y_masked = Y_layer[mask]
                Z_bottom_masked = Z_bottom[mask]
                Z_top_masked = Z_top[mask]
                density_masked = density_values[mask]

                # Create color mapping
                colors_layer = cmap(density_masked)

                # Draw individual volume elements as small boxes
                for j in range(len(X_masked)):
                    if density_masked[j] > 0.4:  # Only draw significant density
                        # Create a small box representing the density
                        # Size based on density and adapted for rectangular shape
                        # Smaller in length
                        box_size_x = 0.04 * (1 + density_masked[j])
                        # Smaller in width
                        box_size_y = 0.03 * (1 + density_masked[j])

                        # Box corners
                        x_center, y_center = X_masked[j], Y_masked[j]
                        z_center = (Z_bottom_masked[j] + Z_top_masked[j]) / 2

                        # Draw a small element to represent density
                        ax.scatter(x_center, y_center, z_center,
                                   s=30 * density_masked[j],  # Adjusted size
                                   c=[colors_layer[j]],
                                   alpha=0.6,
                                   edgecolors='none')

        # Set title
        ax.set_title(f"{name}: Density-Filled Pore Distribution", fontsize=11,
                     color='#333333', weight='bold')

    # Add overall title and info
    plt.suptitle('Density-Filled Pore Distribution Analysis',
                 fontsize=16, fontweight='bold', color='#333333', y=0.95)

    # Add information text
    info_text = ("Layered density visualization showing pore distribution patterns.\n"
                 "Density varies based on experimental intrusion data and spatial distribution.")
    plt.figtext(0.5, 0.02, info_text, ha='center', fontsize=10,
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))

    plt.tight_layout()
    plt.subplots_adjust(top=0.88, bottom=0.12)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Density-filled visualization saved to {output_file}")
    plt.close()
