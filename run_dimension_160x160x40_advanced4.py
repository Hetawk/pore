#!/usr/bin/env python3
"""
Special wrapper script for 160×160×40mm configuration with multi-color pores,
advanced analysis v4, and custom colorbar using pore colors.
"""

import main
from app.config import MaterialConfig, CONFIG, set_configuration
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Set environment variables
os.environ["DIMENSION_OVERRIDE"] = "true"
os.environ["MULTI_COLOR_PORES"] = "true"
os.environ["CUSTOM_COLORBAR"] = "true"
os.environ["ADVANCED_ANALYSIS"] = "true"

print("Applying dimension override (160×160×40mm) with multi-color pores, advanced analysis v4, and custom colorbar...")

# Store original function
original_load_default_config = MaterialConfig._load_default_config


def custom_160x160x40_advanced4_config(self):
    # First call original to get all default settings
    original_load_default_config(self)

    # Apply 160×160×40mm dimensions (default dimensions)
    self.board_length_mm = 160.0
    self.board_width_mm = 160.0
    self.board_thickness_mm = 40.0

    # Update coordinate scaling (standard aspect ratio)
    self.length_scale = 2.0
    self.width_scale = 2.0
    self.thickness_scale = 0.5
    self.aspect_ratio = [4, 4, 1]

    # Adjust visualization limits (expanded to prevent cutoff)
    self.x_limits = (-2.2, 2.2)
    self.y_limits = (-2.2, 2.2)
    self.z_limits = (-0.6, 0.6)

    # Matrix boundaries (slightly smaller than limits to ensure full visibility)
    self.matrix_fill_x_bounds = (-2.0, 2.0)
    self.matrix_fill_y_bounds = (-2.0, 2.0)
    self.matrix_fill_z_bounds = (-0.5, 0.5)

    # Particle distribution (matching matrix bounds)
    self.matrix_length_norm = 2.0
    self.matrix_width_norm = 2.0
    self.default_x_bounds = (-2.0, 2.0)
    self.default_y_bounds = (-2.0, 2.0)
    self.default_z_bounds = (-0.5, 0.5)

    # Camera and view settings (adjusted for better full view)
    self.camera_position = np.array([3.0, 3.0, 1.2])
    self.view_elevation = 25
    self.view_azimuth = 50

    # Standard pore counts (default volume)
    self.n_pores_individual = 600
    self.n_pores_comparative = 400
    self.n_pores_density = 500
    self.n_pores_matrix = 800
    self.n_pores_hybrid = 800

    # Standard particle counts
    self.base_particles_matrix = 15000
    self.base_particles_hybrid_main = 8000
    self.base_particles_hybrid_combined = 5000

    # MULTI-COLOR PORE SETTINGS (size-based with custom colorbar)
    self.micropore_color = "#FF1493"  # Deep pink (Micropores)
    self.mesopore_color = "#FFFF00"   # Bright yellow (Mesopores)
    self.macropore_color = "#00FFFF"  # Bright cyan (Macropores)

    # Custom colorbar settings using pore colors
    self.use_custom_colorbar = True
    self.custom_colorbar_colors = [
        self.micropore_color, self.mesopore_color, self.macropore_color]
    self.custom_colorbar_labels = ['Micropores', 'Mesopores', 'Macropores']

    # ADVANCED ANALYSIS SETTINGS (from advanced configuration)
    self.enable_advanced_analysis = True
    self.advanced_analysis = True
    self.advanced_colormap = "custom"  # Use custom colormap instead of jet
    self.advanced_tick_count = 8
    self.advanced_bins = 30

    # Enhanced advanced analysis parameters
    self.advanced_stats_position = (0.5, 0.95)
    self.advanced_colorbar_colormap = 'custom'
    self.advanced_colorbar_position = 'right'
    self.advanced_plot_padding = 0.15
    self.advanced_colorbar_formatter = '%.2e'

    # Matrix settings to match advanced
    self.matrix_fill_color = "#333333"
    self.matrix_alpha = 0.1

    # Enable legends for size-based colors
    self.show_legends = False  # Disable legends for advanced4
    self.show_legend = False
    self.enable_legends = False

    # Visualization settings
    self.pore_alpha = 1.0
    self.alpha = 1.0
    self.dpi = 300
    self.figure_size = (12, 8)  # Landscape for flat board

    print("\nSimple Pore Analysis - Advanced v4 with Multi-Color Pores and Custom Colorbar")
    print("=============================================================================")
    print("160×160×40mm board configuration applied:")
    print(
        f"  - Board dimensions: {self.board_length_mm:.1f} × {self.board_width_mm:.1f} × {self.board_thickness_mm:.1f} mm")
    print(
        f"  - Pore counts: Individual={self.n_pores_individual}, Comparative={self.n_pores_comparative}")
    print("  - Visualization features:")
    print("    * Three distinct pore colors (Red/Green/Blue)")
    print("    * Custom colorbar using pore colors")
    print("    * Advanced statistical analysis enabled")
    print("    * Volume histogram and sphericity analysis")
    print("    * Size-based legends displayed")


# Replace the config method
MaterialConfig._load_default_config = custom_160x160x40_advanced4_config

# Execute main first
result = main.main()

# After main execution, manually create the advanced analysis files with custom colorbar
try:
    from app.advanced_pore_analysis import create_advanced_pore_analysis
    from app.data_processor import load_and_clean_data

    print("[DEBUG] Manually generating advanced analysis v4 files...")

    # Load the data with the correct filename
    data_filename = "dataset/pore_data.csv"
    data = load_and_clean_data(data_filename)
    if data is not None:
        print(f"[DEBUG] Data loaded, type: {type(data)}, shape: {data.shape}")
        print(f"[DEBUG] Data columns: {list(data.columns)}")

        # Extract data for each sample from the DataFrame
        try:
            if 'diam_T1' in data.columns and 'int_T1' in data.columns:
                diam1 = data['diam_T1'].values
                intr1 = data['int_T1'].values
                diam2 = data['diam_T2'].values
                intr2 = data['int_T2'].values
                diam3 = data['diam_T3'].values
                intr3 = data['int_T3'].values
                print(
                    "[DEBUG] Successfully extracted data using diam_T1/int_T1 pattern")
            else:
                # Fallback to column indices
                columns = list(data.columns)
                diam1 = data[columns[0]].values
                intr1 = data[columns[1]].values
                diam2 = data[columns[3]].values
                intr2 = data[columns[4]].values
                diam3 = data[columns[6]].values
                intr3 = data[columns[7]].values
                print(
                    f"[DEBUG] Extracted data from columns: {[columns[0], columns[1], columns[3], columns[4], columns[6], columns[7]]}")
        except Exception as e:
            print(f"[DEBUG] Failed to extract data from DataFrame: {e}")
            raise

        # Generate advanced analysis for each sample with multi-color pores
        samples = [
            (diam1, intr1, 'T1'),
            (diam2, intr2, 'T2'),
            (diam3, intr3, 'T3')
        ]

        for diam, intr, sample_name in samples:
            output_file = f"out/{sample_name}_advanced_v4_analysis.png"
            print(f"[DEBUG] Creating advanced analysis v4 for {sample_name}")
            print(
                f"[DEBUG] Data shapes - diam: {len(diam)}, intr: {len(intr)}")

            # Ensure multi-color pore settings are active (not single-color)
            CONFIG.micropore_color = "#FF0000"  # Red
            CONFIG.mesopore_color = "#00FF00"   # Green
            CONFIG.macropore_color = "#0000FF"  # Blue

            # Remove any sample-specific color override for this version
            if hasattr(CONFIG, 'sample_pore_colors'):
                delattr(CONFIG, 'sample_pore_colors')

            print(
                f"[DEBUG] Using multi-color pores for {sample_name}: Red/Green/Blue")

            # Create the advanced analysis with timeout protection
            try:
                import signal

                def timeout_handler(signum, frame):
                    raise TimeoutError("Advanced analysis rendering timeout")

                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(120)

                print(
                    f"[DEBUG] Starting advanced analysis v4 rendering for {sample_name}...")
                create_advanced_pore_analysis(
                    diam, intr, sample_name, output_file)

                signal.alarm(0)

            except TimeoutError:
                print(
                    f"[DEBUG] Advanced analysis v4 for {sample_name} timed out, skipping")
                continue
            except Exception as rendering_error:
                print(
                    f"[DEBUG] Advanced analysis v4 rendering failed for {sample_name}: {rendering_error}")
                continue
            finally:
                signal.alarm(0)

            print(f"[DEBUG] Advanced analysis v4 saved: {output_file}")
    else:
        print("[DEBUG] Could not load data for advanced analysis v4")

except Exception as e:
    print(f"[DEBUG] Failed to create advanced analysis v4 files: {e}")
    import traceback
    traceback.print_exc()

# Exit with the result from main
sys.exit(result)
