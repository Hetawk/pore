# 3D Pore Visualization System

A comprehensive Python-based system for creating advanced 3D visualizations of pore distributions in thermal insulating boards. This project provides realistic volumetric representations of pore structures within clean orange prism frames.

## Features

- **Individual Sample Visualizations**: Clean 3D representations of T1, T2, and T3 thermal board samples
- **Combined Visualizations**: Side-by-side comparisons of all three samples
- **Density-Filled Visualizations**: Layered density representations showing material composition
- **Sand/Dust-Filled Visualizations**: Dense granular material representations
- **Combined Pores + Sand**: Hybrid visualizations showing both realistic pores and sand/dust filling
- **Modular Architecture**: Clean, organized code structure with separate modules for each visualization type

## Project Structure

```
simple_pore/
├── app/                           # Visualization modules
│   ├── __init__.py               # Package initialization
│   ├── data_processor.py         # Data loading and processing
│   ├── utils.py                  # Common utilities and frame drawing
│   ├── individual_viz.py         # Individual sample visualizations
│   ├── combined_viz.py           # Combined sample visualizations
│   ├── density_viz.py            # Density-filled visualizations
│   ├── sand_dust_viz.py          # Sand/dust-filled visualizations
│   └── combined_pores_sand_viz.py # Combined pores + sand visualizations
├── dataset/                      # Data files (not tracked in git)
│   └── pore_data.csv            # Pore distribution data
├── out/                          # Output directory (not tracked in git)
│   ├── T1_individual_clean.png
│   ├── T2_individual_clean.png
│   ├── T3_individual_clean.png
│   ├── combined_three_samples_clean.png
│   ├── density_filled_clean.png
│   ├── sand_dust_filled_clean.png
│   ├── T1_pores_sand_combined.png
│   ├── T2_pores_sand_combined.png
│   ├── T3_pores_sand_combined.png
│   └── combined_pores_sand_filled.png
├── main.py                       # Main entry point
├── main_clean.py                 # Clean version of main
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Hetawk/pore.git
cd pore
```

2. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required dependencies:

```bash
pip install pandas numpy matplotlib scipy tqdm
```

## Usage

1. Place your pore data CSV file in the `dataset/` directory as `pore_data.csv`

2. Run the main visualization script:

```bash
python3 main.py
```

3. Check the `out/` directory for generated visualizations

## Data Format

The system expects a CSV file with the following columns:

- `diam_T1`, `int_T1`, `cond_T1`: Diameter, intrusion, and conductivity data for sample T1
- `diam_T2`, `int_T2`, `cond_T2`: Diameter, intrusion, and conductivity data for sample T2
- `diam_T3`, `int_T3`, `cond_T3`: Diameter, intrusion, and conductivity data for sample T3

## Visualization Types

### 1. Individual Sample Visualizations

Clean 3D representations of each thermal board sample (T1, T2, T3) with realistic pore distributions within orange prism frames.

### 2. Combined Three-Sample Visualization

Side-by-side comparison of all three samples for easy comparative analysis.

### 3. Density-Filled Visualization

Layered density representations showing material composition with varying density based on pore characteristics.

### 4. Sand/Dust-Filled Visualization

Dense granular material representation completely filling the orange container from edge to edge.

### 5. Combined Pores + Sand Visualizations

Hybrid visualizations showing both realistic pores and sand/dust filling in the same view.

## Board Specifications

- **Dimensions**: 160mm × 40mm × 40mm (laying horizontally)
- **Viewing Angle**: Isometric left-facing view (elevation=30°, azimuth=60°)
- **Aspect Ratio**: 4:1:1 (length:width:height)

## Sample Descriptions

- **T1**: CSA cement with expanded vermiculite
- **T2**: CSA cement with expanded vermiculite and rice husk ash
- **T3**: CSA cement with vermiculite, rice husk ash and bamboo fiber

## Technical Details

- **Pore Size Categories**:

  - Mesopores: < 100nm
  - Larger mesopores/smaller macropores: 100-2000nm
  - Medium macropores: 2000-50000nm
  - Large macropores: > 50000nm

- **Visualization Engine**: Matplotlib with 3D plotting capabilities
- **Data Processing**: Pandas and NumPy for efficient data handling
- **Progress Tracking**: TQDM for user-friendly progress bars

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for thermal insulating board research and analysis
- Designed for scientific visualization and material characterization
- Optimized for realistic pore distribution representation
