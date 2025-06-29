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


# Default color settings for different pore types
# Even more intense colors that will be clearly visible against matrix
DEFAULT_MICROPORE_COLOR = "#FF1493"  # Deep pink (Micropores)
DEFAULT_MESOPORE_COLOR = "#FFFF00"   # Bright yellow (Mesopores)
DEFAULT_MACROPORE_COLOR = "#00FFFF"  # Bright cyan (Macropores)


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
        self.micropore_color = DEFAULT_MICROPORE_COLOR
        self.mesopore_color = DEFAULT_MESOPORE_COLOR
        self.macropore_color = DEFAULT_MACROPORE_COLOR
        self.matrix_fill_color = "#cccccc"  # Default matrix fill color
        self.enable_advanced_analysis = False  # Disabled by default
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
        self.dpi = 300                    # Figure resolution
        self.output_format = 'png'        # Output file format
        self.figure_size = (12, 8)        # Figure size in inches

        # Maintain aspect ratio proportional to board dimensions
        thickness_ratio = self.board_thickness_mm / self.board_length_mm
        self.aspect_ratio = [1, 1, thickness_ratio]  # e.g., [1, 1, 0.25]

        # Camera and depth sorting
        self.camera_position = np.array([3.0, 1.0, 1.0])
        self.sort_particles = True        # Enable depth sorting for realism
        self.view_elevation = 30          # Camera elevation angle
        self.view_azimuth = 60            # Camera azimuth angle
        self.z_depth_bonus = 0.1          # Bonus for depth sorting

        # Frame visualization
        self.frame_color = '#FF8C00'      # Orange color for the frame
        self.frame_linewidth = 1.5        # Line width for the frame
        self.frame_alpha = 0.8            # Transparency of the frame

        # === POSITIONING PARAMETERS ===
        self.edge_margin_factor = 0.95
        self.z_margin_factor = 0.8
        self.diagonal_pore_ratio = 0.25
        self.jitter_strength = 0.01
        self.z_jitter_factor = 0.5
        self.edge_position_factor = 0.9
        self.corner_position_factor = 0.85

        # === PARTICLE GENERATION PARAMETERS ===
        self.base_particles_matrix = 15000
        self.base_particles_hybrid_main = 8000
        self.base_particles_hybrid_combined = 5000

        # === PARTICLE SIZE PARAMETERS ===
        self.particle_base_size = 0.8
        self.particle_size_variation = 1.5
        self.color_intensity_base = 0.25
        self.color_intensity_variation = 0.25
        self.pore_color_intensity_base = 0.3
        self.pore_color_intensity_variation = 0.4

        # === MATRIX MATERIAL PARAMETERS ===
        # These parameters control the sand/dust visualization that fills the board
        # Default boundaries for matrix fill to match board dimensions
        self.matrix_fill_x_bounds = (-1.95, 1.95)
        self.matrix_fill_y_bounds = (-1.95, 1.95)
        self.matrix_fill_z_bounds = (-0.45, 0.45)

        # Normalization constants for particle distribution
        self.matrix_length_norm = 1.95
        self.matrix_width_norm = 1.95

        # Particle size parameters for matrix fill - INCREASE SIZES FOR VISIBILITY
        self.matrix_base_particle_size = 2.0      # Increased from 0.8 for visibility
        self.matrix_particle_size_variation = 2.5  # Increased from 1.5 for contrast
        self.matrix_base_particles = 15000        # Base number of particles

        # Restore to original value for better visibility
        self.matrix_particle_alpha = 0.5          # Increased from 0.2 for visibility
        self.matrix_batch_size = 1000             # Batch size for rendering

        # Enhanced color intensity for better visibility
        self.matrix_color_intensity_base = 0.3      # Increased from 0.1
        self.matrix_color_intensity_variation = 0.5  # Increased from 0.3

        # === PARTICLE GENERATION PARAMETERS ===
        # Increase particle counts for all visualizations
        self.base_particles_matrix = 20000        # Increased from 15000
        self.base_particles_hybrid_main = 15000    # Increased from 8000
        self.base_particles_hybrid_combined = 10000  # Increased from 5000

        # === PORE VISUALIZATION PARAMETERS ===
        self.pore_alpha = 1.0               # Maximum opacity for pores
        self.pore_edge_width = 0.5          # Add edges to pores for better definition
        self.pore_edge_color = 'black'      # Black edges to outline pores

        # === COORDINATE BOUNDS ===
        # Default coordinate bounds for particle placement
        self.default_x_bounds = (-1.95, 1.95)
        self.default_y_bounds = (-1.95, 1.95)
        self.default_z_bounds = (-0.45, 0.45)

        # === ADVANCED ANALYSIS PARAMETERS ===
        # Parameters for advanced statistical visualization
        # Colormap for volume colorbar ('jet', 'viridis', etc.)
        self.advanced_colorbar_colormap = 'jet'
        self.advanced_tick_count = 8                # Number of ticks on volume colorbar
        # Number of bins in diameter histogram
        self.advanced_bins_count = 30
        # Jitter amount for sphericity points
        self.advanced_jitter_amount = 1.5
        # Position for statistics text
        self.advanced_stats_position = (0.5, 0.98)
        self.advanced_colorbar_formatter = ':.4f'  # Format for colorbar tick labels

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

        # === PARTICLE GENERATION PARAMETERS ===
        # Scale particle counts with volume for small specimens
        self.base_particles_matrix = int(15000 * volume_ratio)
        self.base_particles_hybrid_main = int(8000 * volume_ratio)
        self.base_particles_hybrid_combined = int(5000 * volume_ratio)

        # === COORDINATE BOUNDS ===
        # Scaled coordinate bounds for small specimens
        boundary_scale = scale_factor * 1.1  # 10% margin
        self.default_x_bounds = (-1.95 * boundary_scale, 1.95 * boundary_scale)
        self.default_y_bounds = (-1.95 * boundary_scale, 1.95 * boundary_scale)
        self.default_z_bounds = (-0.45 * (self.specimen_thickness_mm / 40.0),
                                 0.45 * (self.specimen_thickness_mm / 40.0))

        # === POSITIONING PARAMETERS ===
        # Same positioning factors (scale-independent)
        self.edge_margin_factor = 0.95
        self.z_margin_factor = 0.8
        self.diagonal_pore_ratio = 0.25
        self.jitter_strength = 0.03 * scale_factor  # Scale jitter with specimen size
        self.z_jitter_factor = 0.5

        # Edge positioning parameters
        self.edge_position_factor = 0.9
        self.corner_position_factor = 0.85

        # === PARTICLE SIZE PARAMETERS ===
        # Same particle sizing (will be scaled by bounds)
        self.particle_base_size = 0.8
        self.particle_size_variation = 1.5
        self.color_intensity_base = 0.25
        self.color_intensity_variation = 0.6
        self.pore_color_intensity_base = 0.8
        self.pore_color_intensity_variation = 0.2

    def set_advanced_analysis(self, enable=True):
        """Enable or disable advanced analysis visualizations."""
        self.enable_advanced_analysis = enable

    def set_matrix_fill_color(self, color):
        """Set the fill color for matrix material."""
        self.matrix_fill_color = color

    def get_advanced_analysis_params(self):
        """Get parameters for advanced pore analysis."""
        return {
            'enabled': getattr(self, 'enable_advanced_analysis', False),
            'colorbar_colormap': getattr(self, 'advanced_colorbar_colormap', 'jet'),
            'tick_count': getattr(self, 'advanced_tick_count', 8),
            'bins_count': getattr(self, 'advanced_bins_count', 30),
            'jitter': getattr(self, 'advanced_jitter_amount', 1.5),
            'stats_position': getattr(self, 'advanced_stats_position', (0.5, 0.98)),
            'micropore_max_radius': self.min_pore_radius + (self.max_pore_radius - self.min_pore_radius) / 3,
            'mesopore_max_radius': self.min_pore_radius + 2 * (self.max_pore_radius - self.min_pore_radius) / 3,
        }

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

    def get_particle_size_parameters(self):
        """Get particle sizing parameters."""
        return {
            'base_size': self.particle_base_size,
            'size_variation': self.particle_size_variation,
            'color_intensity_base': self.color_intensity_base,
            'color_intensity_variation': self.color_intensity_variation,
            'pore_color_intensity_base': self.pore_color_intensity_base,
            'pore_color_intensity_variation': self.pore_color_intensity_variation
        }

    def get_normalized_bounds(self):
        """Get normalized coordinate bounds for visualizations."""
        return {
            'x_bounds': self.matrix_fill_x_bounds,
            'y_bounds': self.matrix_fill_y_bounds,
            'z_bounds': self.matrix_fill_z_bounds,
            'length_norm': self.matrix_length_norm,
            'width_norm': self.matrix_width_norm
        }

    def get_dimension_scale_factors(self):
        """Get dimension scaling factors for board size adjustments."""
        # Calculate volume scale based on current dimensions vs default 160x160x40
        volume_scale = (self.board_length_mm * self.board_width_mm *
                        self.board_thickness_mm) / (160.0 * 160.0 * 40.0)
        return {
            'volume_scale': volume_scale,
            'length_scale': self.board_length_mm / 160.0,
            'width_scale': self.board_width_mm / 160.0,
            'thickness_scale': self.board_thickness_mm / 40.0
        }

    def get_particle_counts(self):
        """Get particle count parameters for different visualizations."""
        return {
            'matrix': self.n_pores_matrix,
            'individual': self.n_pores_individual,
            'comparative': self.n_pores_comparative,
            'density': self.n_pores_density,
            'hybrid': self.n_pores_hybrid,
            'hybrid_main': self.base_particles_hybrid_main,
            'hybrid_combined': self.base_particles_hybrid_combined
        }

    def get_matrix_parameters(self):
        """Get all matrix material parameters."""
        return {
            'x_bounds': self.matrix_fill_x_bounds,
            'y_bounds': self.matrix_fill_y_bounds,
            'z_bounds': self.matrix_fill_z_bounds,
            'length_norm': self.matrix_length_norm,
            'width_norm': self.matrix_width_norm,
            'base_particle_size': self.matrix_base_particle_size,
            'particle_size_variation': self.matrix_particle_size_variation,
            'base_particles': self.matrix_base_particles,
            'particle_alpha': self.matrix_particle_alpha,
            'batch_size': self.matrix_batch_size,
            'color_intensity_base': self.matrix_color_intensity_base,
            'color_intensity_variation': self.matrix_color_intensity_variation
        }

    def get_positioning_parameters(self):
        """Get positioning and margin parameters for pore placement."""
        return {
            'edge_margin_factor': self.edge_margin_factor,
            'z_margin_factor': self.z_margin_factor,
            'diagonal_pore_ratio': self.diagonal_pore_ratio,
            'jitter_strength': self.jitter_strength,
            'z_jitter_factor': self.z_jitter_factor,
            'edge_position_factor': self.edge_position_factor,
            'corner_position_factor': self.corner_position_factor
        }

    def get_coordinate_bounds(self):
        """Get default coordinate bounds for element positioning."""
        return {
            'x_bounds': self.default_x_bounds,
            'y_bounds': self.default_y_bounds,
            'z_bounds': self.default_z_bounds
        }

    def set_pore_colors(self, micropore=None, mesopore=None, macropore=None):
        """
        Set custom colors for different pore types.

        Parameters:
        -----------
        micropore : str
            Color for micropores (hex code or color name)
        mesopore : str
            Color for mesopores (hex code or color name)
        macropore : str
            Color for macropores (hex code or color name)
        """
        if micropore:
            self.micropore_color = micropore
        if mesopore:
            self.mesopore_color = mesopore
        if macropore:
            self.macropore_color = macropore

    def get_pore_colors(self):
        """
        Get the current colors for different pore types.

        Returns:
        --------
        dict
            Dictionary with keys 'micropore_color', 'mesopore_color', 'macropore_color'
        """
        return {
            "micropore_color": self.micropore_color,
            "mesopore_color": self.mesopore_color,
            "macropore_color": self.macropore_color,
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
