# Configuration Override Script - Complete Reference

## Overview

The `config_override.sh` script provides comprehensive parameter control for the Simple Pore Analysis system, including matrix material modeling, hybrid visualizations, and intelligent scaling. It enables modification of all configuration parameters without changing any source code files, ensuring reproducible and scalable modeling.

## Quick Start

### Basic Usage

```bash
# Run with current configuration
./config_override.sh

# Preview changes without execution (recommended first step)
./config_override.sh --dry-run

# Get help with all available parameters
./config_override.sh --help
```

### Common Scenarios

```bash
# Small specimen analysis (10mm diameter)
./config_override.sh --diameter 10 --tolerance 1

# High-quality output for publication
./config_override.sh --dpi 600 --figure-size "16,12" --format pdf

# Performance optimization (faster rendering)
./config_override.sh --pores-all 300 --matrix-particles 8000

# Scaled analysis (50% size)
./config_override.sh --scale 0.5
```

## Common Use Cases

### Performance Optimization (Faster Rendering)

```bash
# Reduce pore counts for faster execution
./config_override.sh --pores-all 200

# Specific pore count reductions
./config_override.sh --pores-individual 300 --pores-comparative 200
```

### High Quality Output

```bash
# High resolution output
./config_override.sh --dpi 600 --figure-size "16,12"

# Custom visualization settings
./config_override.sh --elevation 45 --azimuth 90 --alpha 0.8
```

### Material Testing Scenarios

#### Small Cylindrical Specimens

```bash
# 10mm diameter specimens (as requested)
./config_override.sh --diameter 10 --thickness 5

# 15mm diameter specimens
./config_override.sh --diameter 15 --thickness 10
```

#### Large Scale Testing

```bash
# Large boards
./config_override.sh --length 300 --width 300 --thickness 80

# With reduced pore counts for performance
./config_override.sh --length 300 --width 300 --thickness 80 --pores-all 400
```

## Parameter Reference

### Dimensional Parameters

| Parameter     | Description             | Range   | Default | Example          |
| ------------- | ----------------------- | ------- | ------- | ---------------- |
| `--diameter`  | Specimen diameter (mm)  | 1-100   | -       | `--diameter 10`  |
| `--tolerance` | Specimen tolerance (mm) | 0.1-10  | 1.0     | `--tolerance 1`  |
| `--length`    | Board length (mm)       | 10-1000 | 160.0   | `--length 160`   |
| `--width`     | Board width (mm)        | 10-1000 | 160.0   | `--width 160`    |
| `--thickness` | Board thickness (mm)    | 1-200   | 40.0    | `--thickness 40` |
| `--scale`     | Global scaling factor   | 0.1-5.0 | 1.0     | `--scale 0.5`    |

### Pore Count Parameters

| Parameter             | Description              | Range    | Default | Example                   |
| --------------------- | ------------------------ | -------- | ------- | ------------------------- |
| `--pores-all`         | Set all pore counts      | 10-10000 | -       | `--pores-all 500`         |
| `--pores-individual`  | Individual visualization | 10-5000  | 600     | `--pores-individual 600`  |
| `--pores-comparative` | Comparative analysis     | 10-5000  | 400     | `--pores-comparative 400` |
| `--pores-density`     | Density modeling         | 10-5000  | 500     | `--pores-density 500`     |
| `--pores-matrix`      | Matrix modeling          | 10-5000  | 800     | `--pores-matrix 800`      |
| `--pores-hybrid`      | Hybrid modeling          | 10-5000  | 800     | `--pores-hybrid 800`      |

### Matrix Material Parameters

| Parameter                  | Description                | Range     | Default | Example                        |
| -------------------------- | -------------------------- | --------- | ------- | ------------------------------ |
| `--matrix-particles`       | Base matrix particle count | 100-50000 | 15000   | `--matrix-particles 20000`     |
| `--matrix-size`            | Base particle size         | 0.1-2.0   | 0.8     | `--matrix-size 0.6`            |
| `--matrix-size-variation`  | Size variation multiplier  | 1.0-3.0   | 1.5     | `--matrix-size-variation 2.0`  |
| `--matrix-alpha`           | Particle transparency      | 0.1-1.0   | 0.7     | `--matrix-alpha 0.8`           |
| `--matrix-batch-size`      | Rendering batch size       | 100-5000  | 1000    | `--matrix-batch-size 2000`     |
| `--matrix-color-base`      | Base color intensity       | 0.0-1.0   | 0.3     | `--matrix-color-base 0.4`      |
| `--matrix-color-variation` | Color intensity variation  | 0.0-1.0   | 0.7     | `--matrix-color-variation 0.5` |

### Hybrid Modeling Parameters

| Parameter                     | Description               | Range      | Default | Example                            |
| ----------------------------- | ------------------------- | ---------- | ------- | ---------------------------------- |
| `--hybrid-main-particles`     | Main hybrid particles     | 1000-30000 | 8000    | `--hybrid-main-particles 10000`    |
| `--hybrid-combined-particles` | Combined hybrid particles | 1000-20000 | 5000    | `--hybrid-combined-particles 6000` |

### Visualization Parameters

| Parameter       | Description          | Range           | Default | Example                 |
| --------------- | -------------------- | --------------- | ------- | ----------------------- |
| `--figure-size` | Figure size (W,H)    | -               | "12,8"  | `--figure-size "16,12"` |
| `--dpi`         | Resolution           | 72-1200         | 300     | `--dpi 600`             |
| `--elevation`   | Camera elevation (°) | -90 to 90       | 30      | `--elevation 45`        |
| `--azimuth`     | Camera azimuth (°)   | 0-360           | 60      | `--azimuth 90`          |
| `--alpha`       | Overall transparency | 0.0-1.0         | 0.9     | `--alpha 0.8`           |
| `--format`      | Output format        | png,jpg,pdf,svg | png     | `--format pdf`          |

### Pore Size Parameters

| Parameter           | Description         | Range     | Default | Example                  |
| ------------------- | ------------------- | --------- | ------- | ------------------------ |
| `--min-pore-radius` | Minimum pore radius | 0.001-1.0 | 0.03    | `--min-pore-radius 0.02` |
| `--max-pore-radius` | Maximum pore radius | 0.01-2.0  | 0.08    | `--max-pore-radius 0.10` |

## Advanced Usage Examples

### High-Detail Matrix Analysis

```bash
# Maximum detail for matrix structure analysis
./config_override.sh \
  --matrix-particles 25000 \
  --matrix-size 0.6 \
  --matrix-alpha 0.8 \
  --dpi 600 \
  --format pdf
```

### Performance-Optimized Workflow

```bash
# Fast preview for development
./config_override.sh \
  --pores-all 200 \
  --matrix-particles 5000 \
  --matrix-batch-size 2000 \
  --dpi 150

# Production quality after preview approval
./config_override.sh \
  --pores-all 800 \
  --matrix-particles 15000 \
  --dpi 300
```

### Scaling Experiments

```bash
# Compare different scales while maintaining proportions
./config_override.sh --scale 0.25  # 25% size
./config_override.sh --scale 0.5   # 50% size
./config_override.sh --scale 1.0   # Original size
./config_override.sh --scale 2.0   # 200% size
```

### Small Specimen Detailed Analysis

```bash
# Optimized for 10mm diameter specimens
./config_override.sh \
  --diameter 10 \
  --tolerance 1 \
  --pores-all 300 \
  --matrix-particles 8000 \
  --matrix-size 0.9 \
  --dpi 600 \
  --alpha 0.95 \
  --elevation 25 \
  --azimuth 45
```

### Hybrid Visualization Optimization

```bash
# Balanced hybrid modeling
./config_override.sh \
  --pores-hybrid 600 \
  --hybrid-main-particles 8000 \
  --hybrid-combined-particles 5000 \
  --matrix-particles 12000 \
  --alpha 0.85
```

### Publication-Quality Output

```bash
# High-resolution figures for academic publication
./config_override.sh \
  --dpi 600 \
  --figure-size "16,12" \
  --format pdf \
  --alpha 0.95 \
  --matrix-alpha 0.8 \
  --elevation 30 \
  --azimuth 60
```

## Intelligent Scaling System

### How Scaling Works

The `--scale` parameter applies intelligent scaling to maintain physical realism:

```bash
# Example: 50% scaling
./config_override.sh --scale 0.5
```

**Scaling Effects:**

- **Dimensions**: Length, width, thickness × 0.5
- **Pore counts**: Original × (0.5)³ = Original × 0.125
- **Matrix particles**: Original × (0.5)³ = Original × 0.125
- **Coordinate bounds**: All bounds × 0.5
- **Particle sizes**: Can be optionally scaled for visibility

### Volume-Based Scaling Logic

```bash
# For 50% linear scale:
# Volume ratio = 0.5³ = 0.125
# Particle density maintained by scaling counts proportionally
# Visual elements scaled to maintain proper proportions
```

### Override Scaling

```bash
# Scale dimensions but keep original particle counts
./config_override.sh --scale 0.5 --pores-all 600 --matrix-particles 15000

# Custom scaling with specific adjustments
./config_override.sh --scale 0.8 --pores-hybrid 1000 --matrix-size 0.9
```

## Examples for Specific Research Scenarios

### Small Specimen Analysis (Your Use Case)

```bash
# Small square specimens with 10 ± 1 mm diameter
./config_override.sh --diameter 10 --tolerance 1 --thickness 5

# With optimized visualization for small specimens
./config_override.sh \
  --diameter 10 \
  --tolerance 1 \
  --thickness 5 \
  --pores-all 250 \
  --dpi 600 \
  --alpha 0.95
```

### Rapid Prototyping

```bash
# Fast execution for testing
./config_override.sh --pores-all 100 --dpi 150
```

### Publication Quality

```bash
# High quality figures for papers
./config_override.sh \
  --dpi 600 \
  --figure-size "16,12" \
  --format pdf \
  --alpha 0.95
```

## Error Handling

The script includes comprehensive validation:

- **Parameter validation**: Ensures all values are within acceptable ranges
- **Type checking**: Validates numeric vs integer parameters
- **File checking**: Verifies required files exist
- **Cleanup**: Automatically removes temporary files after execution

## Files Created/Modified

The script creates temporary files that are automatically cleaned up:

- `temp_config_override.py` - Temporary configuration override
- `main_temp.py` - Temporary main file with configuration injection
- `main.py.backup` - Backup of original main.py (automatically restored)

## Troubleshooting

### Script Execution Issues

```bash
# Make sure script is executable
chmod +x config_override.sh

# Check if script exists and is in current directory
ls -la config_override.sh
```

### Parameter Validation Errors

```bash
# Use dry-run to check parameter validity
./config_override.sh --your-parameters --dry-run

# Check parameter ranges in help output
./config_override.sh --help
```

### Python Environment Issues

```bash
# Ensure Python environment is activated
source .venv/bin/activate  # or your environment activation command

# Check if required packages are installed
pip install -r requirements.txt

# Verify Python version compatibility
python --version
```

### Memory and Performance Issues

```bash
# Reduce particle counts for large specimens
./config_override.sh --scale 2.0 --matrix-particles 8000 --pores-all 400

# Increase batch size for better memory management
./config_override.sh --matrix-batch-size 2000

# Use lower DPI for faster rendering
./config_override.sh --dpi 150
```

### Configuration Debugging

```bash
# Use verbose mode for detailed output
./config_override.sh --your-parameters --verbose

# Compare configurations with dry-run
./config_override.sh --dry-run > current_config.txt
./config_override.sh --scale 0.5 --dry-run > scaled_config.txt
diff current_config.txt scaled_config.txt
```

### Matrix Visualization Issues

```bash
# If matrix particles don't appear properly
./config_override.sh --matrix-alpha 0.8 --matrix-color-base 0.4

# If matrix is too dense/sparse
./config_override.sh --matrix-particles 10000  # adjust count

# If matrix particles are too large/small
./config_override.sh --matrix-size 0.6 --matrix-size-variation 1.2
```

## Output Files and Results

### Generated Files

The script produces the same output files as `python main.py`:

```
out/
├── combined_pores_matrix_filled.png     # Matrix-filled combined view
├── T1_pores_matrix_combined.png         # Hybrid T1 sample
├── T2_pores_matrix_combined.png         # Hybrid T2 sample
├── T3_pores_matrix_combined.png         # Hybrid T3 sample
├── matrix_filled_clean.png              # Pure matrix visualization
├── density_filled_clean.png             # Density distribution
├── T1_individual_clean.png              # Individual sample views
├── T2_individual_clean.png
├── T3_individual_clean.png
└── comparative_analysis.png             # Comparative analysis
```

### Result Validation

```bash
# Compare file sizes and modification times
ls -la out/*.png

# Visual inspection workflow
./config_override.sh --dry-run           # Preview parameters
./config_override.sh                     # Generate results
# Check output files for expected appearance
```

### Reproducibility

```bash
# Save configuration for reproducibility
./config_override.sh --your-parameters --dry-run > experiment_config.txt

# Reproduce exact results later
./config_override.sh $(cat experiment_config.txt | grep -E "^  -" | tr '\n' ' ')
```

## Best Practices

### Development Workflow

1. **Start with dry-run**: Always preview changes before execution
2. **Use scaling**: Test with smaller scales first for faster iteration
3. **Optimize performance**: Reduce particle counts during development
4. **Document parameters**: Save successful configurations for reuse

### Production Analysis

1. **Validate parameters**: Ensure all parameters are within acceptable ranges
2. **Monitor resources**: Watch memory usage with large particle counts
3. **Check output quality**: Verify all visualizations are generated correctly
4. **Archive configurations**: Save parameter sets for reproducible research

### Parameter Selection Guidelines

```bash
# For small specimens (< 20mm)
--pores-all 200-400
--matrix-particles 5000-10000
--dpi 600
--alpha 0.95

# For standard specimens (160mm boards)
--pores-all 600-800
--matrix-particles 15000-20000
--dpi 300
--alpha 0.9

# For large specimens (> 200mm)
--scale 1.2-2.0
--pores-all 800-1200
--matrix-particles 20000-30000
--matrix-batch-size 2000
```
