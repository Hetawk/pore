#!/usr/bin/env python3
"""
Data loading and processing module for pore visualization.
"""

import pandas as pd
import numpy as np
from io import StringIO


def load_and_clean_data(filename):
    """Load and clean the CSV data, removing invalid rows"""
    print("Loading and cleaning data...")

    # Read every line of the file
    with open(filename, 'r') as f:
        all_lines = f.readlines()

    # Keep only those lines whose first field can be parsed as a float
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
