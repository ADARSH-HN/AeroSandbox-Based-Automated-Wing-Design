"""
Utility functions for Wing Analyzer application
"""
import os
import pandas as pd
import numpy as np


def normalize(series, invert=False):
    """
    Normalize a pandas Series to [0, 1] range
    
    Args:
        series: pandas Series to normalize
        invert: If True, inverts the series before normalization
    
    Returns:
        Normalized pandas Series
    """
    s = series.copy()
    if invert:
        s = -s
    return (s - s.min()) / (s.max() - s.min())


def ensure_file_removed(filepath):
    """
    Remove a file if it exists
    
    Args:
        filepath: Path to the file to remove
    """
    if os.path.exists(filepath):
        os.remove(filepath)


def save_dataframe_csv(df, filepath, remove_existing=True):
    """
    Save a DataFrame to CSV with optional file removal
    
    Args:
        df: pandas DataFrame to save
        filepath: Path to save the CSV
        remove_existing: If True, removes existing file first
    """
    if remove_existing:
        ensure_file_removed(filepath)
    df.to_csv(filepath, index=False)
    print(f"Saved data to {filepath}")


def get_airfoil_files(folder_path):
    """
    Get all .dat airfoil files from a folder
    
    Args:
        folder_path: Path to folder containing airfoil files
    
    Returns:
        List of airfoil file paths
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Airfoils folder not found: {folder_path}")
    
    files = [f for f in os.listdir(folder_path) if f.endswith(".dat")]
    if not files:
        raise ValueError(f"No .dat files found in {folder_path}")
    
    return files


def calculate_reynolds_number(velocity, chord, kinematic_viscosity=1.81e-5):
    """
    Calculate Reynolds number
    
    Args:
        velocity: Flow velocity (m/s)
        chord: Chord length (m)
        kinematic_viscosity: Kinematic viscosity (m^2/s)
    
    Returns:
        Reynolds number
    """
    return velocity * chord / kinematic_viscosity


def calculate_lift_force(cl, velocity, chord, wingspan, air_density=1.225):
    """
    Calculate lift force in Newtons
    
    Args:
        cl: Lift coefficient
        velocity: Flow velocity (m/s)
        chord: Chord length (m)
        wingspan: Wing span (m)
        air_density: Air density (kg/m^3)
    
    Returns:
        Lift force in Newtons
    """
    wing_area = chord * wingspan
    return cl * 0.5 * air_density * velocity**2 * wing_area


def newtons_to_kgs(force_newtons):
    """Convert Newtons to kilograms"""
    return force_newtons / 9.81


def kgs_to_newtons(mass_kgs):
    """Convert kilograms to Newtons"""
    return mass_kgs * 9.81
