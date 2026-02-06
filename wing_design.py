"""
Wing Design and Analysis Module
Handles wing parameter calculations and VLM analysis
"""
import os
import pandas as pd
import aerosandbox as asb

from config import *
from utils import normalize, calculate_lift_force, kgs_to_newtons


class WingDesigner:
    """Handles wing geometry design and parameter calculations"""
    
    def __init__(self, velocity=DEFAULT_VELOCITY, max_wingspan=DEFAULT_MAX_WINGSPAN,
                 aspect_ratios=None):
        """
        Initialize wing designer
        
        Args:
            velocity: Design velocity (m/s)
            max_wingspan: Maximum allowable wingspan (m)
            aspect_ratios: List of aspect ratios to evaluate
        """
        self.velocity = velocity
        self.max_wingspan = max_wingspan
        self.aspect_ratios = aspect_ratios or DEFAULT_ASPECT_RATIOS
    
    def calculate_chord(self, reynolds_number):
        """
        Calculate suitable chord length from Reynolds number
        
        Args:
            reynolds_number: Target Reynolds number
        
        Returns:
            Chord length in meters
        """
        return (reynolds_number * KINEMATIC_VISCOSITY) / (AIR_DENSITY * self.velocity)
    
    def generate_wing_configurations(self, ranked_df):
        """
        Generate all valid wing configurations from ranked airfoils
        
        Args:
            ranked_df: DataFrame with ranked airfoils and their parameters
        
        Returns:
            DataFrame with all valid wing configurations
        """
        rows = []
        
        for _, row in ranked_df.iterrows():
            chord = self.calculate_chord(row["Re"])
            
            for AR in self.aspect_ratios:
                wingspan = AR * chord
                
                # Only include if within wingspan limit
                if wingspan <= self.max_wingspan:
                    rows.append({
                        "airfoil_name": row["airfoil_name"],
                        "Re": row["Re"],
                        "Suitable_chord": chord,
                        "Aspect_Ratio": AR,
                        "Wingspan_m": wingspan,
                        "velocity": self.velocity,
                        "Optimum_angle": row["Optimum_angle"],
                        "Optimum_CL": row["Optimum_CL"],
                        "Optimum_CD": row["Optimum_CD"],
                        "MAX_CL/CD": row["MAX_CL/CD"],
                        "CL_max": row["CL_max"],
                        "CL_at_0_deg": row["CL_at_0_deg"],
                        "stall_angle_deg": row["stall_angle_deg"],
                        "angle_diff": row["angle_diff"],
                        "score": row["score"],
                    })
        
        return pd.DataFrame(rows)


class WingAnalyzer:
    """Performs VLM analysis on wing designs"""
    
    def __init__(self, airfoils_folder):
        """
        Initialize wing analyzer
        
        Args:
            airfoils_folder: Path to folder with airfoil .dat files
        """
        self.airfoils_folder = airfoils_folder
    
    def analyze_wing(self, airfoil_name, chord, wingspan, velocity, alpha):
        """
        Perform VLM analysis on a rectangular wing
        
        Args:
            airfoil_name: Name of airfoil (without .dat extension)
            chord: Chord length (m)
            wingspan: Wing span (m)
            velocity: Flight velocity (m/s)
            alpha: Angle of attack (degrees)
        
        Returns:
            Dictionary with aerodynamic results from VLM
        """
        airfoil_path = os.path.join(self.airfoils_folder, airfoil_name + ".dat")
        
        if not os.path.exists(airfoil_path):
            raise FileNotFoundError(f"Airfoil file not found: {airfoil_path}")
        
        print(f"Analyzing wing with {airfoil_name}...")
        
        # Load airfoil
        wing_airfoil = asb.Airfoil(airfoil_path)
        
        # Create airplane with rectangular wing
        airplane = asb.Airplane(
            name="AEROCLUB_NITTE_RC_PLANE",
            xyz_ref=[0, 2, 0],  # CG location
            wings=[
                asb.Wing(
                    name="Rectangular Wing",
                    symmetric=True,
                    xsecs=[
                        asb.WingXSec(  # Root
                            xyz_le=[0, 0, 0],
                            chord=chord,
                            twist=0,
                            airfoil=wing_airfoil
                        ),
                        asb.WingXSec(  # Tip
                            xyz_le=[0, wingspan / 2, 0],
                            chord=chord,
                            twist=0,
                            airfoil=wing_airfoil
                        )
                    ],
                )
            ],
        )
        
        # Setup VLM
        vlm = asb.VortexLatticeMethod(
            airplane=airplane,
            op_point=asb.OperatingPoint(
                velocity=velocity,
                alpha=alpha,
            ),
        )
        
        # Run analysis
        aero = vlm.run()
        
        return aero
    
    def analyze_all_wings(self, wing_configs_df, progress_callback=None):
        """
        Run VLM analysis on all wing configurations
        
        Args:
            wing_configs_df: DataFrame with wing configurations
            progress_callback: Optional callback function(current, total, message)
        
        Returns:
            DataFrame with VLM results added
        """
        wing_results = []
        total = len(wing_configs_df)
        
        for idx, row in wing_configs_df.iterrows():
            try:
                if progress_callback:
                    progress_callback(idx, total, f"Analyzing wing {idx+1}/{total}: {row['airfoil_name']}")
                
                print(f"Progress: {idx+1}/{total}")
                
                wing_para = self.analyze_wing(
                    airfoil_name=row["airfoil_name"],
                    chord=row["Suitable_chord"],
                    wingspan=row["Wingspan_m"],
                    velocity=row["velocity"],
                    alpha=row["Optimum_angle"],
                )
                
                # Combine row data with VLM results
                result_row = row.to_dict()
                result_row.update(wing_para)
                wing_results.append(result_row)
                
            except Exception as e:
                print(f"✗ Error analyzing wing {row['airfoil_name']}: {e}")
                continue
        
        if progress_callback:
            progress_callback(total, total, "VLM analysis complete!")
        
        return pd.DataFrame(wing_results)


class WingSelector:
    """Selects wings that meet performance requirements"""
    
    def __init__(self, mtow_kgs, velocity=DEFAULT_VELOCITY):
        """
        Initialize wing selector
        
        Args:
            mtow_kgs: Maximum takeoff weight in kilograms
            velocity: Design velocity (m/s)
        """
        self.mtow_newtons = kgs_to_newtons(mtow_kgs)
        self.velocity = velocity
    
    def calculate_lift(self, row):
        """
        Calculate lift force for a wing configuration
        
        Args:
            row: DataFrame row with wing parameters
        
        Returns:
            Lift force in Newtons
        """
        return calculate_lift_force(
            cl=row["CL"],
            velocity=self.velocity,
            chord=row["Suitable_chord"],
            wingspan=row["Wingspan_m"],
            air_density=AIR_DENSITY
        )
    
    def filter_suitable_wings(self, wing_df):
        """
        Filter wings that can lift the required weight
        
        Args:
            wing_df: DataFrame with wing analysis results
        
        Returns:
            DataFrame with suitable wings only
        """
        suitable_wings = []
        
        for _, row in wing_df.iterrows():
            lift = self.calculate_lift(row)
            
            if lift >= self.mtow_newtons:
                suitable_wings.append({
                    "airfoil_name": row["airfoil_name"],
                    "Re": row["Re"],
                    "velocity": row["velocity"],
                    "Aspect_Ratio": row["Aspect_Ratio"],
                    "Suitable_chord": row["Suitable_chord"],
                    "Wingspan_m": row["Wingspan_m"],
                    "Lift_N": lift,
                    "Lift_Kgs": lift / 9.81,
                    "Optimum_angle": row["Optimum_angle"],
                    "Optimum_CL": row["Optimum_CL"],
                    "MAX_CL/CD": row["MAX_CL/CD"],
                })
        
        return pd.DataFrame(suitable_wings)
    
    def rank_suitable_wings(self, suitable_df):
        """
        Rank suitable wings by normalized lift and span
        
        Args:
            suitable_df: DataFrame with suitable wings
        
        Returns:
            Ranked DataFrame
        """
        df = suitable_df.copy()
        
        # Normalize lift and wingspan
        df["Lift_norm"] = normalize(df["Lift_Kgs"])
        df["Span_norm"] = normalize(df["Wingspan_m"])
        
        # Equal weighting for lift and span
        df["final_score"] = 0.5 * df["Lift_norm"] + 0.5 * df["Span_norm"]
        
        # Sort by final score
        ranked = df.sort_values("final_score", ascending=False).reset_index(drop=True)
        
        return ranked
