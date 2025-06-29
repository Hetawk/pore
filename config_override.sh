#!/bin/bash

# ==============================================================================
# Configuration Override Script for Simple Pore Analysis
# ==============================================================================
# 
# This script allows you to easily override configuration parameters without
# modifying the source code. It creates a temporary configuration override
# and runs the main application with the new settings.
#
# Usage Examples:
#   ./config_override.sh --diameter 10 --thickness 10      # Small specimen (config.py values)
#   ./config_override.sh --config small_specimen
#   ./config_override.sh --length 160 --width 160 --thickness 40  # Default board (config.py)
#   ./config_override.sh --pores-individual 600            # Default individual pores (config.py)
#   ./config_override.sh --help
#
# ==============================================================================

set -e  # Exit on any error

# Default values from config.py - will be overridden by command line arguments
CONFIG_TYPE=""
BOARD_LENGTH="160.0"           # Default: 160.0mm from config.py
BOARD_WIDTH="160.0"            # Default: 160.0mm from config.py
BOARD_THICKNESS="40.0"         # Default: 40.0mm from config.py
SCALE_FACTOR=""                # Scale factor for entire figure (e.g., 0.5 for 50% scale)
SPECIMEN_DIAMETER=""
SPECIMEN_TOLERANCE=""
N_PORES_INDIVIDUAL="600"       # Default: 600 from config.py
N_PORES_COMPARATIVE="400"      # Default: 400 from config.py
N_PORES_DENSITY="500"          # Default: 500 from config.py
N_PORES_MATRIX="800"           # Default: 800 from config.py
N_PORES_HYBRID="800"           # Default: 800 from config.py
MIN_PORE_RADIUS="0.03"         # Default: 0.03 from config.py
MAX_PORE_RADIUS="0.08"         # Default: 0.08 from config.py
MATRIX_FILL_X_BOUNDS="-1.95,1.95" # Default: (-1.95, 1.95) from config.py
MATRIX_FILL_Y_BOUNDS="-1.95,1.95" # Default: (-1.95, 1.95) from config.py
MATRIX_FILL_Z_BOUNDS="-0.45,0.45" # Default: (-0.45, 0.45) from config.py
MATRIX_LENGTH_NORM="1.95"      # Default: 1.95 from config.py
MATRIX_WIDTH_NORM="1.95"       # Default: 1.95 from config.py
MATRIX_BASE_PARTICLE_SIZE="0.8" # Default: 0.8 from config.py
MATRIX_PARTICLE_SIZE_VARIATION="1.5" # Default: 1.5 from config.py
MATRIX_BASE_PARTICLES="15000"   # Default: 15000 from config.py
MATRIX_PARTICLE_ALPHA="0.7"     # Default: 0.7 from config.py
MATRIX_BATCH_SIZE="1000"        # Default: 1000 from config.py
MATRIX_COLOR_INTENSITY_BASE="0.3" # Default: 0.3 from config.py
MATRIX_COLOR_INTENSITY_VARIATION="0.7" # Default: 0.7 from config.py
FIGURE_SIZE="12,8"             # Default: (12, 8) from config.py
DPI="300"                      # Default: 300 from config.py
VIEW_ELEVATION="30"            # Default: 30 from config.py
VIEW_AZIMUTH="60"              # Default: 60 from config.py
ALPHA_TRANSPARENCY="0.9"       # Default: 0.9 from config.py
OUTPUT_FORMAT="png"            # Default: 'png' from config.py
CLEANUP="true"
VERBOSE="false"
DRY_RUN="false"

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
BACKUP_FILE="${SCRIPT_DIR}/main.py.backup"
TEMP_CONFIG_FILE="${SCRIPT_DIR}/temp_config_override.py"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==============================================================================
# Helper Functions
# ==============================================================================

print_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Configuration Override Script for Simple Pore Analysis

OPTIONS:
    --config TYPE              Set configuration type (default, small_specimen)
    --scale VALUE              Scale entire figure by factor (e.g., 0.5 for 50%, 2.0 for 200%)
    --diameter VALUE           Set specimen diameter (mm) - for circular specimens
    --tolerance VALUE          Set specimen tolerance (mm) - for circular specimens  
    --length VALUE             Set board length (mm) - default: 160.0 from config.py
    --width VALUE              Set board width (mm) - default: 160.0 from config.py
    --thickness VALUE          Set board thickness (mm) - default: 40.0 from config.py
    
    --pores-individual VALUE   Number of pores for individual visualization - default: 600
    --pores-comparative VALUE  Number of pores for comparative analysis - default: 400
    --pores-density VALUE      Number of pores for density modeling - default: 500
    --pores-matrix VALUE       Number of pores for matrix modeling - default: 800
    --pores-hybrid VALUE       Number of pores for hybrid modeling - default: 800
    --pores-all VALUE          Set all pore counts to same value
    
    --min-pore-radius VALUE    Minimum pore radius - default: 0.03 from config.py
    --max-pore-radius VALUE    Maximum pore radius - default: 0.08 from config.py
    
    --matrix-x-bounds "MIN,MAX"  Matrix fill X boundaries - default: "-2.0,2.0"
    --matrix-y-bounds "MIN,MAX"  Matrix fill Y boundaries - default: "-2.0,2.0"
    --matrix-z-bounds "MIN,MAX"  Matrix fill Z boundaries - default: "-0.5,0.5"
    --matrix-len-norm VALUE    Matrix length normalization - default: 1.95
    --matrix-width-norm VALUE  Matrix width normalization - default: 1.95
    --matrix-base-size VALUE   Matrix base particle size - default: 0.005
    --matrix-size-var VALUE    Matrix particle size variation - default: 0.005

    --figure-size "W,H"        Figure size as "width,height" - default: "12,8" from config.py
    --dpi VALUE                Figure DPI/resolution - default: 300 from config.py
    --elevation VALUE          Camera elevation angle - default: 30 from config.py
    --azimuth VALUE            Camera azimuth angle - default: 60 from config.py
    --alpha VALUE              Sphere transparency (0.0-1.0) - default: 0.9 from config.py
    --format FORMAT            Output format (png, jpg, pdf, svg) - default: png from config.py
    
    --no-cleanup               Don't cleanup temporary files after execution
    --verbose                  Enable verbose output
    --dry-run                  Show what would be changed without executing
    --help                     Show this help message

EXAMPLES:
    # Test default configuration values from config.py
    $0 --length 160 --width 160 --thickness 40
    
    # Scale entire figure to 50% (like 10±1mm from 160×160×40mm default)
    $0 --scale 0.0625
    
    # Scale to small specimen size (10mm from 160mm = 0.0625 scale factor)
    $0 --scale 0.0625 --tolerance 1
    
    # Test default pore counts from config.py
    $0 --pores-individual 600 --pores-comparative 400 --pores-density 500
    
    # Test default visualization settings from config.py
    $0 --dpi 300 --figure-size "12,8" --elevation 30 --azimuth 60
    
    # Test default pore size range from config.py
    $0 --min-pore-radius 0.03 --max-pore-radius 0.08
    
    # Small specimen configuration (config.py small_specimen values)
    $0 --diameter 10 --tolerance 1 --thickness 10
    
    # Use predefined small specimen config
    $0 --config small_specimen
    
    # High quality output (override defaults)
    $0 --dpi 600 --figure-size "16,12"

EOF
}

log_info() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[INFO]${NC} $1"
    fi
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# ==============================================================================
# Parameter Validation Functions
# ==============================================================================

validate_numeric() {
    local value="$1"
    local name="$2"
    
    if ! [[ "$value" =~ ^[0-9]*\.?[0-9]+$ ]]; then
        log_error "Invalid numeric value for $name: $value"
        exit 1
    fi
}

validate_integer() {
    local value="$1"
    local name="$2"
    
    if ! [[ "$value" =~ ^[0-9]+$ ]]; then
        log_error "Invalid integer value for $name: $value"
        exit 1
    fi
}

validate_range() {
    local value="$1"
    local min="$2"
    local max="$3"
    local name="$4"
    
    if (( $(echo "$value < $min" | bc -l) )) || (( $(echo "$value > $max" | bc -l) )); then
        log_error "Value for $name ($value) must be between $min and $max"
        exit 1
    fi
}

# ==============================================================================
# Configuration Generation Functions
# ==============================================================================

generate_config_override() {
    cat << EOF > "$TEMP_CONFIG_FILE"
#!/usr/bin/env python3
"""
Temporary configuration override generated by config_override.sh
This file will be automatically cleaned up after execution.
"""

import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from config import MaterialConfig

class OverriddenMaterialConfig(MaterialConfig):
    """Configuration with runtime overrides."""
    
    def __init__(self, config_name: str = "default"):
        super().__init__(config_name)
        self._apply_overrides()
    
    def _apply_overrides(self):
        """Apply command-line overrides to configuration."""
EOF

    # Add scaling factor override (applies to entire figure proportionally)
    if [[ -n "$SCALE_FACTOR" ]]; then
        cat << EOF >> "$TEMP_CONFIG_FILE"
        
        # Apply scaling factor to entire figure
        import numpy as np
        scale_factor = $SCALE_FACTOR
        
        # Scale all dimensions proportionally
        self.board_length_mm = 160.0 * scale_factor
        self.board_width_mm = 160.0 * scale_factor  
        self.board_thickness_mm = 40.0 * scale_factor
        
        # Update normalized scales (maintain same proportions)
        self.length_scale = 2.0 * scale_factor
        self.width_scale = 2.0 * scale_factor
        self.thickness_scale = 0.5 * scale_factor
        
        # Scale visualization limits proportionally
        self.x_limits = (-2.2 * scale_factor, 2.2 * scale_factor)
        self.y_limits = (-2.2 * scale_factor, 2.2 * scale_factor)
        self.z_limits = (-0.7 * scale_factor, 0.7 * scale_factor)
        
        # Scale pore sizes proportionally
        self.min_pore_radius = 0.03 * scale_factor
        self.max_pore_radius = 0.08 * scale_factor
        
        # Scale coordinate bounds proportionally
        self.default_x_bounds = (-1.95 * scale_factor, 1.95 * scale_factor)
        self.default_y_bounds = (-1.95 * scale_factor, 1.95 * scale_factor)
        self.default_z_bounds = (-0.45 * scale_factor, 0.45 * scale_factor)
        
        # Scale camera position proportionally
        self.camera_position = np.array([3.0 * scale_factor, 1.0 * scale_factor, 1.0 * scale_factor])
        
        # Scale jitter proportionally
        self.jitter_strength = 0.03 * scale_factor
        
        # Adjust pore counts based on volume scaling (optional - maintains density)
        volume_scale = scale_factor ** 3
        if volume_scale < 1.0:  # For smaller scales, ensure minimum pore counts
            self.n_pores_individual = max(50, int(600 * volume_scale))
            self.n_pores_comparative = max(30, int(400 * volume_scale))
            self.n_pores_density = max(40, int(500 * volume_scale))
            self.n_pores_matrix = max(60, int(800 * volume_scale))
            self.n_pores_hybrid = max(60, int(800 * volume_scale))
            
            # Scale particle counts too
            self.base_particles_matrix = max(1000, int(15000 * volume_scale))
            self.base_particles_hybrid_main = max(500, int(8000 * volume_scale))
            self.base_particles_hybrid_combined = max(300, int(5000 * volume_scale))
        else:  # For larger scales, increase counts proportionally
            self.n_pores_individual = int(600 * volume_scale)
            self.n_pores_comparative = int(400 * volume_scale)
            self.n_pores_density = int(500 * volume_scale)
            self.n_pores_matrix = int(800 * volume_scale)
            self.n_pores_hybrid = int(800 * volume_scale)
            
            # Scale particle counts too
            self.base_particles_matrix = int(15000 * volume_scale)
            self.base_particles_hybrid_main = int(8000 * volume_scale)
            self.base_particles_hybrid_combined = int(5000 * volume_scale)
        
        # Adjust DPI based on scale (smaller scales need higher DPI for detail)
        if scale_factor < 0.5:
            self.dpi = int(300 / scale_factor)  # Higher DPI for small scales
        elif scale_factor > 2.0:
            self.dpi = max(150, int(300 / (scale_factor * 0.5)))  # Lower DPI for large scales
        # else keep default DPI of 300
        
        print(f"Applied scale factor {scale_factor}:")
        print(f"  Board dimensions: {self.board_length_mm:.1f} × {self.board_width_mm:.1f} × {self.board_thickness_mm:.1f} mm")
        print(f"  Pore size range: {self.min_pore_radius:.4f} - {self.max_pore_radius:.4f}")
        print(f"  Pore counts: Individual={self.n_pores_individual}, Matrix={self.n_pores_matrix}")
        print(f"  DPI adjusted to: {self.dpi}")
EOF
    fi

    # Add dimension overrides
    if [[ -n "$SPECIMEN_DIAMETER" ]]; then
        cat << EOF >> "$TEMP_CONFIG_FILE"
        
        # Override specimen diameter
        self.specimen_diameter_mm = $SPECIMEN_DIAMETER
        
        # Recalculate dependent values
        import numpy as np
        equivalent_side = self.specimen_diameter_mm / np.sqrt(np.pi) * 2
        self.board_length_mm = equivalent_side
        self.board_width_mm = equivalent_side
        
        # Update scales
        scale_factor = equivalent_side / 160.0
        self.length_scale = 2.0 * scale_factor
        self.width_scale = 2.0 * scale_factor
EOF
    fi

    if [[ -n "$SPECIMEN_TOLERANCE" ]]; then
        echo "        self.specimen_tolerance_mm = $SPECIMEN_TOLERANCE" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$BOARD_LENGTH" ]]; then
        cat << EOF >> "$TEMP_CONFIG_FILE"
        
        # Override board dimensions
        self.board_length_mm = $BOARD_LENGTH
        scale_factor = $BOARD_LENGTH / 160.0
        self.length_scale = 2.0 * scale_factor
EOF
    fi

    if [[ -n "$BOARD_WIDTH" ]]; then
        cat << EOF >> "$TEMP_CONFIG_FILE"
        self.board_width_mm = $BOARD_WIDTH
        scale_factor = $BOARD_WIDTH / 160.0
        self.width_scale = 2.0 * scale_factor
EOF
    fi

    if [[ -n "$BOARD_THICKNESS" ]]; then
        cat << EOF >> "$TEMP_CONFIG_FILE"
        self.board_thickness_mm = $BOARD_THICKNESS
        self.thickness_scale = 0.5 * ($BOARD_THICKNESS / 40.0)
        self.z_limits = (-0.7 * ($BOARD_THICKNESS / 40.0), 0.7 * ($BOARD_THICKNESS / 40.0))
EOF
    fi

    # Add pore count overrides
    if [[ -n "$N_PORES_INDIVIDUAL" ]]; then
        echo "        self.n_pores_individual = $N_PORES_INDIVIDUAL" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$N_PORES_COMPARATIVE" ]]; then
        echo "        self.n_pores_comparative = $N_PORES_COMPARATIVE" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$N_PORES_DENSITY" ]]; then
        echo "        self.n_pores_density = $N_PORES_DENSITY" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$N_PORES_MATRIX" ]]; then
        echo "        self.n_pores_matrix = $N_PORES_MATRIX" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$N_PORES_HYBRID" ]]; then
        echo "        self.n_pores_hybrid = $N_PORES_HYBRID" >> "$TEMP_CONFIG_FILE"
    fi

    # Add pore size overrides
    if [[ -n "$MIN_PORE_RADIUS" ]]; then
        echo "        self.min_pore_radius = $MIN_PORE_RADIUS" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MAX_PORE_RADIUS" ]]; then
        echo "        self.max_pore_radius = $MAX_PORE_RADIUS" >> "$TEMP_CONFIG_FILE"
    fi

    # Add matrix fill parameter overrides
    if [[ -n "$MATRIX_FILL_X_BOUNDS" ]]; then
        echo "        self.matrix_fill_x_bounds = ($MATRIX_FILL_X_BOUNDS)" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MATRIX_FILL_Y_BOUNDS" ]]; then
        echo "        self.matrix_fill_y_bounds = ($MATRIX_FILL_Y_BOUNDS)" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MATRIX_FILL_Z_BOUNDS" ]]; then
        echo "        self.matrix_fill_z_bounds = ($MATRIX_FILL_Z_BOUNDS)" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MATRIX_LENGTH_NORM" ]]; then
        echo "        self.matrix_length_norm = $MATRIX_LENGTH_NORM" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MATRIX_WIDTH_NORM" ]]; then
        echo "        self.matrix_width_norm = $MATRIX_WIDTH_NORM" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MATRIX_BASE_PARTICLE_SIZE" ]]; then
        echo "        self.matrix_base_particle_size = $MATRIX_BASE_PARTICLE_SIZE" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MATRIX_PARTICLE_SIZE_VARIATION" ]]; then
        echo "        self.matrix_particle_size_variation = $MATRIX_PARTICLE_SIZE_VARIATION" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MATRIX_BASE_PARTICLES" ]]; then
        echo "        self.matrix_base_particles = $MATRIX_BASE_PARTICLES" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MATRIX_PARTICLE_ALPHA" ]]; then
        echo "        self.matrix_particle_alpha = $MATRIX_PARTICLE_ALPHA" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MATRIX_BATCH_SIZE" ]]; then
        echo "        self.matrix_batch_size = $MATRIX_BATCH_SIZE" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MATRIX_COLOR_INTENSITY_BASE" ]]; then
        echo "        self.matrix_color_intensity_base = $MATRIX_COLOR_INTENSITY_BASE" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$MATRIX_COLOR_INTENSITY_VARIATION" ]]; then
        echo "        self.matrix_color_intensity_variation = $MATRIX_COLOR_INTENSITY_VARIATION" >> "$TEMP_CONFIG_FILE"
    fi

    # Override visualization parameters
    if [[ -n "$FIGURE_SIZE" ]]; then
        echo "        self.figure_size = (${FIGURE_SIZE})" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$DPI" ]]; then
        echo "        self.dpi = $DPI" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$VIEW_ELEVATION" ]]; then
        echo "        self.view_elevation = $VIEW_ELEVATION" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$VIEW_AZIMUTH" ]]; then
        echo "        self.view_azimuth = $VIEW_AZIMUTH" >> "$TEMP_CONFIG_FILE"
    fi

    if [[ -n "$ALPHA_TRANSPARENCY" ]]; then
        echo "        self.alpha_transparency = $ALPHA_TRANSPARENCY" >> "$TEMP_CONFIG_FILE"
    fi

    # Add comprehensive dimension override functions
    cat << 'EOF' >> "$TEMP_CONFIG_FILE"

    # === DIMENSION OVERRIDE FUNCTIONS ===
    def get_normalized_bounds(self):
        """Get normalized bounds based on current configuration"""
        length_norm = self.board_length_mm / 80.0  # 80 is half of default 160
        width_norm = self.board_width_mm / 80.0
        thickness_norm = self.board_thickness_mm / 20.0  # 20 is half of default 40
        
        return {
            'x_bounds': (-length_norm * 0.975, length_norm * 0.975),
            'y_bounds': (-width_norm * 0.975, width_norm * 0.975), 
            'z_bounds': (-thickness_norm * 0.9, thickness_norm * 0.9),
            'length_norm': length_norm,
            'width_norm': width_norm,
            'thickness_norm': thickness_norm
        }

    def get_dimension_scale_factors(self):
        """Get scaling factors for dimension-dependent calculations"""
        return {
            'length_scale': self.board_length_mm / 160.0,
            'width_scale': self.board_width_mm / 160.0,
            'thickness_scale': self.board_thickness_mm / 40.0,
            'volume_scale': (self.board_length_mm / 160.0) * (self.board_width_mm / 160.0) * (self.board_thickness_mm / 40.0)
        }
    
    def get_particle_counts(self):
        """Get base particle counts for different visualization types."""
        return {
            'matrix': getattr(self, 'base_particles_matrix', 15000),
            'hybrid_main': getattr(self, 'base_particles_hybrid_main', 8000),
            'hybrid_combined': getattr(self, 'base_particles_hybrid_combined', 5000)
        }

    def get_coordinate_bounds(self):
        """Get default coordinate bounds for element positioning."""
        return {
            'x_bounds': getattr(self, 'default_x_bounds', (-1.95, 1.95)),
            'y_bounds': getattr(self, 'default_y_bounds', (-1.95, 1.95)),
            'z_bounds': getattr(self, 'default_z_bounds', (-0.45, 0.45))
        }

    def get_positioning_parameters(self):
        """Get positioning and margin parameters."""
        return {
            'edge_margin_factor': getattr(self, 'edge_margin_factor', 0.95),
            'z_margin_factor': getattr(self, 'z_margin_factor', 0.8),
            'diagonal_pore_ratio': getattr(self, 'diagonal_pore_ratio', 0.25),
            'jitter_strength': getattr(self, 'jitter_strength', 0.03),
            'z_jitter_factor': getattr(self, 'z_jitter_factor', 0.5),
            'edge_position_factor': getattr(self, 'edge_position_factor', 0.9),
            'corner_position_factor': getattr(self, 'corner_position_factor', 0.85)
        }

    def get_particle_size_parameters(self):
        """Get particle sizing parameters."""
        return {
            'base_size': getattr(self, 'particle_base_size', 0.8),
            'size_variation': getattr(self, 'particle_size_variation', 1.5),
            'color_intensity_base': getattr(self, 'color_intensity_base', 0.25),
            'color_intensity_variation': getattr(self, 'color_intensity_variation', 0.6),
            'pore_color_intensity_base': getattr(self, 'pore_color_intensity_base', 0.8),
            'pore_color_intensity_variation': getattr(self, 'pore_color_intensity_variation', 0.2)
        }
EOF

    if [[ -n "$OUTPUT_FORMAT" ]]; then
        echo "        self.output_format = '$OUTPUT_FORMAT'" >> "$TEMP_CONFIG_FILE"
    fi

    cat << EOF >> "$TEMP_CONFIG_FILE"

# Override the global config instance
_config_instance = None

def set_configuration(config_name: str = "default"):
    """Set the global configuration with overrides."""
    global _config_instance
    _config_instance = OverriddenMaterialConfig(config_name)

def get_config():
    """Get the current configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = OverriddenMaterialConfig("default")
    return _config_instance

def get_board_dimensions():
    """Get board dimensions from current configuration."""
    config = get_config()
    return (config.board_length_mm, config.board_width_mm, config.board_thickness_mm)
EOF

    log_info "Generated configuration override file: $TEMP_CONFIG_FILE"
}

backup_main_file() {
    if [[ ! -f "$BACKUP_FILE" ]]; then
        cp "${SCRIPT_DIR}/main.py" "$BACKUP_FILE"
        log_info "Created backup of main.py"
    fi
}

modify_main_file() {
    log_info "Modifying main.py to use configuration override"
    
    # Create temporary main.py with import override
    cat << EOF > "${SCRIPT_DIR}/main_temp.py"
#!/usr/bin/env python3
"""
Temporary main file with configuration override
This file will be automatically cleaned up after execution.
"""

# Import override configuration instead of default
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import temp_config_override as config_override

# Replace the config module
sys.modules['app.config'] = config_override

EOF

    # Append the rest of the original main.py, skipping the first line (shebang)
    tail -n +2 "${SCRIPT_DIR}/main.py" >> "${SCRIPT_DIR}/main_temp.py"
    
    # Add dimension override patches to the temporary main file
    cat << 'EOF' >> "${SCRIPT_DIR}/main_temp.py"

# === DIMENSION OVERRIDE PATCHES ===
# Patch functions that have hardcoded dimensions

def patch_matrix_material_modeling():
    """Patch matrix_material_modeling.py to use dynamic dimensions"""
    import app.matrix_material_modeling as matrix_module
    import app.config as config
    
    original_create_matrix = matrix_module.create_matrix_filled_visualization
    
    def patched_create_matrix(*args, **kwargs):
        # Get current dimensions
        bounds = config.get_config().get_normalized_bounds()
        scales = config.get_config().get_dimension_scale_factors()
        
        # Monkey patch the hardcoded values in the module
        matrix_module.DIMENSION_BOUNDS = bounds
        matrix_module.SCALE_FACTORS = scales
        
        return original_create_matrix(*args, **kwargs)
    
    matrix_module.create_matrix_material_visualization = patched_create_matrix

def patch_hybrid_pore_matrix():
    """Patch hybrid_pore_matrix_modeling.py to use dynamic dimensions"""
    import app.hybrid_pore_matrix_modeling as hybrid_module
    import app.config as config
    
    original_create_hybrid = hybrid_module.create_combined_pores_matrix_visualization
    
    def patched_create_hybrid(*args, **kwargs):
        # Get current dimensions
        bounds = config.get_config().get_normalized_bounds()
        scales = config.get_config().get_dimension_scale_factors()
        
        # Monkey patch the hardcoded values in the module
        hybrid_module.DIMENSION_BOUNDS = bounds
        hybrid_module.SCALE_FACTORS = scales
        
        return original_create_hybrid(*args, **kwargs)
    
    hybrid_module.create_hybrid_pore_matrix_visualization = patched_create_hybrid

# Apply patches
patch_matrix_material_modeling()
patch_hybrid_pore_matrix()

EOF
    
    # Replace CONFIG_TYPE if specified
    if [[ -n "$CONFIG_TYPE" ]]; then
        sed -i.bak "s/CONFIG_TYPE = \".*\"/CONFIG_TYPE = \"$CONFIG_TYPE\"/" "${SCRIPT_DIR}/main_temp.py"
        rm -f "${SCRIPT_DIR}/main_temp.py.bak"
    fi
}

# ==============================================================================
# Cleanup Functions
# ==============================================================================

cleanup() {
    if [[ "$CLEANUP" == "true" ]]; then
        log_info "Cleaning up temporary files"
        rm -f "$TEMP_CONFIG_FILE"
        rm -f "${SCRIPT_DIR}/main_temp.py"
        rm -f "${SCRIPT_DIR}/main_temp.py.bak"
    else
        log_info "Temporary files preserved:"
        log_info "  - $TEMP_CONFIG_FILE"
        log_info "  - ${SCRIPT_DIR}/main_temp.py"
    fi
}

restore_main_file() {
    if [[ -f "$BACKUP_FILE" ]]; then
        cp "$BACKUP_FILE" "${SCRIPT_DIR}/main.py"
        rm -f "$BACKUP_FILE"
        log_info "Restored original main.py"
    fi
}

# Set up cleanup trap
trap cleanup EXIT

# ==============================================================================
# Command Line Parsing
# ==============================================================================

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --config)
            CONFIG_TYPE="$2"
            shift 2
            ;;
        --scale)
            SCALE_FACTOR="$2"
            validate_numeric "$SCALE_FACTOR" "scale"
            validate_range "$SCALE_FACTOR" "0.01" "10" "scale"
            shift 2
            ;;
        --diameter)
            SPECIMEN_DIAMETER="$2"
            validate_numeric "$SPECIMEN_DIAMETER" "diameter"
            validate_range "$SPECIMEN_DIAMETER" "1" "100" "diameter"
            shift 2
            ;;
        --tolerance)
            SPECIMEN_TOLERANCE="$2"
            validate_numeric "$SPECIMEN_TOLERANCE" "tolerance"
            validate_range "$SPECIMEN_TOLERANCE" "0.1" "10" "tolerance"
            shift 2
            ;;
        --length)
            BOARD_LENGTH="$2"
            validate_numeric "$BOARD_LENGTH" "length"
            validate_range "$BOARD_LENGTH" "10" "1000" "length"
            shift 2
            ;;
        --width)
            BOARD_WIDTH="$2"
            validate_numeric "$BOARD_WIDTH" "width"
            validate_range "$BOARD_WIDTH" "10" "1000" "width"
            shift 2
            ;;
        --thickness)
            BOARD_THICKNESS="$2"
            validate_numeric "$BOARD_THICKNESS" "thickness"
            validate_range "$BOARD_THICKNESS" "1" "200" "thickness"
            shift 2
            ;;
        --pores-individual)
            N_PORES_INDIVIDUAL="$2"
            validate_integer "$N_PORES_INDIVIDUAL" "pores-individual"
            validate_range "$N_PORES_INDIVIDUAL" "10" "5000" "pores-individual"
            shift 2
            ;;
        --pores-comparative)
            N_PORES_COMPARATIVE="$2"
            validate_integer "$N_PORES_COMPARATIVE" "pores-comparative"
            validate_range "$N_PORES_COMPARATIVE" "10" "5000" "pores-comparative"
            shift 2
            ;;
        --pores-density)
            N_PORES_DENSITY="$2"
            validate_integer "$N_PORES_DENSITY" "pores-density"
            validate_range "$N_PORES_DENSITY" "10" "5000" "pores-density"
            shift 2
            ;;
        --pores-matrix)
            N_PORES_MATRIX="$2"
            validate_integer "$N_PORES_MATRIX" "pores-matrix"
            validate_range "$N_PORES_MATRIX" "10" "5000" "pores-matrix"
            shift 2
            ;;
        --pores-hybrid)
            N_PORES_HYBRID="$2"
            validate_integer "$N_PORES_HYBRID" "pores-hybrid"
            validate_range "$N_PORES_HYBRID" "10" "5000" "pores-hybrid"
            shift 2
            ;;
        --pores-all)
            ALL_PORES="$2"
            validate_integer "$ALL_PORES" "pores-all"
            validate_range "$ALL_PORES" "10" "5000" "pores-all"
            N_PORES_INDIVIDUAL="$ALL_PORES"
            N_PORES_COMPARATIVE="$ALL_PORES"
            N_PORES_DENSITY="$ALL_PORES"
            N_PORES_MATRIX="$ALL_PORES"
            N_PORES_HYBRID="$ALL_PORES"
            shift 2
            ;;
        --min-pore-radius)
            MIN_PORE_RADIUS="$2"
            validate_numeric "$MIN_PORE_RADIUS" "min-pore-radius"
            validate_range "$MIN_PORE_RADIUS" "0.001" "1.0" "min-pore-radius"
            shift 2
            ;;
        --max-pore-radius)
            MAX_PORE_RADIUS="$2"
            validate_numeric "$MAX_PORE_RADIUS" "max-pore-radius"
            validate_range "$MAX_PORE_RADIUS" "0.01" "2.0" "max-pore-radius"
            shift 2
            ;;
        --matrix-x-bounds)
            MATRIX_FILL_X_BOUNDS="$2"
            shift 2
            ;;
        --matrix-y-bounds)
            MATRIX_FILL_Y_BOUNDS="$2"
            shift 2
            ;;
        --matrix-z-bounds)
            MATRIX_FILL_Z_BOUNDS="$2"
            shift 2
            ;;
        --matrix-len-norm)
            MATRIX_LENGTH_NORM="$2"
            validate_numeric "$MATRIX_LENGTH_NORM" "matrix length norm"
            shift 2
            ;;
        --matrix-width-norm)
            MATRIX_WIDTH_NORM="$2"
            validate_numeric "$MATRIX_WIDTH_NORM" "matrix width norm"
            shift 2
            ;;
        --matrix-base-size)
            MATRIX_BASE_PARTICLE_SIZE="$2"
            validate_numeric "$MATRIX_BASE_PARTICLE_SIZE" "matrix base particle size"
            shift 2
            ;;
        --matrix-size-var)
            MATRIX_PARTICLE_SIZE_VARIATION="$2"
            validate_numeric "$MATRIX_PARTICLE_SIZE_VARIATION" "matrix particle size variation"
            shift 2
            ;;
        --figure-size)
            FIGURE_SIZE="$2"
            if ! [[ "$FIGURE_SIZE" =~ ^[0-9]+,[0-9]+$ ]]; then
                log_error "Figure size must be in format 'width,height' (e.g., '12,8')"
                exit 1
            fi
            shift 2
            ;;
        --dpi)
            DPI="$2"
            validate_integer "$DPI" "dpi"
            validate_range "$DPI" "72" "1200" "dpi"
            shift 2
            ;;
        --elevation)
            VIEW_ELEVATION="$2"
            validate_numeric "$VIEW_ELEVATION" "elevation"
            validate_range "$VIEW_ELEVATION" "-90" "90" "elevation"
            shift 2
            ;;
        --azimuth)
            VIEW_AZIMUTH="$2"
            validate_numeric "$VIEW_AZIMUTH" "azimuth"
            validate_range "$VIEW_AZIMUTH" "0" "360" "azimuth"
            shift 2
            ;;
        --alpha)
            ALPHA_TRANSPARENCY="$2"
            validate_numeric "$ALPHA_TRANSPARENCY" "alpha"
            validate_range "$ALPHA_TRANSPARENCY" "0.0" "1.0" "alpha"
            shift 2
            ;;
        --format)
            OUTPUT_FORMAT="$2"
            if [[ ! "$OUTPUT_FORMAT" =~ ^(png|jpg|jpeg|pdf|svg)$ ]]; then
                log_error "Output format must be one of: png, jpg, jpeg, pdf, svg"
                exit 1
            fi
            shift 2
            ;;
        --no-cleanup)
            CLEANUP="false"
            shift
            ;;
        --verbose)
            VERBOSE="true"
            shift
            ;;
        --dry-run)
            DRY_RUN="true"
            shift
            ;;
        --micropore-color)
            MICROPORE_COLOR="$2"
            shift; shift
            ;;
        --mesopore-color)
            MESOPORE_COLOR="$2"
            shift; shift
            ;;
        --macropore-color)
            MACROPORE_COLOR="$2"
            shift; shift
            ;;
        --matrix-fill-color)
            MATRIX_FILL_COLOR="$2"
            shift; shift
            ;;
        --matrix-alpha)
            MATRIX_ALPHA="$2"
            shift; shift
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# ==============================================================================
# Main Execution
# ==============================================================================

# Validate pore radius relationship
if [[ -n "$MIN_PORE_RADIUS" && -n "$MAX_PORE_RADIUS" ]]; then
    if (( $(echo "$MIN_PORE_RADIUS >= $MAX_PORE_RADIUS" | bc -l) )); then
        log_error "Minimum pore radius ($MIN_PORE_RADIUS) must be less than maximum pore radius ($MAX_PORE_RADIUS)"
        exit 1
    fi
fi

# Show what would be changed in dry-run mode
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}DRY RUN MODE - No changes will be made${NC}"
    echo ""
    echo "Configuration overrides that would be applied:"
    
    [[ -n "$CONFIG_TYPE" ]] && echo "  - Configuration type: $CONFIG_TYPE"
    if [[ -n "$SCALE_FACTOR" ]]; then
        # Calculate scaled dimensions for display
        SCALED_LENGTH=$(echo "160.0 * $SCALE_FACTOR" | bc -l)
        SCALED_WIDTH=$(echo "160.0 * $SCALE_FACTOR" | bc -l)
        SCALED_THICKNESS=$(echo "40.0 * $SCALE_FACTOR" | bc -l)
        SCALED_MIN_PORE=$(echo "0.03 * $SCALE_FACTOR" | bc -l)
        SCALED_MAX_PORE=$(echo "0.08 * $SCALE_FACTOR" | bc -l)
        echo "  - Scale factor: ${SCALE_FACTOR} (entire figure scaled proportionally)"
        echo "    * Board dimensions: 160.0 × 160.0 × 40.0 mm → ${SCALED_LENGTH} × ${SCALED_WIDTH} × ${SCALED_THICKNESS} mm"
        echo "    * Pore size range: 0.03 - 0.08 → ${SCALED_MIN_PORE} - ${SCALED_MAX_PORE}"
    fi
    [[ -n "$SPECIMEN_DIAMETER" ]] && echo "  - Specimen diameter: ${SPECIMEN_DIAMETER}mm"
    [[ -n "$SPECIMEN_TOLERANCE" ]] && echo "  - Specimen tolerance: ±${SPECIMEN_TOLERANCE}mm"
    
    # Show board dimensions (scaled if scale factor is applied)
    if [[ -n "$SCALE_FACTOR" ]]; then
        # Don't show individual dimension overrides when scaling is applied
        [[ -z "$BOARD_LENGTH" && -z "$BOARD_WIDTH" && -z "$BOARD_THICKNESS" ]] && echo "  - Board dimensions: ${SCALED_LENGTH} × ${SCALED_WIDTH} × ${SCALED_THICKNESS} mm (scaled)"
    else
        [[ -n "$BOARD_LENGTH" ]] && echo "  - Board length: ${BOARD_LENGTH}mm"
        [[ -n "$BOARD_WIDTH" ]] && echo "  - Board width: ${BOARD_WIDTH}mm"
        [[ -n "$BOARD_THICKNESS" ]] && echo "  - Board thickness: ${BOARD_THICKNESS}mm"
    fi
    
    # Show pore counts (scaled if scale factor is applied)
    if [[ -n "$SCALE_FACTOR" ]]; then
        # Calculate scaled pore counts for display using Python for reliability
        VOLUME_SCALE=$(echo "$SCALE_FACTOR * $SCALE_FACTOR * $SCALE_FACTOR" | bc -l)
        
        # Use Python for more reliable calculations
        SCALED_INDIVIDUAL=$(python3 -c "
volume_scale = $VOLUME_SCALE
scaled = int(volume_scale * 600)
print(max(50, scaled))
")
        SCALED_COMPARATIVE=$(python3 -c "
volume_scale = $VOLUME_SCALE
scaled = int(volume_scale * 400)
print(max(30, scaled))
")
        SCALED_DENSITY=$(python3 -c "
volume_scale = $VOLUME_SCALE
scaled = int(volume_scale * 500)
print(max(40, scaled))
")
        SCALED_MATRIX=$(python3 -c "
volume_scale = $VOLUME_SCALE
scaled = int(volume_scale * 800)
print(max(60, scaled))
")
        SCALED_HYBRID=$(python3 -c "
volume_scale = $VOLUME_SCALE
scaled = int(volume_scale * 800)
print(max(60, scaled))
")
        
        echo "  - Pore counts (volume-scaled for ${SCALE_FACTOR} scale factor):"
        echo "    * Individual: 600 → ${SCALED_INDIVIDUAL} pores"
        echo "    * Comparative: 400 → ${SCALED_COMPARATIVE} pores"
        echo "    * Density: 500 → ${SCALED_DENSITY} pores"
        echo "    * Matrix: 800 → ${SCALED_MATRIX} pores"
        echo "    * Hybrid: 800 → ${SCALED_HYBRID} pores"
        
        # Show adjusted DPI
        if (( $(echo "$SCALE_FACTOR < 0.5" | bc -l) )); then
            ADJUSTED_DPI=$(python3 -c "print(int(300 / $SCALE_FACTOR))")
            echo "  - DPI: 300 → ${ADJUSTED_DPI} (increased for small scale detail)"
        elif (( $(echo "$SCALE_FACTOR > 2.0" | bc -l) )); then
            ADJUSTED_DPI=$(python3 -c "print(max(150, int(300 / ($SCALE_FACTOR * 0.5))))")
            echo "  - DPI: 300 → ${ADJUSTED_DPI} (adjusted for large scale)"
        else
            echo "  - DPI: 300 (unchanged)"
        fi
    else
        [[ -n "$N_PORES_INDIVIDUAL" ]] && echo "  - Individual pores: $N_PORES_INDIVIDUAL"
        [[ -n "$N_PORES_COMPARATIVE" ]] && echo "  - Comparative pores: $N_PORES_COMPARATIVE"
        [[ -n "$N_PORES_DENSITY" ]] && echo "  - Density pores: $N_PORES_DENSITY"
        [[ -n "$N_PORES_MATRIX" ]] && echo "  - Matrix pores: $N_PORES_MATRIX"
        [[ -n "$N_PORES_HYBRID" ]] && echo "  - Hybrid pores: $N_PORES_HYBRID"
        [[ -n "$DPI" ]] && echo "  - DPI: $DPI"
    fi
    
    # Show pore sizes (scaled if scale factor is applied)
    if [[ -n "$SCALE_FACTOR" ]]; then
        # Don't show individual pore size overrides when scaling is applied
        [[ -z "$MIN_PORE_RADIUS" && -z "$MAX_PORE_RADIUS" ]] && echo "  - Pore size range: ${SCALED_MIN_PORE} - ${SCALED_MAX_PORE} (scaled)"
    else
        [[ -n "$MIN_PORE_RADIUS" ]] && echo "  - Min pore radius: $MIN_PORE_RADIUS"
        [[ -n "$MAX_PORE_RADIUS" ]] && echo "  - Max pore radius: $MAX_PORE_RADIUS"
    fi
    
    # Show matrix fill parameters (scaled if scale factor is applied)
    if [[ -n "$SCALE_FACTOR" ]]; then
        # Scale matrix fill parameters
        local matrix_x_min=$(echo "$MATRIX_FILL_X_BOUNDS" | cut -d',' -f1)
        local matrix_x_max=$(echo "$MATRIX_FILL_X_BOUNDS" | cut -d',' -f2)
        local matrix_y_min=$(echo "$MATRIX_FILL_Y_BOUNDS" | cut -d',' -f1)
        local matrix_y_max=$(echo "$MATRIX_FILL_Y_BOUNDS" | cut -d',' -f2)
        local matrix_z_min=$(echo "$MATRIX_FILL_Z_BOUNDS" | cut -d',' -f1)
        local matrix_z_max=$(echo "$MATRIX_FILL_Z_BOUNDS" | cut -d',' -f2)

        SCALED_MATRIX_X_MIN=$(echo "$matrix_x_min * $SCALE_FACTOR" | bc -l)
        SCALED_MATRIX_X_MAX=$(echo "$matrix_x_max * $SCALE_FACTOR" | bc -l)
        SCALED_MATRIX_Y_MIN=$(echo "$matrix_y_min * $SCALE_FACTOR" | bc -l)
        SCALED_MATRIX_Y_MAX=$(echo "$matrix_y_max * $SCALE_FACTOR" | bc -l)
        SCALED_MATRIX_Z_MIN=$(echo "$matrix_z_min * $SCALE_FACTOR" | bc -l)
        SCALED_MATRIX_Z_MAX=$(echo "$matrix_z_max * $SCALE_FACTOR" | bc -l)

        SCALED_MATRIX_LENGTH_NORM=$(echo "$MATRIX_LENGTH_NORM * $SCALE_FACTOR" | bc -l)
        SCALED_MATRIX_WIDTH_NORM=$(echo "$MATRIX_WIDTH_NORM * $SCALE_FACTOR" | bc -l)
        SCALED_MATRIX_BASE_PARTICLE_SIZE=$(echo "$MATRIX_BASE_PARTICLE_SIZE * $SCALE_FACTOR" | bc -l)
        SCALED_MATRIX_PARTICLE_SIZE_VARIATION=$(echo "$MATRIX_PARTICLE_SIZE_VARIATION * $SCALE_FACTOR" | bc -l)

        echo ""
        echo "${YELLOW}Matrix Fill Parameters:${NC}"
        echo "  - Matrix X Bounds: ($MATRIX_FILL_X_BOUNDS_ORIGINAL) -> ($MATRIX_FILL_X_BOUNDS)"
        echo "  - Matrix Y Bounds: ($MATRIX_FILL_Y_BOUNDS_ORIGINAL) -> ($MATRIX_FILL_Y_BOUNDS)"
        echo "  - Matrix Z Bounds: ($MATRIX_FILL_Z_BOUNDS_ORIGINAL) -> ($MATRIX_FILL_Z_BOUNDS)"
        echo "  - Matrix Length Norm: $MATRIX_LENGTH_NORM_ORIGINAL -> $MATRIX_LENGTH_NORM"
        echo "  - Matrix Width Norm: $MATRIX_WIDTH_NORM_ORIGINAL -> $MATRIX_WIDTH_NORM"
        echo "  - Matrix Base Particle Size: $MATRIX_BASE_PARTICLE_SIZE_ORIGINAL -> $MATRIX_BASE_PARTICLE_SIZE"
        echo "  - Matrix Particle Size Variation: $MATRIX_PARTICLE_SIZE_VARIATION_ORIGINAL -> $MATRIX_PARTICLE_SIZE_VARIATION"
    else
        echo "  - Matrix X Bounds: ($MATRIX_FILL_X_BOUNDS)"
        echo "  - Matrix Y Bounds: ($MATRIX_FILL_Y_BOUNDS)"
        echo "  - Matrix Z Bounds: ($MATRIX_FILL_Z_BOUNDS)"
        echo "  - Matrix Length Norm: $MATRIX_LENGTH_NORM"
        echo "  - Matrix Width Norm: $MATRIX_WIDTH_NORM"
        echo "  - Matrix Base Particle Size: $MATRIX_BASE_PARTICLE_SIZE"
        echo "  - Matrix Particle Size Variation: $MATRIX_PARTICLE_SIZE_VARIATION"
        echo "  - Matrix Base Particles: $MATRIX_BASE_PARTICLES"
        echo "  - Matrix Particle Alpha: $MATRIX_PARTICLE_ALPHA"
        echo "  - Matrix Batch Size: $MATRIX_BATCH_SIZE"
        echo "  - Matrix Color Intensity Base: $MATRIX_COLOR_INTENSITY_BASE"
        echo "  - Matrix Color Intensity Variation: $MATRIX_COLOR_INTENSITY_VARIATION"
    fi
    
    # Show other parameters (only if not handled by scaling)
    [[ -n "$FIGURE_SIZE" ]] && echo "  - Figure size: $FIGURE_SIZE"
    if [[ -z "$SCALE_FACTOR" ]]; then
        [[ -n "$DPI" ]] && echo "  - DPI: $DPI"
    fi
    [[ -n "$VIEW_ELEVATION" ]] && echo "  - View elevation: ${VIEW_ELEVATION}°"
    [[ -n "$VIEW_AZIMUTH" ]] && echo "  - View azimuth: ${VIEW_AZIMUTH}°"
    [[ -n "$ALPHA_TRANSPARENCY" ]] && echo "  - Alpha transparency: $ALPHA_TRANSPARENCY"
    [[ -n "$OUTPUT_FORMAT" ]] && echo "  - Output format: $OUTPUT_FORMAT"
    
    echo ""
    echo "Use without --dry-run to actually apply these changes."
    exit 0
fi

# Check if we have any overrides to apply
if [[ -z "$CONFIG_TYPE" && -z "$SPECIMEN_DIAMETER" && -z "$BOARD_LENGTH" && -z "$BOARD_WIDTH" && 
      -z "$BOARD_THICKNESS" && -z "$N_PORES_INDIVIDUAL" && -z "$N_PORES_COMPARATIVE" && 
      -z "$N_PORES_DENSITY" && -z "$N_PORES_MATRIX" && -z "$N_PORES_HYBRID" && 
      -z "$MIN_PORE_RADIUS" && -z "$MAX_PORE_RADIUS" && -z "$FIGURE_SIZE" && 
      -z "$DPI" && -z "$VIEW_ELEVATION" && -z "$VIEW_AZIMUTH" && -z "$ALPHA_TRANSPARENCY" && 
      -z "$OUTPUT_FORMAT" ]]; then
    log_error "No configuration overrides specified. Use --help for usage information."
    exit 1
fi

# Check if Python environment is set up
if ! command -v python3 &> /dev/null; then
    log_error "python3 not found. Please ensure Python 3 is installed and in your PATH."
    exit 1
fi

# Check if required files exist
if [[ ! -f "${SCRIPT_DIR}/main.py" ]]; then
    log_error "main.py not found in ${SCRIPT_DIR}"
    exit 1
fi

if [[ ! -f "${SCRIPT_DIR}/app/config.py" ]]; then
    log_error "app/config.py not found in ${SCRIPT_DIR}"
    exit 1
fi

# Display configuration summary
echo -e "${BLUE}Simple Pore Analysis - Configuration Override${NC}"
echo "=============================================="

if [[ -n "$CONFIG_TYPE" ]]; then
    echo "Base configuration: $CONFIG_TYPE"
fi

echo "Applying overrides:"
[[ -n "$SPECIMEN_DIAMETER" ]] && echo "  - Specimen diameter: ${SPECIMEN_DIAMETER}mm"
[[ -n "$SPECIMEN_TOLERANCE" ]] && echo "  - Specimen tolerance: ±${SPECIMEN_TOLERANCE}mm"  
[[ -n "$BOARD_LENGTH" ]] && echo "  - Board length: ${BOARD_LENGTH}mm"
[[ -n "$BOARD_WIDTH" ]] && echo "  - Board width: ${BOARD_WIDTH}mm"
[[ -n "$BOARD_THICKNESS" ]] && echo "  - Board thickness: ${BOARD_THICKNESS}mm"

if [[ -n "$N_PORES_INDIVIDUAL" || -n "$N_PORES_COMPARATIVE" || -n "$N_PORES_DENSITY" || -n "$N_PORES_MATRIX" || -n "$N_PORES_HYBRID" ]]; then
    echo "  - Pore counts:"
    [[ -n "$N_PORES_INDIVIDUAL" ]] && echo "    * Individual: $N_PORES_INDIVIDUAL"
    [[ -n "$N_PORES_COMPARATIVE" ]] && echo "    * Comparative: $N_PORES_COMPARATIVE"
    [[ -n "$N_PORES_DENSITY" ]] && echo "    * Density: $N_PORES_DENSITY"
    [[ -n "$N_PORES_MATRIX" ]] && echo "    * Matrix: $N_PORES_MATRIX"
    [[ -n "$N_PORES_HYBRID" ]] && echo "    * Hybrid: $N_PORES_HYBRID"
fi

[[ -n "$MIN_PORE_RADIUS" ]] && echo "  - Min pore radius: $MIN_PORE_RADIUS"
[[ -n "$MAX_PORE_RADIUS" ]] && echo "  - Max pore radius: $MAX_PORE_RADIUS"
[[ -n "$FIGURE_SIZE" ]] && echo "  - Figure size: $FIGURE_SIZE"
[[ -n "$DPI" ]] && echo "  - DPI: $DPI"
[[ -n "$VIEW_ELEVATION" ]] && echo "  - View elevation: ${VIEW_ELEVATION}°"
[[ -n "$VIEW_AZIMUTH" ]] && echo "  - View azimuth: ${VIEW_AZIMUTH}°"
[[ -n "$ALPHA_TRANSPARENCY" ]] && echo "  - Alpha transparency: $ALPHA_TRANSPARENCY"
[[ -n "$OUTPUT_FORMAT" ]] && echo "  - Output format: $OUTPUT_FORMAT"

echo ""

# Generate the configuration override
generate_config_override

# Backup and modify main file
backup_main_file
modify_main_file

# Execute the Python script
log_info "Executing main application with overridden configuration..."
echo ""

cd "$SCRIPT_DIR"
PYTHON_ARGS=""
if [[ -n "$MICROPORE_COLOR" ]]; then
    PYTHON_ARGS="$PYTHON_ARGS --micropore-color $MICROPORE_COLOR"
fi
if [[ -n "$MESOPORE_COLOR" ]]; then
    PYTHON_ARGS="$PYTHON_ARGS --mesopore-color $MESOPORE_COLOR"
fi
if [[ -n "$MACROPORE_COLOR" ]]; then
    PYTHON_ARGS="$PYTHON_ARGS --macropore-color $MACROPORE_COLOR"
fi
if [[ -n "$MATRIX_FILL_COLOR" ]]; then
    PYTHON_ARGS="$PYTHON_ARGS --matrix-fill-color $MATRIX_FILL_COLOR"
fi
if [[ -n "$MATRIX_ALPHA" ]]; then
    PYTHON_ARGS="$PYTHON_ARGS --matrix-alpha $MATRIX_ALPHA"
fi

if python3 main_temp.py $PYTHON_ARGS; then
    log_success "Application executed successfully with overridden configuration!"
else
    log_error "Application execution failed"
    exit 1
fi

echo ""
log_success "Configuration override completed successfully!"
