"""
Airfoil Analysis Module
Handles airfoil loading, aerodynamic analysis, and data extraction
"""
import os
import aerosandbox as asb
import aerosandbox.numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import aerosandbox.tools.pretty_plots as p

from config import *
from utils import ensure_file_removed


class AirfoilAnalyzer:
    """Handles aerodynamic analysis of airfoils"""
    
    def __init__(self, airfoils_folder, velocity=DEFAULT_VELOCITY):
        """
        Initialize the airfoil analyzer
        
        Args:
            airfoils_folder: Path to folder containing .dat airfoil files
            velocity: Design velocity in m/s
        """
        self.airfoils_folder = airfoils_folder
        self.velocity = velocity
        self.mach = velocity / MACH_BASE
        
    def analyze_airfoil(self, airfoil_file):
        """
        Analyze a single airfoil across range of angles and Reynolds numbers
        
        Args:
            airfoil_file: Name of the .dat airfoil file
        
        Returns:
            pandas DataFrame with analysis results
        """
        file_path = os.path.join(self.airfoils_folder, airfoil_file)
        airfoil_name = airfoil_file.split(".")[0]
        
        print(f"Analyzing {airfoil_name}...")
        
        # Load and convert airfoil
        af = asb.Airfoil(file_path)
        af = af.to_kulfan_airfoil()
        
        # Setup analysis grid
        alpha = np.linspace(ALPHA_MIN, ALPHA_MAX, 
                           int((ALPHA_MAX - ALPHA_MIN) / ALPHA_STEP) + 1)
        re = np.geomspace(RE_MIN, RE_MAX, RE_POINTS)
        Alpha, Re = np.meshgrid(alpha, re)
        
        # Run NeuralFoil analysis
        res = af.get_aero_from_neuralfoil(
            alpha=Alpha.flatten(),
            Re=Re.flatten(),
            mach=self.mach,
            model_size=NEURALFOIL_MODEL_SIZE
        )
        
        # Create results DataFrame
        df = pd.DataFrame({
            "airfoil_path": af.name,
            "airfoil_name": airfoil_name,
            "alpha_deg": Alpha.flatten(),
            "Re": Re.flatten(),
            "Velocity": self.velocity,
            "CL": res["CL"],
            "CD": res["CD"],
            "CL/CD": res["CL"] / res["CD"],
            "CM": res["CM"],
        })
        
        return df
    
    def analyze_all_airfoils(self, output_file):
        """
        Analyze all airfoil files in the folder
        
        Args:
            output_file: Path to save combined results CSV
        
        Returns:
            pandas DataFrame with all results
        """
        ensure_file_removed(output_file)
        
        airfoil_files = [f for f in os.listdir(self.airfoils_folder) 
                        if f.endswith(".dat")]
        
        if not airfoil_files:
            raise ValueError(f"No .dat files found in {self.airfoils_folder}")
        
        all_results = []
        
        for airfoil_file in airfoil_files:
            try:
                df = self.analyze_airfoil(airfoil_file)
                all_results.append(df)
                
                # Append to CSV incrementally
                df.to_csv(
                    output_file,
                    mode="a",
                    header=not os.path.exists(output_file),
                    index=False,
                )
                print(f"✓ Saved results for {airfoil_file.split('.')[0]}")
                
            except Exception as e:
                print(f"✗ Error analyzing {airfoil_file}: {e}")
                continue
        
        # Return combined DataFrame
        if all_results:
            return pd.concat(all_results, ignore_index=True)
        else:
            raise ValueError("No airfoils were successfully analyzed")


def extract_stall_data(df):
    """
    Extract maximum CL (stall) data for each airfoil and Reynolds number
    
    Args:
        df: DataFrame with airfoil analysis results
    
    Returns:
        DataFrame with stall angle and CL_max
    """
    stall_data = (
        df.loc[df.groupby(["airfoil_name", "Re"])["CL"].idxmax()]
        [["airfoil_name", "Re", "alpha_deg", "CL"]]
        .rename(columns={"alpha_deg": "stall_angle_deg", "CL": "CL_max"})
    )
    return stall_data


def extract_optimum_operating_data(df, alpha_min=OPER_ALPHA_MIN, alpha_max=OPER_ALPHA_MAX):
    """
    Extract optimum operating point (max L/D) in specified angle range
    
    Args:
        df: DataFrame with airfoil analysis results
        alpha_min: Minimum angle for operating range
        alpha_max: Maximum angle for operating range
    
    Returns:
        DataFrame with optimum operating conditions
    """
    df_oper = df[(df["alpha_deg"] >= alpha_min) & (df["alpha_deg"] <= alpha_max)]
    
    optimum_data = (
        df_oper.loc[df_oper.groupby(["airfoil_name", "Re"])["CL/CD"].idxmax()]
        [["airfoil_name", "alpha_deg", "Re", "Velocity", "CL", "CD", "CL/CD"]]
        .rename(columns={
            "alpha_deg": "Optimum_angle",
            "CL": "Optimum_CL",
            "CD": "Optimum_CD",
            "CL/CD": "MAX_CL/CD"
        })
    )
    return optimum_data


def extract_zero_alpha_data(df):
    """
    Extract aerodynamic data at zero angle of attack
    
    Args:
        df: DataFrame with airfoil analysis results
    
    Returns:
        DataFrame with CL and CD at alpha=0
    """
    zero_data = (
        df[df["alpha_deg"] == 0.0]
        [["airfoil_name", "Re", "CL", "CD"]]
        .rename(columns={"CL": "CL_at_0_deg", "CD": "CD_at_0_deg"})
    )
    return zero_data


def create_combined_dataframe(df):
    """
    Create combined DataFrame with all extracted features
    
    Args:
        df: Raw airfoil analysis DataFrame
    
    Returns:
        DataFrame combining stall, optimum, and zero-alpha data
    """
    stall_data = extract_stall_data(df)
    optimum_data = extract_optimum_operating_data(df)
    zero_data = extract_zero_alpha_data(df)
    
    # Merge all data
    final_df = (
        optimum_data.merge(stall_data, on=["airfoil_name", "Re"], how="left")
        .merge(zero_data, on=["airfoil_name", "Re"], how="left")
    )
    
    # Calculate angle difference (stall margin)
    final_df["angle_diff"] = final_df["stall_angle_deg"] - final_df["Optimum_angle"]
    
    return final_df
