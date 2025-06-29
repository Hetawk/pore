#!/usr/bin/env python3
"""
Comprehensive 3D Pore Structure Modeling System for CSA Cement-Based Insulating Boards

Main computational modeling script for experimental thermal insulating board characterization.
Generates advanced 3D visualizations and analysis of pore structures based on 
mercury intrusion porosimetry data from calcium sulfoaluminate cement boards 
with agricultural waste components.

Configuration System:
- Switch between 'default' (160×160×40mm boards) and 'small_specimen' (10mm diameter)
- All parameters centralized in app.config module
- Easy parameter modification without touching core analysis code
"""

import os
from app import config
from app.data_processor import load_and_clean_data, sort_by_diameter
from app.individual_board_modeling import create_individual_sample_visualization
from app.comparative_analysis import create_combined_three_samples_visualization
from app.density_distribution_modeling import create_density_filled_visualization
from app.matrix_material_modeling import create_matrix_filled_visualization
from app.hybrid_pore_matrix_modeling import (
    create_combined_pores_matrix_visualization,
    create_combined_three_samples_pores_matrix_visualization
)
from app.config import set_configuration, get_config
from app.config import set_configuration, get_config, get_board_dimensions
from app.advanced_pore_analysis import create_advanced_pore_analysis
import argparse


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="3D Pore Structure Modeling in CSA Cement Boards")

    # Advanced analysis options
    parser.add_argument('--advanced-analysis', type=str, default='false',
                        help='Enable advanced statistical analysis (true/false)')

    # Advanced visualization parameters
    parser.add_argument('--advanced-colormap', type=str,
                        help='Colormap for advanced analysis (e.g., jet, viridis)')
    parser.add_argument('--advanced-tick-count', type=int,
                        help='Number of ticks on colorbar in advanced analysis')
    parser.add_argument('--advanced-bins', type=int,
                        help='Number of bins in diameter histogram')

    # Color-related arguments
    parser.add_argument('--micropore-color', type=str,
                        help='Color for micropores')
    parser.add_argument('--mesopore-color', type=str,
                        help='Color for mesopores')
    parser.add_argument('--macropore-color', type=str,
                        help='Color for macropores')
    parser.add_argument('--matrix-fill-color', type=str,
                        help='Color for matrix fill')
    parser.add_argument('--matrix-alpha', type=float,
                        help='Alpha transparency for matrix')

    return parser.parse_args()


def main():
    """
    Main computational modeling function for thermal insulating board analysis.

    Executes comprehensive 3D pore structure modeling pipeline including:
    - Individual board composition analysis (T1, T2, T3)
    - Comparative pore structure analysis  
    - Density-based pore distribution modeling
    - Matrix material visualization
    - Hybrid pore-matrix modeling

    Configuration can be changed by modifying the CONFIG_TYPE variable below.
    """

    # === CONFIGURATION SELECTION ===
    # Change this to switch between configurations:
    # - "default": Standard 160×160×40mm boards
    # - "small_specimen": Small 10±1mm diameter specimens
    CONFIG_TYPE = "default"  # <-- CHANGE THIS FOR DIFFERENT TEST SCENARIOS

    # Apply the selected configuration
    set_configuration(CONFIG_TYPE)
    # Rename this to avoid confusion with the module name
    config_obj = get_config()

    # Display current configuration
    print(f"\n{'='*60}")
    print(
        f"3D PORE STRUCTURE MODELING - Configuration: {config_obj.config_name.upper()}")
    print(f"{'='*60}")

    board_dims = get_board_dimensions()
    print(
        f"Board dimensions: {board_dims[0]:.1f} × {board_dims[1]:.1f} × {board_dims[2]:.1f} mm")
    print(
        f"Pore counts: Individual={config_obj.n_pores_individual}, Comparative={config_obj.n_pores_comparative}")
    print(
        f"Visualization resolution: {config_obj.sphere_u_resolution}×{config_obj.sphere_v_resolution}")
    print(f"Output format: {config_obj.output_format} at {config_obj.dpi} DPI")
    print(f"{'='*60}\n")

    # Experimental mercury intrusion porosimetry data location
    filename = "dataset/pore_data.csv"

    # Check if data file exists
    if not os.path.exists(filename):
        print(f"Error: Data file '{filename}' not found!")
        print("Please ensure 'pore_data.csv' is in the dataset/ directory")
        return

    # Load and process data
    df = load_and_clean_data(filename)

    if df is None or df.empty:
        print("Error: Failed to load or process data!")
        return

    print(f"Loaded data: {len(df)} samples for each thermal board")

    # Extract and sort data for each sample
    diam1, intr1 = sort_by_diameter(df["diam_T1"].values, df["int_T1"].values)
    diam2, intr2 = sort_by_diameter(df["diam_T2"].values, df["int_T2"].values)
    diam3, intr3 = sort_by_diameter(df["diam_T3"].values, df["int_T3"].values)

    # Create output directory
    output_dir = "out"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Create individual sample visualizations
    print("\n" + "="*60)
    print("Creating individual board models...")
    print("="*60)

    create_individual_sample_visualization(
        diam1, intr1, "T1",
        os.path.join(output_dir, "T1_individual_clean.png"), 'Reds')

    create_individual_sample_visualization(
        diam2, intr2, "T2",
        os.path.join(output_dir, "T2_individual_clean.png"), 'Blues')

    create_individual_sample_visualization(
        diam3, intr3, "T3",
        os.path.join(output_dir, "T3_individual_clean.png"), 'Oranges')

    # 2. Create comparative board analysis
    print("\n" + "="*60)
    print("Creating comparative board analysis...")
    print("="*60)

    create_combined_three_samples_visualization(
        diam1, intr1, diam2, intr2, diam3, intr3,
        os.path.join(output_dir, "comparative_analysis.png"))

    # 3. Create density distribution models
    print("\n" + "="*60)
    print("Creating density distribution models...")
    print("="*60)

    create_density_filled_visualization(
        diam1, intr1, diam2, intr2, diam3, intr3,
        os.path.join(output_dir, "density_filled_clean.png"))

    # 4. Create matrix material models
    print("\n" + "="*60)
    print("Creating matrix material models...")
    print("="*60)

    create_matrix_filled_visualization(
        diam1, intr1, diam2, intr2, diam3, intr3,
        os.path.join(output_dir, "matrix_filled_clean.png"))

    # 5. Create individual hybrid pore-matrix models
    print("\n" + "="*60)
    print("Creating individual hybrid pore-matrix models...")
    print("="*60)

    create_combined_pores_matrix_visualization(
        diam1, intr1, "T1",
        os.path.join(output_dir, "T1_pores_matrix_combined.png"), 'Reds')

    create_combined_pores_matrix_visualization(
        diam2, intr2, "T2",
        os.path.join(output_dir, "T2_pores_matrix_combined.png"), 'Blues')

    create_combined_pores_matrix_visualization(
        diam3, intr3, "T3",
        os.path.join(output_dir, "T3_pores_matrix_combined.png"), 'Oranges')

    # 6. Create comprehensive hybrid models
    print("\n" + "="*60)
    print("Creating comprehensive hybrid models...")
    print("="*60)

    create_combined_three_samples_pores_matrix_visualization(
        diam1, intr1, diam2, intr2, diam3, intr3,
        os.path.join(output_dir, "combined_pores_matrix_filled.png"))

    # Get arguments
    args = parse_args()

    # Configure advanced analysis
    current_config = get_config()

    # Set colors if provided
    if args.micropore_color or args.mesopore_color or args.macropore_color:
        current_config.set_pore_colors(
            micropore=args.micropore_color,
            mesopore=args.mesopore_color,
            macropore=args.macropore_color
        )

    # Set matrix parameters if provided
    if args.matrix_fill_color:
        current_config.set_matrix_fill_color(args.matrix_fill_color)

    if args.matrix_alpha is not None:
        current_config.matrix_particle_alpha = args.matrix_alpha

    # Enable advanced analysis if requested
    enable_advanced = args.advanced_analysis.lower() in ['true', 'yes', '1']
    current_config.enable_advanced_analysis = enable_advanced

    # Set advanced visualization parameters if provided
    if args.advanced_colormap:
        current_config.advanced_colorbar_colormap = args.advanced_colormap

    if args.advanced_tick_count:
        current_config.advanced_tick_count = args.advanced_tick_count

    if args.advanced_bins:
        current_config.advanced_bins_count = args.advanced_bins

    # Advanced pore analysis if enabled
    if hasattr(current_config, 'enable_advanced_analysis') and current_config.enable_advanced_analysis:
        print("\n" + "="*60)
        print("Creating advanced statistical pore analysis...")
        print("="*60)

        create_advanced_pore_analysis(
            diam1, intr1, "T1",
            os.path.join(output_dir, "T1_advanced_analysis.png"))

        create_advanced_pore_analysis(
            diam2, intr2, "T2",
            os.path.join(output_dir, "T2_advanced_analysis.png"))

        create_advanced_pore_analysis(
            diam3, intr3, "T3",
            os.path.join(output_dir, "T3_advanced_analysis.png"))

    # Final summary
    print("\n" + "="*80)
    print("=== ALL VISUALIZATIONS COMPLETED SUCCESSFULLY! ===")
    print("="*80)
    print(
        f"All output files have been saved to the '{output_dir}/' directory:")
    print()
    print("Individual Sample Visualizations:")
    print("  - T1_individual_clean.png")
    print("  - T2_individual_clean.png")
    print("  - T3_individual_clean.png")
    print()
    print("Combined Visualizations:")
    print("  - combined_three_samples_clean.png")
    print("  - density_filled_clean.png")
    print("  - matrix_filled_clean.png")
    print()
    print("Pores + Sand Combined Visualizations:")
    print("  - T1_pores_sand_combined.png")
    print("  - T2_pores_sand_combined.png")
    print("  - T3_pores_sand_combined.png")
    print("  - combined_pores_sand_filled.png")
    print()
    print("Total: 10 visualization files created")
    print("="*80)


if __name__ == "__main__":
    main()
