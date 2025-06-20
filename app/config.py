#!/usr/bin/env python3
"""
Configuration management for 3D pore structure modeling in
calcium sulfoaluminate cement-based thermal insulating boards.

This module centralizes all physical, geometric, and visualization parameters
to enable easy switching between different experimental configurations
without modifying core analysis code.
"""

from typing import Dict, Any
import numpy as np


class MaterialConfig:
    """
    Configuration class for CSA cement-based insulating board modeling.

    Provides centralized parameter management for different experimental
    scenarios including standard board testing and small specimen analysis.
    """

    def __init__(self, config_name: str = "default"):
        """
        Initialize configuration with specified parameter set.

        Parameters:
        -----------
        config_name : str
            Configuration identifier ('default', 'small_specimen', 'custom')
        """
        self.config_name = config_name
        self._load_configuration(config_name)

    def _load_configuration(self, config_name: str):
        """Load the specified configuration parameters."""

        if config_name == "default":
            self._load_default_config()
        elif config_name == "small_specimen":
            self._load_small_specimen_config()
        else:
            raise ValueError(f"Unknown configuration: {config_name}")

    def _load_default_config(self):
        """
        Default configuration for standard CSA cement board testing.

        Physical dimensions: 160×160×40 mm rectangular boards
        Visualization: Full-scale 3D rendering with detailed pore structures
        """

        # === PHYSICAL DIMENSIONS ===
        # Board geometry in millimeters (experimental standard)
        self.board_length_mm = 160.0      # X-dimension (length)
        self.board_width_mm = 160.0       # Y-dimension (width)
        self.board_thickness_mm = 40.0    # Z-dimension (thickness)

        # Normalized coordinate scaling for visualization
        # Reference: 160mm → 2.0 units, 40mm → 0.5 units
        self.length_scale = 2.0           # Half-length in normalized coordinates
        self.width_scale = 2.0            # Half-width in normalized coordinates
        self.thickness_scale = 0.5        # Half-thickness in normalized coordinates

        # === PORE GENERATION PARAMETERS ===
        # Original pore counts to maintain visual density and quality
        # Number of pores for individual visualizations (original: 600)
        self.n_pores_individual = 600
        # Number of pores per sample in comparisons (original: 400)
        self.n_pores_comparative = 400
        # Number of pores for density modeling (original: 500)
        self.n_pores_density = 500
        # Number of pores for matrix material modeling (original: 800)
        self.n_pores_matrix = 800
        # Number of pores for hybrid modeling (original: 800)
        self.n_pores_hybrid = 800

        # Original pore size scaling factors to maintain visual appearance
        # No additional scaling (original had none)
        self.pore_scale_factor = 1.0
        # Minimum pore radius (original: 0.03)
        self.min_pore_radius = 0.03
        # Maximum pore radius (original: 0.08)
        self.max_pore_radius = 0.08

        # === VISUALIZATION PARAMETERS ===
        # 3D plotting boundaries
        self.x_limits = (-2.2, 2.2)      # X-axis visualization range
        self.y_limits = (-2.2, 2.2)      # Y-axis visualization range
        self.z_limits = (-0.7, 0.7)      # Z-axis visualization range

        # Rendering quality settings (original values)
        # Azimuthal sphere resolution (original: 12)
        self.sphere_u_resolution = 12
        # Polar sphere resolution (original: 8)
        self.sphere_v_resolution = 8
        self.alpha_transparency = 0.9     # Sphere transparency (original: 0.9)

        # Camera and depth sorting
        self.camera_position = np.array([3.0, 1.0, 1.0])
        self.z_depth_bonus = 0.2          # Z-height visibility bonus

        # Frame visualization
        self.frame_color = '#FF8C00'      # Orange frame color
        self.frame_linewidth = 1.5        # Frame line thickness
        self.frame_alpha = 0.8            # Frame transparency

        # Aspect ratio (matches physical dimensions: 160:160:40 = 4:4:1)
        self.aspect_ratio = [4, 4, 1]

        # Default viewing angle
        self.view_elevation = 30          # Camera elevation angle
        self.view_azimuth = 60            # Camera azimuth angle

        # === OUTPUT CONFIGURATION ===
        self.figure_size = (12, 8)        # Matplotlib figure size
        self.dpi = 300                    # Figure resolution for saving
        self.output_format = 'png'        # Default output format

        # === PHYSICAL PROPERTIES ===
        # Mercury intrusion porosimetry parameters
        self.mercury_contact_angle = 140  # Mercury contact angle (degrees)
        self.mercury_surface_tension = 0.485  # Surface tension (N/m)

        # Sample composition identifiers
        self.sample_names = ['T1', 'T2', 'T3']
        self.sample_colors = ['jet', 'viridis', 'plasma']

    def _load_small_specimen_config(self):
        """
        Configuration for small circular specimen testing.

        Physical dimensions: 10 ± 1 mm diameter circular specimens
        Visualization: High-resolution rendering for detailed microstructure analysis
        """

        # === PHYSICAL DIMENSIONS ===
        # Small specimen geometry (circular, 10mm diameter)
        self.specimen_diameter_mm = 10.0   # Nominal diameter
        self.specimen_tolerance_mm = 1.0   # ± tolerance
        self.specimen_thickness_mm = 10.0  # Assumed thickness (cubic-like)

        # Convert to rectangular approximation for visualization
        # Use square cross-section with equivalent area
        equivalent_side = self.specimen_diameter_mm / np.sqrt(np.pi) * 2

        self.board_length_mm = equivalent_side
        self.board_width_mm = equivalent_side
        self.board_thickness_mm = self.specimen_thickness_mm

        # Normalized coordinate scaling (adjusted for small specimens)
        # Scale to maintain similar visualization proportions
        scale_factor = equivalent_side / 160.0  # Ratio to default dimensions

        self.length_scale = 2.0 * scale_factor
        self.width_scale = 2.0 * scale_factor
        self.thickness_scale = 0.5 * (self.specimen_thickness_mm / 40.0)

        # === PORE GENERATION PARAMETERS ===
        # Proportionally reduced pore counts for smaller specimen volume
        volume_ratio = (equivalent_side / 160.0) ** 3

        self.n_pores_individual = max(
            50, int(600 * volume_ratio))   # Original: 600
        self.n_pores_comparative = max(
            30, int(400 * volume_ratio))  # Original: 400
        self.n_pores_density = max(
            40, int(500 * volume_ratio))      # Original: 500
        self.n_pores_matrix = max(
            60, int(800 * volume_ratio))       # Original: 800
        self.n_pores_hybrid = max(
            60, int(800 * volume_ratio))       # Original: 800

        # Maintain original pore size scaling but adjust for small specimens
        self.pore_scale_factor = 2.0      # Larger relative pore sizes for visibility
        self.min_pore_radius = 0.03 * scale_factor  # Scale the original 0.03
        self.max_pore_radius = 0.08 * scale_factor  # Scale the original 0.08
        self.min_pore_radius = 0.01       # Slightly larger minimum
        self.max_pore_radius = 0.4        # Larger maximum for visibility

        # === VISUALIZATION PARAMETERS ===
        # Adjusted plotting boundaries for small specimens
        boundary_scale = scale_factor * 1.1  # 10% margin

        self.x_limits = (-2.2 * boundary_scale, 2.2 * boundary_scale)
        self.y_limits = (-2.2 * boundary_scale, 2.2 * boundary_scale)
        self.z_limits = (-0.7 * (self.specimen_thickness_mm / 40.0),
                         0.7 * (self.specimen_thickness_mm / 40.0))

        # Higher rendering quality for detailed analysis (but not too high)
        self.sphere_u_resolution = 12     # Keep original resolution
        self.sphere_v_resolution = 8      # Keep original resolution
        self.alpha_transparency = 0.9     # Keep original transparency

        # Adjusted camera position for small specimens
        self.camera_position = np.array([3.0 * scale_factor,
                                        1.0 * scale_factor,
                                        1.0 * scale_factor])
        self.z_depth_bonus = 0.3          # Increased depth bonus

        # Frame visualization (adjusted)
        self.frame_color = '#FF8C00'      # Keep orange color
        self.frame_linewidth = 2.0        # Thicker lines for visibility
        self.frame_alpha = 0.9            # Higher opacity

        # Maintain aspect ratio proportional to specimen
        thickness_ratio = self.specimen_thickness_mm / equivalent_side
        self.aspect_ratio = [1, 1, thickness_ratio]

        # Closer viewing angle for small specimens
        self.view_elevation = 25          # Slightly lower elevation
        self.view_azimuth = 45            # Different azimuth for clarity

        # === OUTPUT CONFIGURATION ===
        self.figure_size = (10, 8)        # Slightly smaller figure
        self.dpi = 600                    # Higher resolution for detail
        self.output_format = 'png'        # PNG for high detail

        # === PHYSICAL PROPERTIES ===
        # Same MIP parameters (material-dependent, not size-dependent)
        self.mercury_contact_angle = 140
        self.mercury_surface_tension = 0.485

        # Sample identifiers (unchanged)
        self.sample_names = ['T1', 'T2', 'T3']
        self.sample_colors = ['jet', 'viridis', 'plasma']

    def get_board_corners(self):
        """
        Calculate the 8 corner vertices of the board geometry.

        Returns:
        --------
        numpy.ndarray
            Array of shape (8, 3) containing corner coordinates
        """
        corners = np.array([
            [-self.length_scale, -self.width_scale, -self.thickness_scale],
            [self.length_scale, -self.width_scale, -self.thickness_scale],
            [self.length_scale, self.width_scale, -self.thickness_scale],
            [-self.length_scale, self.width_scale, -self.thickness_scale],
            [-self.length_scale, -self.width_scale, self.thickness_scale],
            [self.length_scale, -self.width_scale, self.thickness_scale],
            [self.length_scale, self.width_scale, self.thickness_scale],
            [-self.length_scale, self.width_scale, self.thickness_scale]
        ])
        return corners

    def get_board_edges(self):
        """
        Get the edge connectivity for the board wireframe.

        Returns:
        --------
        list
            List of tuples defining edge connections between vertices
        """
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
            (0, 4), (1, 5), (2, 6), (3, 7)   # Connecting edges
        ]
        return edges

    def is_point_inside_board(self, x, y, z):
        """
        Check if a point is inside the board geometry.

        Parameters:
        -----------
        x, y, z : float or array_like
            Coordinates to check

        Returns:
        --------
        bool or array_like
            True if point(s) are inside the board boundaries
        """
        x_inside = np.abs(x) <= self.length_scale
        y_inside = np.abs(y) <= self.width_scale
        z_inside = np.abs(z) <= self.thickness_scale

        return x_inside & y_inside & z_inside

    def get_summary(self):
        """
        Get a summary of the current configuration.

        Returns:
        --------
        dict
            Dictionary containing key configuration parameters
        """
        return {
            'config_name': self.config_name,
            'board_dimensions_mm': (self.board_length_mm,
                                    self.board_width_mm,
                                    self.board_thickness_mm),
            'normalized_scales': (self.length_scale,
                                  self.width_scale,
                                  self.thickness_scale),
            'pore_counts': {
                'individual': self.n_pores_individual,
                'comparative': self.n_pores_comparative,
                'density': self.n_pores_density,
                'matrix': self.n_pores_matrix,
                'hybrid': self.n_pores_hybrid
            },
            'visualization_limits': {
                'x': self.x_limits,
                'y': self.y_limits,
                'z': self.z_limits
            }
        }


# Global configuration instance
# Users can switch configurations by changing this
CONFIG = MaterialConfig("default")


def set_configuration(config_name: str):
    """
    Switch to a different configuration.

    Parameters:
    -----------
    config_name : str
        Configuration to switch to ('default', 'small_specimen')
    """
    global CONFIG
    CONFIG = MaterialConfig(config_name)
    print(f"Switched to configuration: {config_name}")
    print("Configuration summary:")
    for key, value in CONFIG.get_summary().items():
        print(f"  {key}: {value}")


def get_config():
    """
    Get the current configuration instance.

    Returns:
    --------
    MaterialConfig
        Current configuration object
    """
    return CONFIG

# Convenience functions for common parameter access


def get_board_dimensions():
    """Get current board dimensions in mm."""
    return (CONFIG.board_length_mm, CONFIG.board_width_mm, CONFIG.board_thickness_mm)


def get_visualization_limits():
    """Get current visualization axis limits."""
    return CONFIG.x_limits, CONFIG.y_limits, CONFIG.z_limits


def get_pore_count(visualization_type: str):
    """Get pore count for specific visualization type."""
    pore_counts = {
        'individual': CONFIG.n_pores_individual,
        'comparative': CONFIG.n_pores_comparative,
        'density': CONFIG.n_pores_density,
        'matrix': CONFIG.n_pores_matrix,
        'hybrid': CONFIG.n_pores_hybrid
    }
    return pore_counts.get(visualization_type, CONFIG.n_pores_individual)
