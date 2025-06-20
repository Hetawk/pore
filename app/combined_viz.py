#!/usr/bin/env python3
"""
Combined visualization module for multiple samples.
"""

import matplotlib.pyplot as plt
from .individual_viz import create_clean_pore_visualization


def create_combined_three_samples_visualization(diam1, intr1, diam2, intr2, diam3, intr3, output_file):
    """Create combined visualization with all three samples"""
    fig = plt.figure(figsize=(18, 7))

    # Create subplots for each sample
    ax1 = fig.add_subplot(131, projection='3d')
    ax2 = fig.add_subplot(132, projection='3d')
    ax3 = fig.add_subplot(133, projection='3d')

    # Sample descriptions
    descriptions = [
        "CSA cement with expanded vermiculite",
        "CSA cement with expanded vermiculite and rice husk ash",
        "CSA cement with vermiculite, rice husk ash and bamboo fiber"
    ]

    # Create visualizations for each sample with different color schemes
    create_clean_pore_visualization(ax1, diam1, intr1, "T1", 'Reds',
                                    f"T1: {descriptions[0]}")
    create_clean_pore_visualization(ax2, diam2, intr2, "T2", 'Blues',
                                    f"T2: {descriptions[1]}")
    create_clean_pore_visualization(ax3, diam3, intr3, "T3", 'Oranges',
                                    f"T3: {descriptions[2]}")

    # Add overall title
    plt.suptitle('Comprehensive 3D Pore Distribution Visualization',
                 fontsize=16, fontweight='bold', color='#333333', y=0.95)

    # Add information text
    info_text = ("Realistic volumetric pore visualization with clean orange prism frames.\n"
                 "Each sample shows authentic pore distribution patterns based on experimental data.")
    plt.figtext(0.5, 0.02, info_text, ha='center', fontsize=10,
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.5'))

    plt.tight_layout()
    plt.subplots_adjust(top=0.88, bottom=0.12)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Combined visualization saved to {output_file}")
    plt.close()
