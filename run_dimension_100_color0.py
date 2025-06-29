#!/usr/bin/env python3
"""
Special wrapper script to enforce dimension override for 100×100×100mm configuration
with single-color pores instead of size-based coloring and no legends.
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

# Store original legend functions
original_mpl_legend = plt.legend
original_axes_legend = matplotlib.axes.Axes.legend

# Replace with no-op versions


def no_op_legend(*args, **kwargs):
    return None


# Apply the patches
plt.legend = no_op_legend
matplotlib.axes.Axes.legend = no_op_legend

# Patch savefig to remove any legends that might still be created
original_savefig = plt.savefig


def patched_savefig(fname, *args, **kwargs):
    # Get the current figure
    fig = plt.gcf()

    # Remove any legends from all axes
    for ax in fig.axes:
        legend = ax.get_legend()
        if legend is not None:
            legend.remove()

    # Call the original savefig
    return original_savefig(fname, *args, **kwargs)


# Apply the patch
plt.savefig = patched_savefig

print("Applying dimension override (100×100×100mm) with single-color pores and no legends...")

# Now import the configuration stuff

# Store original function for reference
original_load_default_config = MaterialConfig._load_default_config


def custom_100x100x100_color0_config(self):
    # First call original to get all default settings
    original_load_default_config(self)

    # Then override specific dimensions and related settings
    self.board_length_mm = 100.0
    self.board_width_mm = 100.0
    self.board_thickness_mm = 100.0

    # Update normalized coordinate scaling for new cubic shape
    self.length_scale = 1.25
    self.width_scale = 1.25
    self.thickness_scale = 1.25

    # Update aspect ratio for cubic shape (all equal)
    thickness_ratio = 1.0  # Equal dimensions for cube
    self.aspect_ratio = [1, 1, thickness_ratio]

    # Adjust visualization limits for the cubic shape
    self.x_limits = (-1.5, 1.5)
    self.y_limits = (-1.5, 1.5)
    self.z_limits = (-1.5, 1.5)

    # Adjust matrix fill boundaries
    self.matrix_fill_x_bounds = (-1.2, 1.2)
    self.matrix_fill_y_bounds = (-1.2, 1.2)
    self.matrix_fill_z_bounds = (-1.2, 1.2)

    # Update normalization constants for particle distribution
    self.matrix_length_norm = 1.2
    self.matrix_width_norm = 1.2

    # Adjust default coordinate bounds for particle placement
    self.default_x_bounds = (-1.2, 1.2)
    self.default_y_bounds = (-1.2, 1.2)
    self.default_z_bounds = (-1.2, 1.2)

    # Update camera position for cubic view
    self.camera_position = np.array([2.0, 2.0, 2.0])

    # Adjust view angle for better cubic board visualization
    self.view_elevation = 35
    self.view_azimuth = 45

    # Calculate the volume ratio compared to default (160×160×40)
    default_volume = 160 * 160 * 40
    new_volume = 100 * 100 * 100
    volume_ratio = new_volume / default_volume  # About 1.56

    # Scale pore counts based on volume
    self.n_pores_individual = int(600 * volume_ratio)
    self.n_pores_comparative = int(400 * volume_ratio)
    self.n_pores_density = int(500 * volume_ratio)
    self.n_pores_matrix = int(800 * volume_ratio)
    self.n_pores_hybrid = int(800 * volume_ratio)

    # Update particle counts for the new dimensions
    self.base_particles_matrix = int(15000 * volume_ratio)
    self.base_particles_hybrid_main = int(8000 * volume_ratio)
    self.base_particles_hybrid_combined = int(5000 * volume_ratio)

    # Override visualization settings to use single color

    # CRITICAL: Define a hook to override plotting in all visualization modules
    def universal_plot_override(fig):
        """Function to be called at the end of any visualization function"""
        # Remove legends from all axes
        for ax in fig.axes:
            legend = ax.get_legend()
            if legend is not None:
                legend.remove()
        return fig

    # Add the hook to the configuration
    self.post_plot_hook = universal_plot_override

    # Make uniform colors of pores by size in all plots
    # Instead of uniform blue, use sample-specific colors like combined_pores_matrix_filled.png

    # Set colors for different samples - matching combined visualization pattern
    self.sample_pore_colors = {
        'T1': "#D62728",  # Red for T1 (matches matrix fill color pattern)
        'T2': "#1F77B4",  # Blue for T2 (matches matrix fill color pattern)
        'T3': "#FF7F0E"   # Orange for T3 (matches matrix fill color pattern)
    }

    # Override micropore/mesopore/macropore colors to use sample-specific colors
    # This will be dynamically set based on the sample being processed
    self.use_sample_specific_colors = True

    # Set default colors (will be overridden per sample)
    self.micropore_color = "#1F77B4"  # Default blue
    self.mesopore_color = "#1F77B4"   # Same as micro (no size distinction)
    self.macropore_color = "#1F77B4"  # Same as micro (no size distinction)

    # Set colors for different samples
    self.t1_color = "#1F77B4"  # Blue for T1
    self.t2_color = "#FF7F0E"  # Green for T2
    self.t3_color = "#D62728"  # Red for T3

    # Disable legends
    self.show_legends = False
    self.show_legend = False  # Alternative name that might be used
    self.enable_legends = False

    # Set alpha for pores and matrix
    self.pore_alpha = 0.9
    self.matrix_alpha = 0.3

    # Set matrix color
    self.matrix_color = "#CCCCCC"
    self.matrix_color_intensity_base = 0.7
    self.matrix_color_intensity_variation = 0.2

    print("\nSimple Pore Analysis - Cubic Dimension with Single-Color Pores (No Legends)")
    print("==============================================")
    print("100×100×100mm board configuration applied:")
    print(
        f"  - Board dimensions: {self.board_length_mm:.1f} × {self.board_width_mm:.1f} × {self.board_thickness_mm:.1f} mm")
    print(
        f"  - Aspect ratio: [{self.aspect_ratio[0]:.1f}, {self.aspect_ratio[1]:.1f}, {self.aspect_ratio[2]:.1f}]")
    print(
        f"  - Pore counts: Individual={self.n_pores_individual}, Comparative={self.n_pores_comparative}")
    print("  - Visualization features:")
    print("    * Single color per sample")
    print("    * No legends displayed")
    print("    * Matrix fill matching matrix_filled_clean.png")


# Replace the _load_default_config method with our custom implementation
MaterialConfig._load_default_config = custom_100x100x100_color0_config

# Make sure we force a reload of the configuration with our monkey patched method
if hasattr(CONFIG, '_config_name'):
    # Create a fresh instance with our patched method
    new_config = MaterialConfig(CONFIG._config_name)
    # Copy the new instance attributes to the existing CONFIG
    for attr_name in dir(new_config):
        if not attr_name.startswith('_'):
            setattr(CONFIG, attr_name, getattr(new_config, attr_name))
else:
    # Replace CONFIG with a fresh instance
    set_configuration("default")  # This will use our patched method

# Make sure no one can create a legend


def block_legend_creation(*args, **kwargs):
    """Make sure legends can't be created"""
    return None


# Apply more patches to specifically target the functions we need
try:
    # Patch individual_board_modeling.py
    import app.individual_board_modeling as ibm
    if hasattr(ibm, 'add_pore_size_legend'):
        ibm.add_pore_size_legend = block_legend_creation

    # Try to find and disable any legend creation in hybrid_pore_matrix_modeling
    import app.hybrid_pore_matrix_modeling as hpm

    # DEBUGGING: Let's see what functions exist in the hybrid module
    print("[DEBUG] Functions in hybrid_pore_matrix_modeling:")
    for attr_name in dir(hpm):
        if not attr_name.startswith('_') and callable(getattr(hpm, attr_name)):
            print(f"  - {attr_name}")

    # CRITICAL: Find and patch the actual function that creates the individual matrix visualizations
    # Look for variations of the function name
    matrix_viz_function = None
    for possible_name in [
        'create_individual_pores_matrix_visualization',
        'create_pores_matrix_combined',
        'create_individual_pore_matrix_model',
        'create_hybrid_pore_matrix_model',
        'create_individual_hybrid_model'
    ]:
        if hasattr(hpm, possible_name):
            matrix_viz_function = possible_name
            print(
                f"[DEBUG] Found matrix visualization function: {possible_name}")
            break

    if matrix_viz_function:
        original_matrix_func = getattr(hpm, matrix_viz_function)

        def force_sample_colors(sample_name, *args, **kwargs):
            print(f"[DEBUG] Creating matrix visualization for {sample_name}")

            # FORCE the sample colors before calling the function
            if hasattr(CONFIG, 'sample_pore_colors') and sample_name in CONFIG.sample_pore_colors:
                target_color = CONFIG.sample_pore_colors[sample_name]
                print(
                    f"[DEBUG] Target color for {sample_name}: {target_color}")

                # Override EVERYTHING related to pore colors
                CONFIG.micropore_color = target_color
                CONFIG.mesopore_color = target_color
                CONFIG.macropore_color = target_color
                CONFIG.default_pore_color = target_color
                CONFIG.pore_color = target_color

                # Also try to override any hardcoded colors in the module
                if hasattr(hpm, 'PORE_COLOR'):
                    hpm.PORE_COLOR = target_color
                if hasattr(hpm, 'DEFAULT_COLOR'):
                    hpm.DEFAULT_COLOR = target_color

                # Override matplotlib colors temporarily
                import matplotlib.pyplot as plt
                original_colors = plt.rcParams['axes.prop_cycle'].by_key()[
                    'color']
                plt.rcParams['axes.prop_cycle'] = plt.cycler(
                    'color', [target_color] * 10)

            # Call the original function
            result = original_matrix_func(sample_name, *args, **kwargs)

            # Restore matplotlib colors
            try:
                plt.rcParams['axes.prop_cycle'] = plt.cycler(
                    'color', original_colors)
            except:
                pass

            # Remove legends
            if hasattr(result, 'axes'):
                for ax in result.axes:
                    if ax.get_legend() is not None:
                        ax.get_legend().remove()

            return result

        # Replace the function
        setattr(hpm, matrix_viz_function, force_sample_colors)

    # ALSO: Find and patch any pore creation functions
    pore_creation_functions = []
    for attr_name in dir(hpm):
        if 'pore' in attr_name.lower() and 'create' in attr_name.lower() and callable(getattr(hpm, attr_name)):
            pore_creation_functions.append(attr_name)
            print(f"[DEBUG] Found pore creation function: {attr_name}")

    for func_name in pore_creation_functions:
        original_func = getattr(hpm, func_name)

        def make_color_override_wrapper(orig_func, name):
            def wrapper(*args, **kwargs):
                # Try to detect sample name from arguments
                sample_name = None
                for arg in args:
                    if isinstance(arg, str) and arg in ['T1', 'T2', 'T3']:
                        sample_name = arg
                        break

                if sample_name and hasattr(CONFIG, 'sample_pore_colors'):
                    target_color = CONFIG.sample_pore_colors[sample_name]
                    print(
                        f"[DEBUG] Overriding colors in {name} for {sample_name}: {target_color}")

                    # Set all possible color attributes
                    for color_attr in ['micropore_color', 'mesopore_color', 'macropore_color',
                                       'default_pore_color', 'pore_color']:
                        if hasattr(CONFIG, color_attr):
                            setattr(CONFIG, color_attr, target_color)

                result = orig_func(*args, **kwargs)

                # If result is a list of pores, force their colors
                if isinstance(result, list) and sample_name:
                    target_color = CONFIG.sample_pore_colors[sample_name]
                    for pore in result:
                        if isinstance(pore, dict):
                            pore['color'] = target_color
                            pore['alpha'] = getattr(CONFIG, 'pore_alpha', 0.9)

                return result
            return wrapper

        setattr(hpm, func_name, make_color_override_wrapper(
            original_func, func_name))

except Exception as e:
    print(f"Note: Some functions couldn't be patched: {e}")
    print("Using matplotlib-level legend blocking instead.")

# Function to remove all legends from all figures


def remove_all_legends():
    """Function to remove all legends from all figures"""
    for fig_num in plt.get_fignums():
        fig = plt.figure(fig_num)
        for ax in fig.axes:
            if ax.get_legend() is not None:
                ax.get_legend().remove()


# Patch plt.show to remove legends before showing
original_show = plt.show


def show_without_legends(*args, **kwargs):
    remove_all_legends()
    return original_show(*args, **kwargs)


plt.show = show_without_legends

# Set advanced analysis to True for more detailed visualizations
CONFIG.set_advanced_analysis(True)

# Execute the main function from the main module
sys.exit(main.main())
