#!/usr/bin/env python3
"""
Special wrapper script to enforce dimension override for 100×100×100mm configuration.
"""

import main
from app.config import MaterialConfig, CONFIG, set_configuration
import os
import sys
import importlib

# Set environment variable to indicate we want dimension override
os.environ["DIMENSION_OVERRIDE"] = "true"

print("Applying dimension override (100×100×100mm)...")

# Store original function for reference
original_load_default_config = MaterialConfig._load_default_config


def custom_100x100x100_config(self):
    # First call original to get all default settings
    original_load_default_config(self)

    # Then override specific dimensions and related settings
    # X-dimension (length) - changed from 160.0
    self.board_length_mm = 100.0
    # Y-dimension (width) - changed from 160.0
    self.board_width_mm = 100.0
    # Z-dimension (thickness) - changed from 40.0
    self.board_thickness_mm = 100.0

    # Update normalized coordinate scaling for new cubic shape
    # Half-length in normalized coordinates (adjusted from 2.0)
    self.length_scale = 1.25
    # Half-width in normalized coordinates (adjusted from 2.0)
    self.width_scale = 1.25
    # Half-thickness in normalized coordinates (increased from 0.5)
    self.thickness_scale = 1.25

    # Update aspect ratio for cubic shape (all equal)
    thickness_ratio = 1.0  # Equal dimensions for cube
    self.aspect_ratio = [1, 1, thickness_ratio]

    # Adjust visualization limits for the cubic shape
    self.x_limits = (-1.5, 1.5)    # X-axis visualization range (adjusted)
    self.y_limits = (-1.5, 1.5)    # Y-axis visualization range (adjusted)
    self.z_limits = (-1.5, 1.5)    # Z-axis visualization range (adjusted)

    # Adjust matrix fill boundaries
    self.matrix_fill_x_bounds = (-1.2, 1.2)  # Adjusted boundaries
    self.matrix_fill_y_bounds = (-1.2, 1.2)  # Adjusted boundaries
    self.matrix_fill_z_bounds = (-1.2, 1.2)  # Adjusted boundaries

    # Update normalization constants for particle distribution
    self.matrix_length_norm = 1.2  # Adjusted from 1.95
    self.matrix_width_norm = 1.2   # Adjusted from 1.95

    # Adjust default coordinate bounds for particle placement
    self.default_x_bounds = (-1.2, 1.2)
    self.default_y_bounds = (-1.2, 1.2)
    self.default_z_bounds = (-1.2, 1.2)

    # Update camera position for cubic view
    import numpy as np
    # Equal distance for cubic shape
    self.camera_position = np.array([2.0, 2.0, 2.0])

    # Adjust view angle for better cubic board visualization
    self.view_elevation = 35
    self.view_azimuth = 45

    # Adjust pore counts for larger cubic volume
    # Calculate the volume ratio compared to default (160×160×40)
    default_volume = 160 * 160 * 40
    new_volume = 100 * 100 * 100
    volume_ratio = new_volume / default_volume  # About 1.56

    # Scale pore counts based on volume
    self.n_pores_individual = int(600 * volume_ratio)  # ~936
    self.n_pores_comparative = int(400 * volume_ratio)  # ~624
    self.n_pores_density = int(500 * volume_ratio)     # ~780
    self.n_pores_matrix = int(800 * volume_ratio)      # ~1248
    self.n_pores_hybrid = int(800 * volume_ratio)      # ~1248

    # Update particle counts for the new dimensions
    self.base_particles_matrix = int(15000 * volume_ratio)  # ~23400
    self.base_particles_hybrid_main = int(8000 * volume_ratio)  # ~12480
    self.base_particles_hybrid_combined = int(5000 * volume_ratio)  # ~7800

    # Adjust pore size range for the cubic shape
    self.min_pore_radius = 0.04
    self.max_pore_radius = 0.1

    # Critical fix for advanced analysis: Fix visualization parameters
    if hasattr(self, 'enable_advanced_analysis') and self.enable_advanced_analysis:
        # Adjust advanced analysis parameters for the cubic shape
        self.advanced_stats_position = (0.5, 0.95)
        self.advanced_colorbar_colormap = 'jet'
        self.advanced_tick_count = 10
        self.advanced_bins_count = 30

        # Cubic shape doesn't need special layout adjustments like the vertical board
        self.advanced_colorbar_position = 'right'
        self.advanced_colorbar_formatter = '%.2e'

    print("\nSimple Pore Analysis - Cubic Dimension Configuration")
    print("==============================================")
    print("100×100×100mm board configuration applied:")
    print(
        f"  - Board dimensions: {self.board_length_mm:.1f} × {self.board_width_mm:.1f} × {self.board_thickness_mm:.1f} mm")
    print(
        f"  - Aspect ratio: [{self.aspect_ratio[0]:.1f}, {self.aspect_ratio[1]:.1f}, {self.aspect_ratio[2]:.1f}]")
    print(
        f"  - Pore counts: Individual={self.n_pores_individual}, Comparative={self.n_pores_comparative}")
    print(f"  - Matrix particles: {self.base_particles_matrix}")
    if hasattr(self, 'enable_advanced_analysis') and self.enable_advanced_analysis:
        print("  - Advanced analysis: Enabled with cubic shape optimizations")


# Replace the _load_default_config method with our custom implementation
MaterialConfig._load_default_config = custom_100x100x100_config

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

    # If we have the cubic 100×100×100 configuration, update advanced params
    if (self.board_length_mm == 100.0 and
        self.board_width_mm == 100.0 and
            self.board_thickness_mm == 100.0):
        params.update({
            'figure_layout': 'square',
            'micropore_max_radius': self.min_pore_radius + (self.max_pore_radius - self.min_pore_radius) / 3,
            'mesopore_max_radius': self.min_pore_radius + 2 * (self.max_pore_radius - self.min_pore_radius) / 3,
            'colorbar_position': 'right',
            'z_scale_factor': 1.0,  # Equal scaling for cubic shape
            'plot_padding': 0.15,
            'colorbar_formatter': '%.2e',
            'stats_position': (0.5, 0.95),
        })
    return params


# Patch the method to return our enhanced parameters
MaterialConfig.get_advanced_analysis_params = enhanced_get_advanced_params

# Enable advanced analysis by default for this run
CONFIG.set_advanced_analysis(True)

# Execute the main function from the main module
sys.exit(main.main())
