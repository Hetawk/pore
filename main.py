#!/usr/bin/env python3
"""
Comprehensive 3D Pore Structure Modeling System for CSA Cement-Based Insulating Boards

Main computational modeling script for experimental thermal insulating board characterization.
Generates advanced 3D visualizations and analysis of pore structures based on 
mercury intrusion porosimetry data from calcium sulfoaluminate cement boards 
with agricultural waste components.
"""

import os
from app.data_processor import load_and_clean_data, sort_by_diameter
from app.individual_board_modeling import create_individual_sample_visualization
from app.comparative_analysis import create_combined_three_samples_visualization
from app.density_distribution_modeling import create_density_filled_visualization
from app.matrix_material_modeling import create_matrix_filled_visualization
from app.hybrid_pore_matrix_modeling import (
    create_combined_pores_matrix_visualization,
    create_combined_three_samples_pores_matrix_visualization
)


def main():
    """
    Main computational modeling function for thermal insulating board analysis.

    Executes comprehensive 3D pore structure modeling pipeline including:
    - Individual board composition analysis (T1, T2, T3)
    - Comparative pore structure analysis  
    - Density-based pore distribution modeling
    - Matrix-filled space visualization
    - Hybrid pore-matrix computational models
    """
    print("=== 3D Pore Structure Modeling for CSA Cement-Based Insulating Boards ===")
    print("Advanced computational analysis with experimental MIP data integration")

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
        os.path.join(output_dir, "combined_three_samples_clean.png"))

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
