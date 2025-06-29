#!/usr/bin/env python3
"""
Special wrapper script to enforce dimension override for 40×40×160mm configuration.
"""

import main
from app.config import MaterialConfig, CONFIG, set_configuration
import os
import sys
import importlib

# Set environment variable to indicate we want dimension override
os.environ["DIMENSION_OVERRIDE"] = "true"

# Import configuration before anything else

print("Applying dimension override (40×40×160mm)...")

# Store original function for reference
original_load_default_config = MaterialConfig._load_default_config

# Define the custom dimension implementation


def custom_40x40x160_config(self):
    # First call original to get all default settings
    original_load_default_config(self)

    # Then override specific dimensions and related settings
    # X-dimension (length) - changed from 160.0
    self.board_length_mm = 40.0
    self.board_width_mm = 40.0       # Y-dimension (width) - changed from 160.0
    # Z-dimension (thickness) - changed from 40.0
    self.board_thickness_mm = 160.0

    # Update normalized coordinate scaling for new aspect ratio
    # Half-length in normalized coordinates (reduced from 2.0)
    self.length_scale = 0.5
    # Half-width in normalized coordinates (reduced from 2.0)
    self.width_scale = 0.5
    # Half-thickness in normalized coordinates (increased from 0.5)
    self.thickness_scale = 2.0

    # Update aspect ratio proportional to new dimensions
    thickness_ratio = self.board_thickness_mm / \
        self.board_length_mm  # Now 4:1 instead of 1:4
    # [1, 1, 4.0] instead of [1, 1, 0.25]
    self.aspect_ratio = [1, 1, thickness_ratio]

    # Adjust visualization limits for the new aspect ratio
    # X-axis visualization range (adjusted from -2.2, 2.2)
    self.x_limits = (-0.7, 0.7)
    # Y-axis visualization range (adjusted from -2.2, 2.2)
    self.y_limits = (-0.7, 0.7)
    # Z-axis visualization range (adjusted from -0.7, 0.7)
    self.z_limits = (-2.2, 2.2)

    # Adjust matrix fill boundaries
    self.matrix_fill_x_bounds = (-0.45, 0.45)  # Adjusted from (-1.95, 1.95)
    self.matrix_fill_y_bounds = (-0.45, 0.45)  # Adjusted from (-1.95, 1.95)
    self.matrix_fill_z_bounds = (-1.95, 1.95)  # Adjusted from (-0.45, 0.45)

    # Update normalization constants for particle distribution
    self.matrix_length_norm = 0.45  # Adjusted from 1.95
    self.matrix_width_norm = 0.45   # Adjusted from 1.95

    # Adjust default coordinate bounds for particle placement
    self.default_x_bounds = (-0.45, 0.45)  # Adjusted from (-1.95, 1.95)
    self.default_y_bounds = (-0.45, 0.45)  # Adjusted from (-1.95, 1.95)
    self.default_z_bounds = (-1.95, 1.95)  # Adjusted from (-0.45, 0.45)

    # Update camera position for new aspect ratio
    import numpy as np
    # Rotated to emphasize z-axis
    self.camera_position = np.array([1.0, 1.0, 3.0])

    # Adjust view angle for better vertical board visualization
    self.view_elevation = 20
    self.view_azimuth = 30

    # Adjust pore counts for smaller board surface area
    self.n_pores_individual = 200
    self.n_pores_comparative = 150
    self.n_pores_density = 150
    self.n_pores_matrix = 300
    self.n_pores_hybrid = 300

    # Update particle counts for the new dimensions
    self.base_particles_matrix = 10000
    self.base_particles_hybrid_main = 5000
    self.base_particles_hybrid_combined = 3000

    # Critical fix for advanced analysis: Fix visualization parameters for advanced analysis
    if hasattr(self, 'enable_advanced_analysis') and self.enable_advanced_analysis:
        # Adjust advanced analysis parameters for vertical board
        self.advanced_stats_position = (0.5, 0.95)
        self.advanced_colorbar_colormap = 'jet'  # Use a colormap with good contrast
        self.advanced_tick_count = 10
        self.advanced_bins_count = 30

        # Add special parameters to fix the advanced analysis visualization
        self.advanced_vertical_layout = True
        self.advanced_figure_layout = 'vertical'
        self.advanced_colorbar_position = 'right'

        # Parameters to specifically address white/blank visualization issue
        self.advanced_z_scale_factor = 4.0  # Scale z-axis for proper rendering
        self.advanced_plot_padding = 0.2  # Add padding around plots
        # Scientific notation for colorbar values
        self.advanced_colorbar_formatter = '%.2e'

    print("\nSimple Pore Analysis - Custom Dimension Configuration")
    print("==============================================")
    print("40×40×160mm board configuration applied:")
    print(
        f"  - Board dimensions: {self.board_length_mm:.1f} × {self.board_width_mm:.1f} × {self.board_thickness_mm:.1f} mm")
    print(
        f"  - Aspect ratio: [{self.aspect_ratio[0]:.1f}, {self.aspect_ratio[1]:.1f}, {self.aspect_ratio[2]:.1f}]")
    print(
        f"  - Pore counts: Individual={self.n_pores_individual}, Comparative={self.n_pores_comparative}")
    print(f"  - Matrix particles: {self.base_particles_matrix}")
    if hasattr(self, 'enable_advanced_analysis') and self.enable_advanced_analysis:
        print("  - Advanced analysis: Enabled with vertical board optimizations")


# Replace the _load_default_config method with our custom implementation
MaterialConfig._load_default_config = custom_40x40x160_config

# Make sure we force a reload of the configuration with our monkey patched method
if hasattr(CONFIG, '_config_name'):  # If CONFIG is already instantiated
    # Create a fresh instance with our patched method
    new_config = MaterialConfig(CONFIG._config_name)
    # Copy the new instance attributes to the existing CONFIG
    for attr_name in dir(new_config):
        if not attr_name.startswith('_'):  # Skip private attributes
            setattr(CONFIG, attr_name, getattr(new_config, attr_name))
else:
    # Replace CONFIG with a fresh instance
    set_configuration("default")  # This will use our patched method

# Fix for get_advanced_analysis_params method to ensure proper rendering with new dimensions
original_get_advanced_params = MaterialConfig.get_advanced_analysis_params


def enhanced_get_advanced_params(self):
    params = original_get_advanced_params(self)

    # If we have the vertical 40×40×160 configuration, update advanced params
    if self.board_length_mm == 40.0 and self.board_width_mm == 40.0 and self.board_thickness_mm == 160.0:
        params.update({
            'vertical_layout': True,
            'figure_layout': 'vertical',
            'micropore_max_radius': self.min_pore_radius + (self.max_pore_radius - self.min_pore_radius) / 3,
            'mesopore_max_radius': self.min_pore_radius + 2 * (self.max_pore_radius - self.min_pore_radius) / 3,
            'colorbar_position': 'right',
            'z_scale_factor': 4.0,
            'plot_padding': 0.2,
            'colorbar_formatter': '%.2e',
            'stats_position': (0.5, 0.95),
        })
    return params


# Patch the method to return our enhanced parameters
MaterialConfig.get_advanced_analysis_params = enhanced_get_advanced_params

# Enable advanced analysis by default for this run
CONFIG.set_advanced_analysis(True)

# Import main.py from the root directory (not from app)

# Execute the main function from the main module# Execute the main function (call the function, not the module)
sys.exit(main.main())
sys.exit(main())
