#!/bin/bash

# ==============================================================================
# Quick Configuration Presets for Simple Pore Analysis
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Script to quickly set configuration options for the pore visualization system
# Usage: ./quick_config.sh [option]
# Options: default, small, advanced, dimension

# Directory setup
CONFIG_DIR="$(dirname "$0")/app/override"
mkdir -p "$CONFIG_DIR"

# Reset any previous overrides
rm -f "$CONFIG_DIR"/*.py

# Create __init__.py to make override directory importable
touch "$CONFIG_DIR/__init__.py"

case "$1" in
    "default")
        echo "📊 Running Default Configuration (config.py values)"
        echo "   - Board: 160×160×40 mm"
        echo "   - Individual pores: 600"
        echo "   - Comparative pores: 400"
        echo "   - Density pores: 500"
        echo "   - Matrix pores: 800"
        echo "   - Hybrid pores: 800"
        echo "   - Pore radius: 0.03-0.08"
        echo "   - DPI: 300, Figure: 12×8"
        echo ""
        exec "$SCRIPT_DIR/config_override.sh" \
            --length 160 \
            --width 160 \
            --thickness 40 \
            --pores-individual 600 \
            --pores-comparative 400 \
            --pores-density 500 \
            --pores-matrix 800 \
            --pores-hybrid 800 \
            --min-pore-radius 0.03 \
            --max-pore-radius 0.08 \
            --dpi 300 \
            --figure-size "12,8" \
            --elevation 30 \
            --azimuth 60 \
            --alpha 0.9
        ;;

    "small-specimen")
        echo "🔬 Running Small Specimen Analysis (10±1mm diameter)"
        echo "   - Diameter: 10mm"
        echo "   - Tolerance: ±1mm"
        echo "   - Thickness: 10mm (config.py small_specimen default)"
        echo "   - Proportionally scaled pore counts"
        echo "   - Higher DPI for detail: 600"
        echo ""
        exec "$SCRIPT_DIR/config_override.sh" \
            --diameter 10 \
            --tolerance 1 \
            --thickness 10 \
            --pores-all 60 \
            --min-pore-radius 0.01 \
            --max-pore-radius 0.4 \
            --dpi 600 \
            --figure-size "10,8" \
            --elevation 25 \
            --azimuth 45 \
            --alpha 0.9
        ;;
    
    "fast")
        echo "⚡ Running Fast Analysis (Reduced Quality)"
        echo "   - Low pore counts for speed"
        echo "   - Lower resolution"
        echo ""
        exec "$SCRIPT_DIR/config_override.sh" \
            --pores-all 150 \
            --dpi 150
        ;;
    
    "publication")
        echo "📄 Running Publication Quality Analysis"
        echo "   - High DPI (600)"
        echo "   - Large figure size"
        echo "   - PDF output"
        echo ""
        exec "$SCRIPT_DIR/config_override.sh" \
            --dpi 600 \
            --figure-size "16,12" \
            --format pdf \
            --alpha 0.95
        ;;
    
    "large-board")
        echo "📏 Running Large Board Analysis (300×300×80mm)"
        echo "   - Length: 300mm"
        echo "   - Width: 300mm"
        echo "   - Thickness: 80mm"
        echo "   - Optimized pore counts"
        echo ""
        exec "$SCRIPT_DIR/config_override.sh" \
            --length 300 \
            --width 300 \
            --thickness 80 \
            --pores-all 400
        ;;
    
    "tall")
        echo "📈 Running Tall Board Analysis (Increased Height/Thickness)"
        echo "   - Board: 160×160×80 mm (double thickness)"
        echo "   - Individual pores: 600"
        echo "   - Comparative pores: 400"
        echo "   - Density pores: 500"
        echo "   - Matrix pores: 800"
        echo "   - Hybrid pores: 800"
        echo "   - Matrix Z-bounds expanded to match taller profile"
        echo "   - DPI: 300, Figure: 10×12 (portrait for tall view)"
        echo "   - Modified camera angles for better height visibility"
        echo ""
        exec "$SCRIPT_DIR/config_override.sh" \
            --length 160 \
            --width 160 \
            --thickness 80 \
            --pores-individual 600 \
            --pores-comparative 400 \
            --pores-density 500 \
            --pores-matrix 800 \
            --pores-hybrid 800 \
            --min-pore-radius 0.03 \
            --max-pore-radius 0.08 \
            --matrix-z-bounds "-1.0,1.0" \
            --dpi 300 \
            --figure-size "10,12" \
            --elevation 20 \
            --azimuth 45 \
            --alpha 0.85
        ;;
    
    "color")
        echo "🌈 Running Colored Pore Size Visualization (Tall Board + Color Categories)"
        echo "   - Board: 160×160×80 mm (double thickness)"
        echo "   - Pore size categories: Micropores, Mesopores, Macropores"
        echo "   - Colors: Micropores=#FF1493 (pink), Mesopores=#FFFF00 (yellow), Macropores=#00FFFF (cyan)"
        echo "   - Matrix fill: #cccccc (very light gray, alpha=0.15)"
        echo "   - Pores: vivid, fully opaque with smooth surfaces"
        echo ""
        exec "$SCRIPT_DIR/config_override.sh" \
            --length 160 \
            --width 160 \
            --thickness 80 \
            --pores-individual 600 \
            --pores-comparative 400 \
            --pores-density 500 \
            --pores-matrix 800 \
            --pores-hybrid 800 \
            --min-pore-radius 0.03 \
            --max-pore-radius 0.08 \
            --matrix-z-bounds "-1.0,1.0" \
            --dpi 300 \
            --figure-size "10,12" \
            --elevation 20 \
            --azimuth 45 \
            --micropore-color "#FF1493" \
            --mesopore-color "#FFFF00" \
            --macropore-color "#00FFFF" \
            --matrix-alpha 0.15 \
            --alpha 1.0
        ;;

    "color2")
        echo "🎨 Running Alternative Color Scheme (Enhanced Contrast)"
        echo "   - Board: 160×160×80 mm (double thickness)"
        echo "   - Pore size categories: Micropores, Mesopores, Macropores"
        echo "   - Colors: Micropores=#FF0000 (red), Mesopores=#00FF00 (green), Macropores=#0000FF (blue)"
        echo "   - Matrix fill: #333333 (dark gray, alpha=0.1)"
        echo "   - Pores: fully opaque, high-contrast RGB scheme"
        echo ""
        exec "$SCRIPT_DIR/config_override.sh" \
            --length 160 \
            --width 160 \
            --thickness 80 \
            --pores-individual 600 \
            --pores-comparative 400 \
            --pores-density 500 \
            --pores-matrix 800 \
            --pores-hybrid 800 \
            --min-pore-radius 0.03 \
            --max-pore-radius 0.08 \
            --matrix-z-bounds "-1.0,1.0" \
            --dpi 300 \
            --figure-size "10,12" \
            --elevation 20 \
            --azimuth 45 \
            --micropore-color "#FF0000" \
            --mesopore-color "#00FF00" \
            --macropore-color "#0000FF" \
            --matrix-fill-color "#333333" \
            --matrix-alpha 0.1 \
            --alpha 1.0 \
            --advanced-analysis false
        ;;
        
    "advanced")
        echo "📊 Running Advanced Pore Analysis Visualization"
        echo "   - Board: 160×160×80 mm (double thickness)"
        echo "   - Statistical analysis of pore distribution"
        echo "   - Volume histogram and sphericity analysis"
        echo "   - Categorical coloring with volume colorbar"
        echo ""
        exec "$SCRIPT_DIR/config_override.sh" \
            --length 160 \
            --width 160 \
            --thickness 80 \
            --min-pore-radius 0.03 \
            --max-pore-radius 0.08 \
            --matrix-z-bounds "-1.0,1.0" \
            --dpi 300 \
            --figure-size "10,12" \
            --elevation 20 \
            --azimuth 45 \
            --micropore-color "#FF0000" \
            --mesopore-color "#00FF00" \
            --macropore-color "#0000FF" \
            --matrix-fill-color "#333333" \
            --matrix-alpha 0.1 \
            --alpha 1.0 \
            --advanced-analysis true \
            --advanced-colormap "jet" \
            --advanced-tick-count 8 \
            --advanced-bins 30
        ;;

    "custom")
        echo "🛠️  Running Custom Configuration"
        echo "   Passing all remaining arguments to config_override.sh"
        echo ""
        shift
        exec "$SCRIPT_DIR/config_override.sh" "$@"
        ;;
    
    "dimension")
        echo -e "📏 Running Custom Dimension Analysis (40×40×160mm)\n   - Length: 40mm\n   - Width: 40mm\n   - Thickness: 160mm\n   - Adjusted pore counts and settings"
        
        # Make the wrapper script executable
        chmod +x "$SCRIPT_DIR/run_dimension_override.py"
        
        # Execute the special wrapper script that ensures dimension override
        exec "$SCRIPT_DIR/run_dimension_override.py"
    ;;
    
    "dim100")
        echo -e "📏 Running Cubic Dimension Analysis (100×100×100mm)\n   - Length: 100mm\n   - Width: 100mm\n   - Thickness: 100mm\n   - Adjusted pore counts and settings for cubic shape"
        
        # Make the wrapper script executable
        chmod +x "$SCRIPT_DIR/run_dimension_100.py"
        
        # Execute the special wrapper script for 100×100×100mm dimensions
        exec "$SCRIPT_DIR/run_dimension_100.py"
    ;;
    
    "dim100color0")
        echo -e "📏 Running Cubic Dimension Analysis (100×100×100mm) with Single-Color Pores\n   - Length: 100mm\n   - Width: 100mm\n   - Thickness: 100mm\n   - Single uniform color per sample (no legend)"
        
        # Make the wrapper script executable
        chmod +x "$SCRIPT_DIR/run_dimension_100_color0.py"
        
        # Execute the special wrapper script for 100×100×100mm dimensions with single-color pores
        exec "$SCRIPT_DIR/run_dimension_100_color0.py"
    ;;
    
    *)
        cat << EOF
🔧 Simple Pore Analysis - Quick Presets

Usage: $0 <preset> [additional_options]

Available Presets:
  default          Default configuration values from config.py
  small-specimen   Small specimens (10±1mm diameter, config.py values)
  fast             Fast analysis with reduced quality
  publication      High quality for publications
  large-board      Large board analysis (300×300×80mm)
  tall             Tall board analysis (increased thickness)
  color            Tall board with colored pore categories (pink/yellow/cyan)
  color2           Alternative color scheme with RGB colors (red/green/blue)
  advanced         Advanced statistical analysis of pore distribution
  custom           Pass custom parameters to config_override.sh
  dimension        Custom dimensions (40×40×160mm)
  dim100           Cubic dimensions (100×100×100mm)
  dim100color0     Cubic dimensions with single-color pores (no size-based legend)

Examples:
  $0 default
  $0 small-specimen
  $0 fast
  $0 publication
  $0 large-board
  $0 tall
  $0 color
  $0 color2
  $0 advanced
  $0 custom --diameter 15 --thickness 8
  $0 dimension
  $0 dim100
  $0 dim100color0

EOF
        exit 1
        ;;
esac
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
        self.advanced_colorbar_formatter = '%.2e'  # Scientific notation for colorbar values
    
    print("\nSimple Pore Analysis - Configuration Override")
    print("==============================================")
    print("Applying overrides:")
    print("  - Board length: 40mm")
    print("  - Board width: 40mm")
    print("  - Board thickness: 160mm")
    print("  - Pore counts:")
    print("    * Individual: 100")
    print("    * Comparative: 50")
    print("    * Density: 75")
    print("    * Matrix: 200")
    print("    * Hybrid: 200")
    print("  - Min pore radius: 0.005")
    print("  - Max pore radius: 0.02")
    print("  - Figure size: 8,10")
    print("  - DPI: 150")
    print("  - View elevation: 30°")
    print("  - View azimuth: 60°")
    print("  - Alpha transparency: 0.9")
    print("  - Output format: png")
    if hasattr(self, 'enable_advanced_analysis') and self.enable_advanced_analysis:
        print("  - Advanced analysis: Enabled with vertical board optimizations")
    print("\n")

# Replace the default config loader with our custom one
MaterialConfig._load_default_config = custom_dimension_config

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

# Make sure we force a reload of the configuration with our monkey patched method
CONFIG = MaterialConfig("default")
    
# Make advanced analysis module aware of dimension changes
try:
    # Try to import and patch the advanced_analysis module if it exists
    from app import advanced_analysis
    
    # Store original plotting function
    if hasattr(advanced_analysis, 'create_advanced_analysis'):
        original_create_advanced = advanced_analysis.create_advanced_analysis
        
        # Create wrapper function that adjusts figure for vertical board
        def dimension_aware_advanced_analysis(*args, **kwargs):
            import matplotlib.pyplot as plt
            # Adjust figure for vertical board
            if CONFIG.board_thickness_mm > CONFIG.board_length_mm:
                plt.figure(figsize=(10, 12))  # Portrait orientation for vertical board
            return original_create_advanced(*args, **kwargs)
            
        # Replace the function with our dimension-aware version
        advanced_analysis.create_advanced_analysis = dimension_aware_advanced_analysis
except (ImportError, AttributeError):
    # Module doesn't exist or doesn't have the expected function, just continue
    pass

print("[SUCCESS] Configuration override completed successfully!")
EOL

        # Create a second file that will ensure the override is loaded at import time
        cat > "$CONFIG_DIR/__init__.py" << 'EOL'
# This makes sure overrides are applied when the app.override package is imported
from . import override_config
EOL

        # Create a marker file to help debugging
        cat > "$CONFIG_DIR/DIMENSION_OVERRIDE_ACTIVE" << 'EOL'
This file indicates that the dimension override is active.
If you're seeing the default dimensions, check that app/override is being imported.
EOL

        # Actually run the application with the dimension configuration and advanced analysis
        echo "Running application with dimension configuration..."
        exec "$SCRIPT_DIR/config_override.sh" \
            --length 40 \
            --width 40 \
            --thickness 160 \
            --pores-individual 200 \
            --pores-comparative 100 \
            --pores-density 150 \
            --pores-matrix 300 \
            --pores-hybrid 300 \
            --min-pore-radius 0.01 \
            --max-pore-radius 0.05 \
            --matrix-z-bounds "-1.95,1.95" \
            --matrix-x-bounds "-0.45,0.45" \
            --matrix-y-bounds "-0.45,0.45" \
            --dpi 300 \
            --figure-size "10,12" \
            --elevation 20 \
            --azimuth 30 \
            --alpha 0.9 \
            --advanced-analysis true \
            --advanced-colormap "jet" \
            --advanced-tick-count 10 \
            --advanced-bins 30
    ;;
    
    *)
        cat << EOF
🔧 Simple Pore Analysis - Quick Presets

Usage: $0 <preset> [additional_options]

Available Presets:
  default          Default configuration values from config.py
  small-specimen   Small specimens (10±1mm diameter, config.py values)
  fast             Fast analysis with reduced quality
  publication      High quality for publications
  large-board      Large board analysis (300×300×80mm)
  tall             Tall board analysis (increased thickness)
  color            Tall board with colored pore categories (pink/yellow/cyan)
  color2           Alternative color scheme with RGB colors (red/green/blue)
  advanced         Advanced statistical analysis of pore distribution
  custom           Pass custom parameters to config_override.sh
  dimension        Custom dimensions (40×40×160mm)
  dim100           Cubic dimensions (100×100×100mm)

Examples:
  $0 default
  $0 small-specimen
  $0 fast
  $0 publication
  $0 large-board
  $0 tall
  $0 color
  $0 color2
  $0 advanced
  $0 custom --diameter 15 --thickness 8
  $0 dimension
  $0 dim100

EOF
        exit 1
        ;;
esac
