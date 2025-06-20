# Configuration System Documentation

## Overview

The `config.py` module serves as the central configuration management system for the 3D pore structure modeling of calcium sulfoaluminate (CSA) cement-based thermal insulating boards. This enhanced system provides complete parameterization of all modeling aspects including matrix fill materials, hybrid visualizations, and scaling capabilities through the `config_override.sh` script.

## Table of Contents

1. [Configuration Architecture](#configuration-architecture)
2. [Physical Dimensions Parameters](#physical-dimensions-parameters)
3. [Pore Generation Parameters](#pore-generation-parameters)
4. [Matrix Material Parameters](#matrix-material-parameters)
5. [Hybrid Modeling Parameters](#hybrid-modeling-parameters)
6. [Visualization Parameters](#visualization-parameters)
7. [Output Configuration](#output-configuration)
8. [Physical Properties](#physical-properties)
9. [Coordinate Bounds](#coordinate-bounds)
10. [Positioning Parameters](#positioning-parameters)
11. [Configuration Override System](#configuration-override-system)
12. [Scaling and Performance](#scaling-and-performance)
13. [Configuration Switching](#configuration-switching)
14. [Impact on Application Modules](#impact-on-application-modules)

---

## Configuration Architecture

### Two Primary Configurations

1. **Default Configuration** (`"default"`)

   - Standard CSA cement board testing (160×160×40 mm)
   - Full-scale 3D rendering with detailed pore structures
   - Optimized for standard laboratory specimens

2. **Small Specimen Configuration** (`"small_specimen"`)
   - Small circular specimens (10 ± 1 mm diameter)
   - High-resolution rendering for microstructure analysis
   - Proportionally scaled parameters for small samples

---

## Physical Dimensions Parameters

### Board Geometry (mm)

```python
# Default Configuration
board_length_mm = 160.0      # X-dimension (length)
board_width_mm = 160.0       # Y-dimension (width)
board_thickness_mm = 40.0    # Z-dimension (thickness)

# Small Specimen Configuration
# Converted from circular (10mm diameter) to equivalent square
board_length_mm ≈ 11.28      # Equivalent side length
board_width_mm ≈ 11.28       # Equivalent side length
board_thickness_mm = 10.0    # Assumed cubic thickness
```

**Impact on Code:**

- **All visualization modules** use these dimensions to set physical boundaries
- **Data processor** scales coordinate systems based on these values
- **Matrix material modeling** calculates particle densities relative to board volume
- **Comparative analysis** normalizes measurements across different specimen sizes

### Normalized Coordinate Scaling

```python
# Default Configuration
length_scale = 2.0           # Half-length in normalized coordinates
width_scale = 2.0            # Half-width in normalized coordinates
thickness_scale = 0.5        # Half-thickness in normalized coordinates

# Small Specimen Configuration
length_scale = 2.0 * scale_factor    # Proportionally scaled
width_scale = 2.0 * scale_factor     # Proportionally scaled
thickness_scale = 0.5 * ratio        # Thickness ratio adjusted
```

**Impact on Code:**

- **Individual board modeling** uses these scales for pore positioning
- **Hybrid pore matrix modeling** determines spatial distribution boundaries
- **Density distribution modeling** calculates normalized coordinate grids
- **Visualization limits** are derived from these scaling factors

---

## Pore Generation Parameters

### Pore Counts for Different Visualizations

```python
# Default Configuration
n_pores_individual = 600     # Individual board visualizations
n_pores_comparative = 400    # Comparative analysis between samples
n_pores_density = 500        # Density distribution modeling
n_pores_matrix = 800         # Matrix material modeling
n_pores_hybrid = 800         # Hybrid pore-matrix modeling

# Small Specimen Configuration
# Scaled by volume ratio: (equivalent_side / 160.0)³
n_pores_individual = max(50, int(600 * volume_ratio))
n_pores_comparative = max(30, int(400 * volume_ratio))
# ... similar scaling for all pore counts
```

**Impact on Code:**

- **Individual board modeling** (`individual_board_modeling.py`): Creates exactly `n_pores_individual` pores
- **Comparative analysis** (`comparative_analysis.py`): Generates `n_pores_comparative` pores per sample
- **Density distribution modeling** (`density_distribution_modeling.py`): Uses `n_pores_density` for spatial analysis
- **Matrix material modeling** (`matrix_material_modeling.py`): Distributes `n_pores_matrix` pores within matrix
- **Hybrid modeling** (`hybrid_pore_matrix_modeling.py`): Balances `n_pores_hybrid` pores with matrix particles

### Pore Size Parameters

```python
# Default Configuration
pore_scale_factor = 1.0      # No additional scaling
min_pore_radius = 0.03       # Minimum pore radius
max_pore_radius = 0.08       # Maximum pore radius

# Small Specimen Configuration
pore_scale_factor = 2.0      # Larger relative sizes for visibility
min_pore_radius = 0.01       # Smaller absolute minimum
max_pore_radius = 0.4        # Larger maximum for visibility
```

**Impact on Code:**

- **Data processor** (`data_processor.py`): Generates pore radii within these bounds
- **All visualization modules**: Render spheres with radii in this range
- **Density modeling**: Calculates volume fractions based on these size distributions
- **Matrix modeling**: Ensures pores don't overlap by respecting size constraints

---

## Matrix Material Parameters

### Matrix Fill Boundaries

```python
# Default Configuration
matrix_fill_x_bounds = (-1.95, 1.95)    # X-axis bounds for matrix fill
matrix_fill_y_bounds = (-1.95, 1.95)    # Y-axis bounds for matrix fill
matrix_fill_z_bounds = (-0.45, 0.45)    # Z-axis bounds for matrix fill
matrix_length_norm = 1.95               # Normalized length for matrix
matrix_width_norm = 1.95                # Normalized width for matrix

# Small Specimen Configuration
# Scaled proportionally with boundary margins
matrix_fill_x_bounds = (-1.95 * boundary_scale, 1.95 * boundary_scale)
matrix_fill_y_bounds = (-1.95 * boundary_scale, 1.95 * boundary_scale)
matrix_fill_z_bounds = (-0.45 * thickness_ratio, 0.45 * thickness_ratio)
```

**Impact on Code:**

- **Matrix material modeling**: Defines spatial boundaries for matrix particle placement
- **Hybrid modeling**: Ensures matrix particles stay within board boundaries
- **Collision detection**: Prevents matrix particles from overlapping with pores
- **Visual consistency**: Maintains proper scaling between pores and matrix

### Matrix Particle Properties

```python
# Default Configuration
matrix_base_particle_size = 0.8         # Base size for matrix particles
matrix_particle_size_variation = 1.5    # Size variation multiplier
matrix_base_particles = 15000           # Base number of matrix particles
matrix_particle_alpha = 0.7             # Transparency for matrix particles
matrix_batch_size = 1000                # Batch size for rendering performance
matrix_color_intensity_base = 0.3       # Base color intensity
matrix_color_intensity_variation = 0.7  # Color intensity variation

# Small Specimen Configuration
# Scaled by volume ratio for proportional density
matrix_base_particles = int(15000 * volume_ratio)
matrix_base_particle_size = 0.8 * size_scale_factor
```

**Impact on Code:**

- **Matrix material modeling**: Controls particle size distribution and density
- **Performance optimization**: Batch rendering for handling large particle counts
- **Visual realism**: Size and color variation creates realistic material appearance
- **Memory management**: Particle count affects memory usage and rendering speed

---

## Hybrid Modeling Parameters

### Hybrid Particle Counts

```python
# Default Configuration
base_particles_hybrid_main = 8000       # Main hybrid visualization particles
base_particles_hybrid_combined = 5000   # Combined hybrid view particles

# Small Specimen Configuration
# Scaled by volume ratio for proportional density
base_particles_hybrid_main = int(8000 * volume_ratio)
base_particles_hybrid_combined = int(5000 * volume_ratio)
```

**Impact on Code:**

- **Hybrid pore matrix modeling**: Balances pore and matrix particle densities
- **Multi-view rendering**: Different particle counts for different visualization types
- **Performance scaling**: Adjusts complexity based on specimen size
- **Visual balance**: Maintains proper pore-to-matrix ratios

### Hybrid Visualization Types

```python
hybrid_pore_counts = {
    'main': n_pores_hybrid,              # Main hybrid visualization
    'combined': n_pores_hybrid           # Combined hybrid view
}

hybrid_particle_counts = {
    'main': base_particles_hybrid_main,
    'combined': base_particles_hybrid_combined
}
```

**Impact on Code:**

- **Hybrid pore matrix modeling**: Provides different visualization modes
- **Comparative analysis**: Enables comparison between pore-only and hybrid views
- **Flexible rendering**: Adapts to different analysis requirements
- **Consistent scaling**: All hybrid views scale proportionally

### 3D Plotting Boundaries

```python
# Default Configuration
x_limits = (-2.2, 2.2)       # X-axis visualization range
y_limits = (-2.2, 2.2)       # Y-axis visualization range
z_limits = (-0.7, 0.7)       # Z-axis visualization range

# Small Specimen Configuration
# Scaled proportionally with boundary margins
x_limits = (-2.2 * boundary_scale, 2.2 * boundary_scale)
y_limits = (-2.2 * boundary_scale, 2.2 * boundary_scale)
z_limits = (-0.7 * thickness_ratio, 0.7 * thickness_ratio)
```

**Impact on Code:**

- **All visualization modules**: Set matplotlib 3D axis limits using these values
- **Camera positioning**: Ensures all elements fit within viewing frustum
- **Pore positioning**: Constrains pore generation to visible regions
- **Frame rendering**: Draws board boundaries at these limits

### Rendering Quality Settings

```python
sphere_u_resolution = 12     # Azimuthal sphere resolution
sphere_v_resolution = 8      # Polar sphere resolution
alpha_transparency = 0.9     # Sphere transparency
```

**Impact on Code:**

- **Individual board modeling**: Creates spheres with this resolution
- **Matrix modeling**: Balances visual quality vs. performance for thousands of particles
- **Hybrid modeling**: Renders both pores and matrix with consistent quality
- **Performance**: Higher resolution = slower rendering but better visual quality

### Camera and Viewing Parameters

```python
# Default Configuration
camera_position = np.array([3.0, 1.0, 1.0])
view_elevation = 30          # Camera elevation angle
view_azimuth = 60           # Camera azimuth angle
z_depth_bonus = 0.2         # Z-height visibility bonus

# Small Specimen Configuration
camera_position = np.array([3.0 * scale_factor, 1.0 * scale_factor, 1.0 * scale_factor])
view_elevation = 25         # Slightly lower for small specimens
view_azimuth = 45          # Different angle for clarity
z_depth_bonus = 0.3        # Increased depth perception
```

**Impact on Code:**

- **All visualization modules**: Set initial camera position and orientation
- **Depth sorting**: Z-depth bonus affects which elements appear in front
- **User interaction**: Default viewing angles for consistent presentation
- **Screenshot generation**: Standardized views for documentation

### Frame Visualization

```python
# Default Configuration
frame_color = '#FF8C00'      # Orange frame color
frame_linewidth = 1.5        # Frame line thickness
frame_alpha = 0.8           # Frame transparency

# Small Specimen Configuration
frame_linewidth = 2.0        # Thicker lines for small specimens
frame_alpha = 0.9           # Higher opacity for visibility
```

**Impact on Code:**

- **All modules with 3D visualization**: Draw board outline with these properties
- **Visual consistency**: Ensures uniform appearance across all visualizations
- **Clarity**: Frame helps distinguish board boundaries from background

### Aspect Ratio

```python
# Default Configuration
aspect_ratio = [4, 4, 1]     # Matches physical dimensions 160:160:40

# Small Specimen Configuration
aspect_ratio = [1, 1, thickness_ratio]  # Proportional to specimen
```

**Impact on Code:**

- **3D plot setup**: Sets axis scaling to maintain proportional appearance
- **Visual accuracy**: Ensures visualizations reflect true physical proportions
- **Measurement interpretation**: Critical for accurate spatial analysis

---

## Output Configuration

### Figure and Export Settings

```python
# Default Configuration
figure_size = (12, 8)        # Matplotlib figure size
dpi = 300                   # Figure resolution for saving
output_format = 'png'       # Default output format

# Small Specimen Configuration
figure_size = (10, 8)       # Slightly smaller for detailed views
dpi = 600                   # Higher resolution for microstructure detail
```

**Impact on Code:**

- **All visualization modules**: Create matplotlib figures with these dimensions
- **Export functionality**: Save images with specified DPI and format
- **Memory usage**: Higher DPI requires more memory for rendering
- **File sizes**: Affects storage requirements for generated images

---

## Physical Properties

### Mercury Intrusion Porosimetry (MIP) Parameters

```python
mercury_contact_angle = 140  # Mercury contact angle (degrees)
mercury_surface_tension = 0.485  # Surface tension (N/m)
```

**Impact on Code:**

- **Data processor**: Calculates pore size distributions from MIP data
- **Density modeling**: Converts pressure measurements to pore diameters
- **Physical validation**: Ensures simulated pores match experimental constraints

### Sample Identifiers

```python
sample_names = ['T1', 'T2', 'T3']
sample_colors = ['jet', 'viridis', 'plasma']
```

**Impact on Code:**

- **Comparative analysis**: Labels different sample types consistently
- **Color mapping**: Assigns unique colormaps to each sample type
- **Data organization**: Structures analysis results by sample identifier
- **Visualization legends**: Provides meaningful labels for plots

---

## Configuration Override System

### Script-Based Parameter Control

The `config_override.sh` script provides a powerful interface for modifying all configuration parameters without editing source code:

```bash
# Basic usage - run with current config
./config_override.sh

# Dry run - preview changes without execution
./config_override.sh --dry-run

# Scale all parameters proportionally
./config_override.sh --scale 0.5

# Override specific dimensions
./config_override.sh --length 200 --width 200 --thickness 50

# Override pore counts
./config_override.sh --pores-individual 800 --pores-matrix 1200

# Override matrix parameters
./config_override.sh --matrix-particles 20000 --matrix-size 0.6
```

### Override Parameter Categories

#### Dimensional Overrides

```bash
--length, --width, --thickness           # Board dimensions (mm)
--diameter, --tolerance                  # Cylindrical specimen conversion
```

#### Pore Count Overrides

```bash
--pores-all                             # Set all pore counts to same value
--pores-individual, --pores-comparative # Specific visualization types
--pores-density, --pores-matrix         # Analysis-specific counts
--pores-hybrid                          # Hybrid modeling pore count
```

#### Matrix Parameter Overrides

```bash
--matrix-particles                      # Base matrix particle count
--matrix-size                          # Base particle size
--matrix-size-variation                # Size variation multiplier
--matrix-alpha                         # Particle transparency
--matrix-batch-size                    # Rendering batch size
--matrix-color-base                    # Base color intensity
--matrix-color-variation               # Color intensity variation
```

#### Visualization Overrides

```bash
--figure-size                          # Figure dimensions
--dpi                                  # Resolution
--elevation, --azimuth                 # Camera angles
--alpha                               # Overall transparency
--format                              # Output format
```

### Scaling System

The override system includes intelligent scaling that maintains proportions:

```bash
# Scale all parameters by 50%
./config_override.sh --scale 0.5

# Scale with custom parameters
./config_override.sh --scale 0.8 --pores-all 1000
```

**Scaling Effects:**

- **Dimensions**: All board dimensions scaled proportionally
- **Pore counts**: Scaled by volume ratio (scale³)
- **Matrix particles**: Scaled by volume ratio for consistent density
- **Coordinate bounds**: Scaled to maintain relative positioning
- **Particle sizes**: Optionally scaled for visibility

---

## Scaling and Performance

### Automatic Scaling Logic

```python
# Volume-based scaling for particle counts
volume_ratio = (new_length / default_length) * \
               (new_width / default_width) * \
               (new_thickness / default_thickness)

scaled_pore_count = max(minimum_count, int(base_count * volume_ratio))
scaled_matrix_particles = int(base_particles * volume_ratio)
```

### Performance Optimization

```python
# Default Configuration (High Quality)
matrix_base_particles = 15000          # High detail
matrix_batch_size = 1000               # Moderate batching
dpi = 300                              # Standard resolution

# Performance Configuration (Fast Rendering)
matrix_base_particles = 5000           # Reduced detail
matrix_batch_size = 2000               # Larger batches
dpi = 150                              # Lower resolution
```

**Impact on Code:**

- **Rendering speed**: Lower particle counts and larger batches improve performance
- **Memory usage**: Fewer particles reduce memory requirements
- **Visual quality**: Trade-off between speed and detail
- **Scalability**: Enables analysis of various specimen sizes

### Memory Management

```python
# Memory-conscious settings for large specimens
if total_particles > 50000:
    matrix_batch_size = min(5000, total_particles // 10)
    enable_memory_optimization = True
    use_progressive_rendering = True
```

### Matrix Material Particle Counts

```python
# Default Configuration
base_particles_matrix = 15000           # Matrix material modeling
base_particles_hybrid_main = 8000       # Hybrid main visualization
base_particles_hybrid_combined = 5000   # Hybrid combined view

# Small Specimen Configuration
# Scaled by volume ratio for proportional density
base_particles_matrix = int(15000 * volume_ratio)
base_particles_hybrid_main = int(8000 * volume_ratio)
base_particles_hybrid_combined = int(5000 * volume_ratio)
```

**Impact on Code:**

- **Matrix material modeling**: Generates exactly this many matrix particles
- **Hybrid modeling**: Balances pore and matrix particle densities
- **Performance**: More particles = higher detail but slower rendering
- **Memory usage**: Particle count directly affects memory requirements

---

## Coordinate Bounds

### Default Positioning Boundaries

```python
# Default Configuration
default_x_bounds = (-1.95, 1.95)       # 5% margin from edges
default_y_bounds = (-1.95, 1.95)       # 5% margin from edges
default_z_bounds = (-0.45, 0.45)       # 10% margin from top/bottom

# Small Specimen Configuration
# Scaled proportionally with boundary margins
default_x_bounds = (-1.95 * boundary_scale, 1.95 * boundary_scale)
default_y_bounds = (-1.95 * boundary_scale, 1.95 * boundary_scale)
default_z_bounds = (-0.45 * thickness_ratio, 0.45 * thickness_ratio)
```

**Impact on Code:**

- **Pore positioning**: Constrains random pore placement to avoid edge effects
- **Matrix particle distribution**: Ensures particles remain within board boundaries
- **Collision detection**: Defines valid regions for element placement
- **Visual margins**: Prevents elements from appearing cut off at edges

---

## Positioning Parameters

### Margin and Distribution Factors

```python
edge_margin_factor = 0.95        # 5% margin from edges
z_margin_factor = 0.8            # 20% margin from top/bottom
diagonal_pore_ratio = 0.25       # 25% of pores in diagonal pattern
jitter_strength = 0.03           # Position jitter strength
z_jitter_factor = 0.5            # Reduced jitter in Z direction
```

**Impact on Code:**

- **Individual board modeling**: Creates realistic pore distributions
- **Matrix modeling**: Prevents matrix particles from clustering at edges
- **Diagonal patterns**: Adds structured arrangement to some pores
- **Randomization**: Jitter prevents overly regular patterns
- **Z-direction control**: Reduced vertical jitter maintains board structure

### Edge and Corner Positioning

```python
edge_position_factor = 0.9       # Edge position randomness
corner_position_factor = 0.85    # Corner position randomness
```

**Impact on Code:**

- **Pore distribution**: Controls how close pores can be to board edges
- **Realistic modeling**: Prevents unrealistic clustering at corners
- **Visual quality**: Maintains balanced appearance across board surface
- **Structural integrity**: Reflects real material constraints

---

## Particle Size Parameters

### Size and Color Variation

```python
particle_base_size = 0.8         # Base particle size
particle_size_variation = 1.5    # Size variation multiplier
color_intensity_base = 0.25      # Base color intensity
color_intensity_variation = 0.6  # Color intensity variation
pore_color_intensity_base = 0.8  # Base pore color intensity
pore_color_intensity_variation = 0.2  # Pore color intensity variation
```

**Impact on Code:**

- **Matrix material modeling**: Creates varied particle sizes for realism
- **Visual distinction**: Different color intensities help distinguish elements
- **Pore highlighting**: Higher pore color intensity makes pores more visible
- **Realistic appearance**: Size variation mimics real material heterogeneity

---

## Configuration Switching

### Global Configuration Management

```python
CONFIG = MaterialConfig("default")  # Global instance

def set_configuration(config_name: str):
    """Switch between configurations"""
    global CONFIG
    CONFIG = MaterialConfig(config_name)
```

**Impact on Code:**

- **All modules**: Import and use the global CONFIG instance
- **Runtime switching**: Can change configurations without restarting
- **Consistency**: Ensures all modules use the same parameter set
- **Debugging**: Easy to test different configurations

### Convenience Functions

```python
def get_board_dimensions():
    """Get current board dimensions in mm."""

def get_visualization_limits():
    """Get current visualization axis limits."""

def get_pore_count(visualization_type: str):
    """Get pore count for specific visualization type."""
```

**Impact on Code:**

- **Simplified access**: Modules don't need to know internal config structure
- **Type safety**: Specific functions for specific parameter types
- **Code readability**: Clear intention of what parameters are needed

---

## Impact on Application Modules

### `individual_board_modeling.py`

- Uses `n_pores_individual` for pore count
- Applies `board dimensions` for scaling
- Uses `visualization parameters` for 3D rendering
- Respects `coordinate bounds` for pore placement

### `comparative_analysis.py`

- Uses `n_pores_comparative` for each sample
- Applies `sample_names` and `sample_colors` for identification
- Uses `figure_size` and `dpi` for output quality
- Respects `positioning parameters` for balanced layouts

### `density_distribution_modeling.py`

- Uses `n_pores_density` for spatial analysis
- Applies `physical properties` for realistic modeling
- Uses `coordinate bounds` for density calculations
- Respects `aspect_ratio` for accurate spatial representation

### `matrix_material_modeling.py`

- Uses `matrix_base_particles` for particle count
- Applies `matrix_fill_*_bounds` for spatial boundaries
- Uses `matrix_base_particle_size` and `matrix_particle_size_variation` for size distribution
- Respects `matrix_batch_size` for rendering performance
- Uses `matrix_color_intensity_*` parameters for visual appearance
- Applies `matrix_particle_alpha` for transparency

### `hybrid_pore_matrix_modeling.py`

- Uses `n_pores_hybrid` and `base_particles_hybrid_*` for element counts
- Balances pore and matrix element densities using all matrix parameters
- Applies all `visualization parameters` and `coordinate bounds`
- Uses `positioning parameters` for spatial organization
- Integrates matrix fill boundaries for consistent placement
- Handles multiple hybrid visualization modes (main, combined)

### `density_distribution_modeling.py`

- Uses `n_pores_density` for spatial analysis
- Applies `dpi` parameter from config instead of hardcoded values
- Uses `physical properties` for realistic modeling
- Uses `coordinate bounds` for density calculations
- Respects `aspect_ratio` for accurate spatial representation

### `data_processor.py`

- Uses `physical properties` for data interpretation
- Applies `board dimensions` for coordinate scaling
- Uses `pore size parameters` for size distributions
- Respects `output configuration` for data export

### `utils.py`

- Provides configuration access functions
- Handles parameter validation
- Manages coordinate transformations
- Supports configuration switching

---

## Usage Examples

### Using Configuration Override Script

```bash
# Basic execution with current configuration
python main.py  # Standard execution
./config_override.sh  # Equivalent using override script

# Preview changes without execution
./config_override.sh --dry-run

# Scale specimen to 50% of original size
./config_override.sh --scale 0.5

# Custom dimensions and parameters
./config_override.sh --length 200 --width 200 --thickness 50 \
  --pores-all 1000 --matrix-particles 20000 --dpi 600

# Small specimen with optimized parameters
./config_override.sh --diameter 10 --tolerance 1 \
  --pores-all 300 --matrix-particles 5000 --alpha 0.95
```

### Accessing Configuration in Code

```python
from app.config import get_config

# Get current configuration
config = get_config()

# Access matrix parameters
matrix_params = config.get_matrix_parameters()
bounds = config.get_coordinate_bounds()
particle_counts = config.get_particle_counts()

# Access specific parameters
board_dims = config.get_board_dimensions()
pore_count = config.n_pores_individual
matrix_size = config.matrix_base_particle_size
```

### Custom Configuration Modifications

```python
# Modify parameters for specific analysis
config = get_config()
config.n_pores_individual = 1000           # Increase pore density
config.matrix_base_particles = 20000       # Increase matrix detail
config.figure_size = (16, 12)              # Larger output figures
config.dpi = 600                           # Higher resolution
```

### Matrix and Hybrid Parameter Access

```python
# Get matrix-specific parameters
matrix_config = config.get_matrix_parameters()
x_bounds = matrix_config['x_bounds']
particle_size = matrix_config['base_size']
alpha = matrix_config['alpha']

# Get hybrid particle counts
hybrid_counts = config.get_particle_counts()
main_particles = hybrid_counts['hybrid_main']
combined_particles = hybrid_counts['hybrid_combined']
```

---

## Enhanced Features

### Complete Parameterization

The enhanced configuration system eliminates all hardcoded values:

- **No fallback logic**: All modules use configuration parameters exclusively
- **Matrix fill parameters**: Complete control over matrix material properties
- **Hybrid modeling**: Full parameterization of combined pore-matrix visualizations
- **Scaling support**: Intelligent scaling maintains proportions and densities
- **Override capability**: Script-based parameter modification without code changes

### Validation and Consistency

```python
# Configuration validation
def validate_config():
    """Validate all configuration parameters for consistency."""
    config = get_config()

    # Check dimension consistency
    assert config.board_length_mm > 0
    assert config.board_width_mm > 0
    assert config.board_thickness_mm > 0

    # Check pore count minimums
    assert config.n_pores_individual >= 10
    assert config.matrix_base_particles >= 100

    # Check bounds consistency
    bounds = config.get_coordinate_bounds()
    assert bounds['x_bounds'][1] > bounds['x_bounds'][0]
```

### Performance Optimization Guidelines

```python
# Recommended settings for different use cases

# High Quality (Publication)
config.dpi = 600
config.matrix_base_particles = 20000
config.matrix_batch_size = 500

# Standard Quality (Analysis)
config.dpi = 300
config.matrix_base_particles = 15000
config.matrix_batch_size = 1000

# Fast Preview (Development)
config.dpi = 150
config.matrix_base_particles = 5000
config.matrix_batch_size = 2000
```

---

## Best Practices

1. **Always use configuration parameters** instead of hardcoding values
2. **Use the config override script** for parameter modifications instead of editing code
3. **Test with --dry-run** before running actual analysis
4. **Scale appropriately** for different specimen sizes using --scale parameter
5. **Monitor performance** when increasing particle counts or resolution
6. **Validate parameter changes** using the configuration summary
7. **Document custom modifications** for reproducibility
8. **Use convenience functions** for common parameter access
9. **Consider memory implications** when increasing matrix particle counts
10. **Maintain aspect ratios** when modifying dimensions
11. **Test output quality** when changing DPI or figure sizes
12. **Use matrix parameters** to control material appearance and density
13. **Balance pore and matrix counts** in hybrid visualizations for optimal results

---

## Configuration Summary

The enhanced configuration system provides:

- **Complete parameterization** of all modeling aspects
- **Script-based override** capabilities without code modification
- **Intelligent scaling** that maintains proportions and densities
- **Matrix material modeling** with full parameter control
- **Hybrid visualizations** combining pores and matrix materials
- **Performance optimization** through configurable batch sizes and particle counts
- **Consistent coordinate systems** across all visualization types
- **Reproducible results** through centralized parameter management

This system ensures that all modeling results are reproducible, scalable, and can be easily adapted to different experimental configurations while maintaining the highest standards of scientific rigor and visual quality. 2. **Test visualizations** with both default and small specimen configurations 3. **Validate parameter changes** using the configuration summary 4. **Document custom modifications** for reproducibility 5. **Use convenience functions** for common parameter access 6. **Consider performance implications** when increasing particle/pore counts 7. **Maintain aspect ratios** when modifying dimensions 8. **Test output quality** when changing DPI or figure sizes

---

This configuration system ensures consistency, reproducibility, and flexibility across the entire 3D pore structure modeling application while maintaining clear separation between experimental parameters and analysis code.
