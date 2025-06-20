# Configuration System Guide

## Overview

The 3D Pore Structure Modeling system now includes a robust configuration management system that allows you to easily switch between different experimental scenarios without modifying the core analysis code.

## Quick Start

### Method 1: Change Configuration in main.py

Edit the `CONFIG_TYPE` variable in `main.py`:

```python
# In main.py, change this line:
CONFIG_TYPE = "default"        # Standard 160×160×40mm boards
# To:
CONFIG_TYPE = "small_specimen" # Small 10±1mm diameter specimens
```

Then run:

```bash
python main.py
```

### Method 2: Programmatic Configuration Switching

```python
from app.config import set_configuration, get_config

# Switch to small specimen testing
set_configuration("small_specimen")

# Run your analysis...
# All visualizations will automatically use the new parameters

# Switch back to default
set_configuration("default")
```

### Method 3: Test Configuration System

Run the configuration test script:

```bash
python test_config.py
```

This will generate test visualizations for both configurations and show parameter comparisons.

## Available Configurations

### 1. Default Configuration (`"default"`)

- **Physical dimensions**: 160 × 160 × 40 mm rectangular boards
- **Use case**: Standard CSA cement board testing
- **Pore counts**: 600 (individual), 400 (comparative), 800 (density)
- **Visualization**: Full-scale 3D rendering with standard resolution

### 2. Small Specimen Configuration (`"small_specimen"`)

- **Physical dimensions**: 10 ± 1 mm diameter circular specimens (converted to equivalent square)
- **Use case**: High-resolution microstructure analysis
- **Pore counts**: Automatically scaled based on volume ratio
- **Visualization**: Higher resolution rendering for detailed analysis

## Configuration Parameters

The configuration system centralizes all key parameters:

### Physical Dimensions

- Board geometry (length, width, thickness in mm)
- Normalized coordinate scaling for visualization
- Aspect ratios and viewing angles

### Pore Generation

- Number of pores for different visualization types
- Pore size scaling factors and limits
- Spatial distribution parameters

### Visualization Quality

- Sphere rendering resolution (u/v subdivisions)
- Transparency and color settings
- Camera positioning and depth sorting

### Output Settings

- Figure size and DPI
- File format and compression
- Axis limits and frame styling

## Adding New Configurations

To add a new configuration, edit `app/config.py`:

1. Add a new method in the `MaterialConfig` class:

```python
def _load_your_config_name(self):
    # Set your parameters here
    self.board_length_mm = your_length
    self.board_width_mm = your_width
    # ... etc
```

2. Add the case to `_load_configuration()`:

```python
elif config_name == "your_config_name":
    self._load_your_config_name()
```

3. Use it:

```python
set_configuration("your_config_name")
```

## Examples

### Switching Between Standard and Small Specimens

```python
# Load your data once
df = load_and_clean_data("dataset/pore_data.csv")
diams, intrs = sort_by_diameter(df)

# Generate standard board visualization
set_configuration("default")
create_individual_sample_visualization(
    diams[0], intrs[0], "T1", "out/standard_T1.png"
)

# Generate small specimen visualization
set_configuration("small_specimen")
create_individual_sample_visualization(
    diams[0], intrs[0], "T1", "out/small_T1.png"
)
```

### Comparing Configurations

```python
from app.config import get_config, get_board_dimensions

for config_name in ["default", "small_specimen"]:
    set_configuration(config_name)
    config = get_config()
    dims = get_board_dimensions()

    print(f"{config_name}: {dims} mm, {config.n_pores_individual} pores")
```

## Benefits

1. **No Code Duplication**: Same analysis code works for all configurations
2. **Easy Testing**: Switch between scenarios with one line change
3. **Parameter Consistency**: All related parameters update together
4. **Extensibility**: Easy to add new experimental scenarios
5. **Maintainability**: Centralized parameter management

## Files Modified

The following files now use the configuration system:

- `app/config.py` - Central configuration management
- `app/utils.py` - Board geometry and pore generation
- `app/individual_board_modeling.py` - Individual visualizations
- `app/comparative_analysis.py` - Comparative analysis
- `main.py` - Main script with configuration selection
- `test_config.py` - Configuration testing and demonstration

## Migration Notes

**Old approach** (hardcoded parameters):

```python
# Hardcoded in each file
x_bound, y_bound, z_bound = 1.9, 1.9, 0.4
n_pores = 600
sphere_resolution = 12
```

**New approach** (config-driven):

```python
config = get_config()
x_bound = config.length_scale * 0.95
n_pores = config.n_pores_individual
sphere_resolution = config.sphere_u_resolution
```

This ensures all parameters stay synchronized and makes testing different scenarios effortless.
