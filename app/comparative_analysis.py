#!/usr/bin/env python3
"""
Comparative pore structure analysis module for CSA cement-based insulating boards.

Generates side-by-side computational models enabling direct comparison of pore
characteristics across different board compositions (T1, T2, T3) to evaluate
the effects of agricultural waste additives on pore structure.
"""

import matplotlib.pyplot as plt
from .individual_board_modeling import create_clean_pore_visualization


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
    create_clean_pore_visualization(ax1, diam1, intr1, "T1", 'Blues')
    create_clean_pore_visualization(ax2, diam2, intr2, "T2", 'Greens')
    create_clean_pore_visualization(ax3, diam3, intr3, "T3", 'Oranges')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Combined visualization saved to {output_file}")
    plt.close()
    """
    Create comparative analysis visualization of all three board compositions.

    Generates simultaneous 3D models of T1, T2, and T3 board pore structures
    for direct comparison of the effects of different agricultural waste
    additives on pore size distribution and spatial organization.

    Parameters:
    -----------
    diam1, diam2, diam3 : array_like
        Experimental pore diameter data for T1, T2, and T3 boards
    intr1, intr2, intr3 : array_like  
        Mercury intrusion volume data for T1, T2, and T3 boards
    output_file : str
        Path for saving the comparative analysis visualization
    """
    fig = plt.figure(figsize=(18, 7))

    # Create subplots for comparative analysis
    ax1 = fig.add_subplot(131, projection='3d')
    ax2 = fig.add_subplot(132, projection='3d')
    ax3 = fig.add_subplot(133, projection='3d')

    # Board composition descriptions for reference
    compositions = [
        "T1: CSA cement + expanded vermiculite",
        "T2: CSA cement + vermiculite + rice husk ash",
        "T3: CSA cement + vermiculite + rice husk ash + moso bamboo fiber"
    ]

    # Generate comparative models with distinct colormaps for differentiation
    create_clean_pore_visualization(ax1, diam1, intr1, "T1", 'Blues')
    create_clean_pore_visualization(ax2, diam2, intr2, "T2", 'Greens')
    create_clean_pore_visualization(ax3, diam3, intr3, "T3", 'Oranges')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Comparative board analysis saved to {output_file}")
    plt.close()
