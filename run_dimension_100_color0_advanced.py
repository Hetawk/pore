#!/usr/bin/env python3
"""
Special wrapper script for 100×100×100mm configuration with single-color pores,
advanced analysis, and no legends.
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
os.environ["SINGLE_COLOR_PORES"] = "true"
os.environ["NO_LEGENDS"] = "true"
os.environ["ADVANCED_ANALYSIS"] = "true"

# Store original legend functions and patch them
original_mpl_legend = plt.legend
original_axes_legend = matplotlib.axes.Axes.legend


def no_op_legend(*args, **kwargs):
    return None


plt.legend = no_op_legend
matplotlib.axes.Axes.legend = no_op_legend

# Patch savefig to remove legends
original_savefig = plt.savefig


def patched_savefig(fname, *args, **kwargs):
    fig = plt.gcf()
    for ax in fig.axes:
        legend = ax.get_legend()
        if legend is not None:
            legend.remove()
    return original_savefig(fname, *args, **kwargs)


plt.savefig = patched_savefig

print("Applying dimension override (100×100×100mm) with single-color pores, advanced analysis, and no legends...")

# Import configuration

# Store original function
original_load_default_config = MaterialConfig._load_default_config


def custom_100x100x100_color0_advanced_config(self):
    # First call original to get all default settings
    original_load_default_config(self)

    # Apply 100×100×100mm dimensions
    self.board_length_mm = 100.0
    self.board_width_mm = 100.0
    self.board_thickness_mm = 100.0

    # Update coordinate scaling
    self.length_scale = 1.25
    self.width_scale = 1.25
    self.thickness_scale = 1.25
    self.aspect_ratio = [1, 1, 1]

    # Adjust visualization limits
    self.x_limits = (-1.5, 1.5)
    self.y_limits = (-1.5, 1.5)
    self.z_limits = (-1.5, 1.5)

    # Matrix boundaries
    self.matrix_fill_x_bounds = (-1.2, 1.2)
    self.matrix_fill_y_bounds = (-1.2, 1.2)
    self.matrix_fill_z_bounds = (-1.2, 1.2)

    # Particle distribution
    self.matrix_length_norm = 1.2
    self.matrix_width_norm = 1.2
    self.default_x_bounds = (-1.2, 1.2)
    self.default_y_bounds = (-1.2, 1.2)
    self.default_z_bounds = (-1.2, 1.2)

    # Camera and view settings
    self.camera_position = np.array([2.0, 2.0, 2.0])
    self.view_elevation = 35
    self.view_azimuth = 45

    # Scale pore counts based on volume
    default_volume = 160 * 160 * 40
    new_volume = 100 * 100 * 100
    volume_ratio = new_volume / default_volume

    self.n_pores_individual = int(600 * volume_ratio)
    self.n_pores_comparative = int(400 * volume_ratio)
    self.n_pores_density = int(500 * volume_ratio)
    self.n_pores_matrix = int(800 * volume_ratio)
    self.n_pores_hybrid = int(800 * volume_ratio)

    # Particle counts
    self.base_particles_matrix = int(15000 * volume_ratio)
    self.base_particles_hybrid_main = int(8000 * volume_ratio)
    self.base_particles_hybrid_combined = int(5000 * volume_ratio)

    # SAMPLE-SPECIFIC COLORS (no size-based distinction)
    self.sample_pore_colors = {
        'T1': "#D62728",  # Red for T1 (matches matrix fill color pattern)
        'T2': "#1F77B4",  # Blue for T2 (matches matrix fill color pattern)
        'T3': "#FF7F0E"   # Orange for T3 (matches matrix fill color pattern)
    }
    self.use_sample_specific_colors = True

    # ADVANCED ANALYSIS SETTINGS (from advanced configuration)
    self.enable_advanced_analysis = True
    self.advanced_analysis = True
    self.advanced_colormap = "jet"
    self.advanced_tick_count = 8
    self.advanced_bins = 30

    # Enhanced advanced analysis parameters
    self.advanced_stats_position = (0.5, 0.95)
    self.advanced_colorbar_colormap = 'jet'
    self.advanced_colorbar_position = 'right'
    self.advanced_plot_padding = 0.15
    self.advanced_colorbar_formatter = '%.2e'

    # Matrix settings to match advanced
    self.matrix_fill_color = "#333333"
    self.matrix_alpha = 0.1

    # Disable all legends
    self.show_legends = False
    self.show_legend = False
    self.enable_legends = False

    # Visualization settings
    self.pore_alpha = 1.0
    self.alpha = 1.0
    self.dpi = 300
    self.figure_size = (10, 12)

    print("\nSimple Pore Analysis - Cubic Dimension with Single-Color Pores and Advanced Analysis")
    print("==============================================")
    print("100×100×100mm board configuration applied:")
    print(
        f"  - Board dimensions: {self.board_length_mm:.1f} × {self.board_width_mm:.1f} × {self.board_thickness_mm:.1f} mm")
    print(
        f"  - Pore counts: Individual={self.n_pores_individual}, Comparative={self.n_pores_comparative}")
    print("  - Visualization features:")
    print("    * Single color per sample (T1=blue, T2=green, T3=red)")
    print("    * Advanced statistical analysis enabled")
    print("    * Volume histogram and sphericity analysis")
    print("    * No legends displayed")


# Replace the config method
MaterialConfig._load_default_config = custom_100x100x100_color0_advanced_config

# Force reload configuration
if hasattr(CONFIG, '_config_name'):
    new_config = MaterialConfig(CONFIG._config_name)
    for attr_name in dir(new_config):
        if not attr_name.startswith('_'):
            setattr(CONFIG, attr_name, getattr(new_config, attr_name))
else:
    set_configuration("default")

# Remove all legend functions


def remove_all_legends():
    for fig_num in plt.get_fignums():
        fig = plt.figure(fig_num)
        for ax in fig.axes:
            if ax.get_legend() is not None:
                ax.get_legend().remove()


original_show = plt.show


def show_without_legends(*args, **kwargs):
    remove_all_legends()
    return original_show(*args, **kwargs)


plt.show = show_without_legends

# Enable advanced analysis
CONFIG.set_advanced_analysis(True)
print(
    f"[DEBUG] Advanced analysis enabled: {getattr(CONFIG, 'enable_advanced_analysis', False)}")

# Execute main first
result = main.main()

# After main execution, manually create the missing advanced analysis files
try:
    from app.advanced_pore_analysis import create_advanced_pore_analysis
    from app.data_processor import load_and_clean_data

    print("[DEBUG] Manually generating advanced analysis files...")

    # Load the data with the correct filename (same as used in main)
    data_filename = "dataset/pore_data.csv"  # Default filename
    data = load_and_clean_data(data_filename)
    if data is not None:
        print(f"[DEBUG] Data loaded, type: {type(data)}, shape: {data.shape}")
        print(f"[DEBUG] Data columns: {list(data.columns)}")

        # Extract data for each sample from the DataFrame
        # Assuming the DataFrame has columns for T1, T2, T3 diameter and intrusion data
        # Based on typical naming conventions, try different column name patterns
        try:
            # Based on the debug output, we have: 'diam_T1', 'int_T1', 'cond_T1', 'diam_T2', 'int_T2', 'cond_T2', 'diam_T3', 'int_T3', 'cond_T3'
            if 'diam_T1' in data.columns and 'int_T1' in data.columns:
                diam1 = data['diam_T1'].values
                intr1 = data['int_T1'].values
                diam2 = data['diam_T2'].values
                intr2 = data['int_T2'].values
                diam3 = data['diam_T3'].values
                intr3 = data['int_T3'].values
                print(
                    "[DEBUG] Successfully extracted data using diam_T1/int_T1 pattern")
            elif 'T1_diameter' in data.columns and 'T1_intrusion' in data.columns:
                diam1 = data['T1_diameter'].values
                intr1 = data['T1_intrusion'].values
                diam2 = data['T2_diameter'].values
                intr2 = data['T2_intrusion'].values
                diam3 = data['T3_diameter'].values
                intr3 = data['T3_intrusion'].values
                print(
                    "[DEBUG] Successfully extracted data using T1_diameter/T1_intrusion pattern")
            elif 'diameter_T1' in data.columns and 'intrusion_T1' in data.columns:
                diam1 = data['diameter_T1'].values
                intr1 = data['intrusion_T1'].values
                diam2 = data['diameter_T2'].values
                intr2 = data['intrusion_T2'].values
                diam3 = data['diameter_T3'].values
                intr3 = data['intrusion_T3'].values
                print(
                    "[DEBUG] Successfully extracted data using diameter_T1/intrusion_T1 pattern")
            else:
                # Try to extract from first 6 columns if standard naming fails
                columns = list(data.columns)
                if len(columns) >= 6:
                    diam1 = data[columns[0]].values
                    intr1 = data[columns[1]].values
                    # Skip cond_T1, use diam_T2
                    diam2 = data[columns[3]].values
                    intr2 = data[columns[4]].values  # Use int_T2
                    # Skip cond_T2, use diam_T3
                    diam3 = data[columns[6]].values
                    intr3 = data[columns[7]].values  # Use int_T3
                    print(
                        f"[DEBUG] Extracted data from correct columns: {[columns[0], columns[1], columns[3], columns[4], columns[6], columns[7]]}")
                else:
                    raise ValueError(
                        f"Insufficient columns in DataFrame: {len(columns)}")
        except Exception as e:
            print(f"[DEBUG] Failed to extract data from DataFrame: {e}")
            raise

        # Generate advanced analysis for each sample with sample-specific colors
        samples = [
            (diam1, intr1, 'T1'),
            (diam2, intr2, 'T2'),
            (diam3, intr3, 'T3')
        ]

        for diam, intr, sample_name in samples:
            output_file = f"out/{sample_name}_advanced_analysis.png"
            print(f"[DEBUG] Creating advanced analysis for {sample_name}")
            print(
                f"[DEBUG] Data shapes - diam: {len(diam)}, intr: {len(intr)}")

            # Temporarily override colors for this sample
            if hasattr(CONFIG, 'sample_pore_colors') and sample_name in CONFIG.sample_pore_colors:
                target_color = CONFIG.sample_pore_colors[sample_name]

                # Store original colors
                orig_micro = getattr(CONFIG, 'micropore_color', None)
                orig_meso = getattr(CONFIG, 'mesopore_color', None)
                orig_macro = getattr(CONFIG, 'macropore_color', None)

                # Set sample-specific colors
                CONFIG.micropore_color = target_color
                CONFIG.mesopore_color = target_color
                CONFIG.macropore_color = target_color

                print(
                    f"[DEBUG] Using sample-specific color for {sample_name}: {target_color}")

            # Create the advanced analysis with timeout protection
            try:
                import signal

                def timeout_handler(signum, frame):
                    raise TimeoutError("Advanced analysis rendering timeout")

                # Set timeout for 120 seconds (increased from 60)
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(120)

                # Call with reduced complexity to prevent hanging
                print(
                    f"[DEBUG] Starting advanced analysis rendering for {sample_name}...")
                create_advanced_pore_analysis(
                    diam, intr, sample_name, output_file)

                # Cancel timeout
                signal.alarm(0)

            except TimeoutError:
                print(
                    f"[DEBUG] Advanced analysis for {sample_name} timed out, skipping")
                continue
            except Exception as rendering_error:
                print(
                    f"[DEBUG] Advanced analysis rendering failed for {sample_name}: {rendering_error}")
                continue
            finally:
                # Always cancel any pending alarm
                signal.alarm(0)

            # Restore original colors
            if 'orig_micro' in locals() and orig_micro is not None:
                CONFIG.micropore_color = orig_micro
                CONFIG.mesopore_color = orig_meso
                CONFIG.macropore_color = orig_macro

            print(f"[DEBUG] Advanced analysis saved: {output_file}")
    else:
        print("[DEBUG] Could not load data for advanced analysis")

except Exception as e:
    print(f"[DEBUG] Failed to create advanced analysis files: {e}")
    import traceback
    traceback.print_exc()

# Exit with the result from main
sys.exit(result)
