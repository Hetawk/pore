# 3D Pore Distribution Modeling for CSA Cement-Based Insulating Boards

**Experimental and Modeling Assessment of Thermal Properties of Calcium Sulfoaluminate Cement-Based Insulating Boards Utilizing Agriculture Waste Products**

A comprehensive Python-based system for 3D computational modeling and visualization of pore structures in thermal insulating boards made from calcium sulfoaluminate (CSA) cement and agricultural waste materials.

## Research Overview

This project provides advanced 3D visualization and computational modeling capabilities for analyzing pore distribution patterns in experimental thermal insulating boards. The system generates realistic pore structure models based on mercury intrusion porosimetry (MIP) data, enabling detailed analysis of material porosity characteristics that directly influence thermal performance.

## Experimental Materials

### Thermal Insulating Board Compositions

- **T1 Board**: Expanded vermiculite + CSA cement + water
  - Base composition with primary insulating material and binder
- **T2 Board**: Expanded vermiculite + rice husk ash + moso bamboo fiber + CSA cement + water
  - Enhanced composition incorporating agricultural waste materials for improved performance
- **T3 Board**: Expanded vermiculite + rice husk ash (high quantity) + moso bamboo fiber (high quantity) + CSA cement + water
  - Optimized composition with increased agricultural waste content for maximum sustainability

### Testing Methodology

Mercury intrusion porosimetry (MIP) testing was conducted on all board samples to characterize pore size distribution, total porosity, and pore connectivity. The experimental data provides the foundation for computational modeling and 3D visualization of pore structures.

## Computational Features

- **Individual Board Modeling**: Detailed 3D pore structure visualization for each board composition (T1, T2, T3)
- **Comparative Analysis**: Side-by-side visualizations enabling direct comparison of pore characteristics
- **Density-Based Modeling**: Layered density representations showing spatial distribution of porosity
- **Matrix-Filled Modeling**: Dense granular material representations simulating filled pore spaces
- **Hybrid Visualizations**: Combined models showing both discrete pores and matrix material
- **Modular Architecture**: Clean, organized code structure with separate modules for each modeling approach

## Project Structure

```
simple_pore/
├── app/                           # Computational modeling modules
│   ├── __init__.py               # Package initialization
│   ├── data_processor.py         # MIP data loading and processing
│   ├── utils.py                  # Common utilities and geometric framework
│   ├── individual_viz.py         # Individual board pore modeling
│   ├── combined_viz.py           # Comparative board analysis
│   ├── density_viz.py            # Density-based pore distribution modeling
│   ├── sand_dust_viz.py          # Matrix-filled pore space modeling
│   └── combined_pores_sand_viz.py # Hybrid pore-matrix modeling
├── dataset/                      # Mercury intrusion porosimetry data (not tracked in git)
│   └── pore_data.csv            # Experimental pore size distribution data
├── out/                          # Generated models and visualizations (not tracked in git)
│   ├── T1_individual_clean.png   # T1 board pore structure model
│   ├── T2_individual_clean.png   # T2 board pore structure model
│   ├── T3_individual_clean.png   # T3 board pore structure model
│   ├── combined_three_samples_clean.png  # Comparative analysis
│   ├── density_filled_clean.png  # Density-based modeling
│   ├── matrix_filled_clean.png   # Matrix-filled pore modeling
│   ├── T1_pores_matrix_combined.png  # T1 hybrid model
│   ├── T2_pores_matrix_combined.png  # T2 hybrid model
│   ├── T3_pores_matrix_combined.png  # T3 hybrid model
│   └── combined_pores_matrix_filled.png  # Combined hybrid models
├── main.py                       # Main computational modeling script
├── .gitignore                    # Git ignore rules
└── README.md                     # This documentation
```

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/Hetawk/pore.git
cd pore
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required computational libraries:

```bash
pip install pandas numpy matplotlib scipy tqdm
```

## Usage and Computational Modeling

1. Place your mercury intrusion porosimetry data CSV file in the `dataset/` directory as `pore_data.csv`

2. Run the computational modeling script:

```bash
python3 main.py
```

3. Generated 3D models and visualizations will be saved in the `out/` directory

## Mercury Intrusion Porosimetry Data Format

The system processes experimental MIP data with the following structure:

- `diam_T1`, `int_T1`, `cond_T1`: Pore diameter, mercury intrusion volume, and conductivity data for T1 board
- `diam_T2`, `int_T2`, `cond_T2`: Pore diameter, mercury intrusion volume, and conductivity data for T2 board
- `diam_T3`, `int_T3`, `cond_T3`: Pore diameter, mercury intrusion volume, and conductivity data for T3 board

## Computational Modeling Approaches

### 1. Individual Board Pore Structure Modeling

Detailed 3D computational models of pore architecture for each insulating board composition (T1, T2, T3), based on experimental MIP characterization data.

### 2. Comparative Pore Analysis

Simultaneous visualization of all three board compositions enabling direct comparison of pore size distribution, connectivity, and spatial organization.

### 3. Density-Based Pore Distribution Modeling

Layered computational models representing spatial variation in pore density and size distribution throughout the board thickness and cross-sectional area.

### 4. Matrix-Filled Pore Space Modeling

Computational representation of fine granular material matrix completely filling the board volume, simulating dense packing of cement, vermiculite, and agricultural waste particles.

### 5. Hybrid Pore-Matrix Modeling

Advanced computational models combining discrete pore structures with surrounding matrix material, providing comprehensive representation of both macro-porosity and matrix composition.

## Board Specifications and Geometry

- **Dimensions**: 160mm × 160mm × 40mm (square insulating board)
- **Coordinate System**: X-axis (length), Y-axis (width), Z-axis (thickness)
- **Viewing Perspective**: Isometric projection (elevation=30°, azimuth=60°)
- **Aspect Ratio**: 4:4:1 (optimized for thermal insulation applications)

## Experimental Board Compositions

- **T1 Board**: CSA cement matrix with expanded vermiculite aggregate
- **T2 Board**: CSA cement with expanded vermiculite and rice husk ash supplementary cementitious material
- **T3 Board**: CSA cement with vermiculite, rice husk ash, and moso bamboo fiber reinforcement

## Technical Implementation

- **Pore Classification System** (based on IUPAC standards):

  - Micropores: < 2nm (not significant in this application)
  - Mesopores: 2-50nm (important for thermal properties)
  - Macropores: > 50nm (primary focus for mechanical and thermal analysis)
  - Custom size ranges based on MIP data resolution

- **Computational Framework**:

  - 3D modeling engine: Matplotlib with advanced surface rendering
  - Scientific computing: NumPy for mathematical operations and mesh generation
  - Data processing: Pandas for experimental data management
  - Progress monitoring: TQDM for computational progress tracking

- **Geometric Modeling**:
  - Spherical pore approximation based on equivalent diameter from MIP
  - Spatial distribution algorithms incorporating physical constraints
  - Boundary condition enforcement for realistic material representation

## Research Applications

This computational modeling system enables:

- **Thermal Property Prediction**: Correlation between pore structure and thermal conductivity
- **Material Optimization**: Systematic evaluation of composition effects on porosity
- **Quality Control**: Standardized visualization for material characterization
- **Educational Visualization**: Clear representation of microstructural concepts
- **Research Publication**: High-quality figures for scientific documentation

## Future Development Opportunities

- **AI/ML Integration**: Machine learning models for pore distribution prediction
- **Finite Element Integration**: Coupling with thermal simulation software
- **Multi-scale Modeling**: Integration of nano, micro, and macro-scale features
- **Interactive Visualization**: Web-based tools for real-time parameter adjustment
- **Experimental Correlation**: Direct integration with thermal testing data

## Contributing to Research

This project welcomes contributions from researchers working on:

1. **Materials Science**: Enhanced pore characterization methods
2. **Computational Modeling**: Advanced algorithms for microstructure simulation
3. **Thermal Engineering**: Integration with heat transfer analysis
4. **Sustainable Materials**: Agricultural waste utilization in construction materials
5. **Data Visualization**: Improved scientific visualization techniques

### Development Workflow

1. Fork the repository
2. Create a research branch (`git checkout -b research/feature-name`)
3. Implement and test your contributions
4. Update documentation and add test cases
5. Submit a pull request with detailed description

## License and Citation

This project is licensed under the MIT License - see the LICENSE file for details.

### Citation

If you use this computational modeling system in your research, please cite:

```
[Your Name et al.] "Experimental and modeling assessment of the thermal properties of calcium sulfoaluminate cement-based insulating boards utilizing agriculture waste product" [Journal/Conference] (Year)
```

## Acknowledgments

- **Research Focus**: Thermal insulating board characterization and modeling
- **Application Domain**: Sustainable construction materials with agricultural waste
- **Computational Approach**: 3D pore structure modeling from experimental MIP data
- **Scientific Impact**: Enhanced understanding of porosity-thermal property relationships
