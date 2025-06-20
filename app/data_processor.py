#!/usr/bin/env python3
"""
Mercury intrusion porosimetry (MIP) data processing module for 
CSA cement-based thermal insulating board characterization.

This module handles experimental data loading, cleaning, and preparation
for 3D pore structure modeling and computational analysis.
"""

import pandas as pd
import numpy as np
from io import StringIO


def load_and_clean_data(filename):
    """
    Load and process experimental mercury intrusion porosimetry data.

    Reads CSV data containing pore diameter, intrusion volume, and conductivity
    measurements for thermal insulating board samples. Performs data validation
    and cleaning to ensure numerical consistency for computational modeling.

    Parameters:
    -----------
    filename : str
        Path to CSV file containing experimental MIP data

    Returns:
    --------
    pandas.DataFrame
        Cleaned experimental data with validated numerical values
        for pore diameter, intrusion volume, and thermal conductivity
    """
    print("Loading and cleaning experimental MIP data...")

    # Read experimental data file line by line
    with open(filename, 'r') as f:
        all_lines = f.readlines()

    # Filter data rows to ensure valid numerical entries for analysis
    clean_lines = []
    for line in all_lines:
        stripped = line.strip()
        if stripped == "":
            continue
        first_token = stripped.split(',')[0]
        try:
            _ = float(first_token)
            clean_lines.append(line)
        except ValueError:
            continue

    # Join clean lines and parse with pandas
    csv_data = "".join(clean_lines)
    df = pd.read_csv(StringIO(csv_data), header=None)

    # Assign column names
    df.columns = [
        "diam_T1", "int_T1", "cond_T1",
        "diam_T2", "int_T2", "cond_T2",
        "diam_T3", "int_T3", "cond_T3"
    ]

    # Force everything to numeric and drop any leftover NaNs
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=["diam_T1", "int_T1", "diam_T2",
                   "int_T2", "diam_T3", "int_T3"])

    return df


def sort_by_diameter(d_arr, v_arr):
    """Sort arrays by diameter values in ascending order"""
    idx = np.argsort(d_arr)
    return d_arr[idx], v_arr[idx]
