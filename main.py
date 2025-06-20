#!/usr/bin/env python3
"""
Comprehensive 3D Pore Visualization System - Main Entry Point
Clean, modular structure with organized output directory.
"""

import os
from app.data_processor import load_and_clean_data, sort_by_diameter
from app.individual_viz import create_individual_sample_visualization
from app.combined_viz import create_combined_three_samples_visualization
from app.density_viz import create_density_filled_visualization
from app.sand_dust_viz import create_sand_dust_filled_visualization
from app.combined_pores_sand_viz import (
    create_combined_pores_sand_visualization,
    create_combined_three_samples_pores_sand_visualization
)


def main():
    """Main function to run all visualizations"""
    print("=== Comprehensive 3D Pore Visualization System ===")
    print("Clean modular structure with organized output")

    # Data file path - now in dataset directory
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
    print("Creating individual sample visualizations...")
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

    # 2. Create combined three-sample visualization
    print("\n" + "="*60)
    print("Creating combined three-sample visualization...")
    print("="*60)
    
    create_combined_three_samples_visualization(
        diam1, intr1, diam2, intr2, diam3, intr3,
        os.path.join(output_dir, "combined_three_samples_clean.png"))

    # 3. Create density-filled visualization
    print("\n" + "="*60)
    print("Creating density-filled visualization...")
    print("="*60)
    
    create_density_filled_visualization(
        diam1, intr1, diam2, intr2, diam3, intr3,
        os.path.join(output_dir, "density_filled_clean.png"))

    # 4. Create sand/dust-filled visualization
    print("\n" + "="*60)
    print("Creating sand/dust-filled visualization...")
    print("="*60)
    
    create_sand_dust_filled_visualization(
        diam1, intr1, diam2, intr2, diam3, intr3,
        os.path.join(output_dir, "sand_dust_filled_clean.png"))

    # 5. Create individual combined pores + sand visualizations
    print("\n" + "="*60)
    print("Creating individual pores + sand visualizations...")
    print("="*60)
    
    create_combined_pores_sand_visualization(
        diam1, intr1, "T1", 
        os.path.join(output_dir, "T1_pores_sand_combined.png"), 'Reds')
    
    create_combined_pores_sand_visualization(
        diam2, intr2, "T2", 
        os.path.join(output_dir, "T2_pores_sand_combined.png"), 'Blues')
    
    create_combined_pores_sand_visualization(
        diam3, intr3, "T3", 
        os.path.join(output_dir, "T3_pores_sand_combined.png"), 'Oranges')

    # 6. Create combined three-sample pores + sand visualization
    print("\n" + "="*60)
    print("Creating combined three-sample pores + sand visualization...")
    print("="*60)
    
    create_combined_three_samples_pores_sand_visualization(
        diam1, intr1, diam2, intr2, diam3, intr3,
        os.path.join(output_dir, "combined_pores_sand_filled.png"))

    # Final summary
    print("\n" + "="*80)
    print("=== ALL VISUALIZATIONS COMPLETED SUCCESSFULLY! ===")
    print("="*80)
    print(f"All output files have been saved to the '{output_dir}/' directory:")
    print()
    print("Individual Sample Visualizations:")
    print("  - T1_individual_clean.png")
    print("  - T2_individual_clean.png")
    print("  - T3_individual_clean.png")
    print()
    print("Combined Visualizations:")
    print("  - combined_three_samples_clean.png")
    print("  - density_filled_clean.png")
    print("  - sand_dust_filled_clean.png")
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
