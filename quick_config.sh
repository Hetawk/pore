#!/bin/bash

# ==============================================================================
# Quick Configuration Presets for Simple Pore Analysis
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

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
    
    "custom")
        echo "🛠️  Running Custom Configuration"
        echo "   Passing all remaining arguments to config_override.sh"
        echo ""
        shift
        exec "$SCRIPT_DIR/config_override.sh" "$@"
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
  custom           Pass custom parameters to config_override.sh

Examples:
  $0 default
  $0 small-specimen
  $0 fast
  $0 publication
  $0 large-board
  $0 tall
  $0 custom --diameter 15 --thickness 8

For full parameter control, use config_override.sh directly:
  ./config_override.sh --help

EOF
        exit 1
        ;;
esac
