"""
Visualization Module
Handles all plotting and chart generation
"""
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from aerosandbox.tools.string_formatting import eng_string
from config import PLOT_DPI


class AirfoilPlotter:
    """Creates plots for airfoil analysis results"""
    
    def __init__(self, db, figsize=(10, 6), dpi=PLOT_DPI):
        """
        Initialize plotter with database
        
        Args:
            db: DataFrame with airfoil analysis results
            figsize: Figure size tuple (width, height)
            dpi: Dots per inch for plot resolution
        """
        self.db = db
        self.figsize = figsize
        self.dpi = dpi
    
    def plot_cl_vs_alpha(self, airfoil_name, show=True):
        """
        Plot CL vs alpha for an airfoil at different Reynolds numbers
        
        Args:
            airfoil_name: Name of airfoil to plot
            show: If True, displays plot immediately
        
        Returns:
            Figure and axes objects
        """
        af_data = self.db[self.db["airfoil_name"] == airfoil_name]
        
        if af_data.empty:
            raise ValueError(f"Airfoil '{airfoil_name}' not found in database")
        
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        for Re_val in sorted(af_data["Re"].unique()):
            d = af_data[af_data["Re"] == Re_val]
            ax.plot(
                d["alpha_deg"],
                d["CL"],
                label=f"Re = {eng_string(Re_val)}",
                linewidth=2
            )
        
        ax.set_title(f"$C_L$ vs $\\alpha$ - {airfoil_name}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Angle of attack $\\alpha$ [deg]", fontsize=12)
        ax.set_ylabel("Lift coefficient $C_L$", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, ax
    
    def plot_cd_vs_alpha(self, airfoil_name, show=True):
        """Plot CD vs alpha for an airfoil"""
        af_data = self.db[self.db["airfoil_name"] == airfoil_name]
        
        if af_data.empty:
            raise ValueError(f"Airfoil '{airfoil_name}' not found in database")
        
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        for Re_val in sorted(af_data["Re"].unique()):
            d = af_data[af_data["Re"] == Re_val]
            ax.plot(
                d["alpha_deg"],
                d["CD"],
                label=f"Re = {eng_string(Re_val)}",
                linewidth=2
            )
        
        ax.set_title(f"$C_D$ vs $\\alpha$ - {airfoil_name}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Angle of attack $\\alpha$ [deg]", fontsize=12)
        ax.set_ylabel("Drag coefficient $C_D$", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, ax
    
    def plot_cl_vs_cd(self, airfoil_name, show=True):
        """Plot CL vs CD (drag polar) for an airfoil"""
        af_data = self.db[self.db["airfoil_name"] == airfoil_name]
        
        if af_data.empty:
            raise ValueError(f"Airfoil '{airfoil_name}' not found in database")
        
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        for Re_val in sorted(af_data["Re"].unique()):
            d = af_data[af_data["Re"] == Re_val]
            ax.plot(
                d["CD"],
                d["CL"],
                label=f"Re = {eng_string(Re_val)}",
                linewidth=2
            )
        
        ax.set_title(f"$C_L$ vs $C_D$ (Drag Polar) - {airfoil_name}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Drag coefficient $C_D$", fontsize=12)
        ax.set_ylabel("Lift coefficient $C_L$", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, ax
    
    def plot_ld_vs_alpha(self, airfoil_name, show=True):
        """Plot L/D ratio vs alpha for an airfoil"""
        af_data = self.db[self.db["airfoil_name"] == airfoil_name]
        
        if af_data.empty:
            raise ValueError(f"Airfoil '{airfoil_name}' not found in database")
        
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        for Re_val in sorted(af_data["Re"].unique()):
            d = af_data[af_data["Re"] == Re_val]
            ax.plot(
                d["alpha_deg"],
                d["CL/CD"],
                label=f"Re = {eng_string(Re_val)}",
                linewidth=2
            )
        
        ax.set_title(f"$C_L/C_D$ vs $\\alpha$ - {airfoil_name}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Angle of attack $\\alpha$ [deg]", fontsize=12)
        ax.set_ylabel("Lift-to-drag ratio $C_L/C_D$", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, ax
    
    def plot_cm_vs_alpha(self, airfoil_name, show=True):
        """Plot moment coefficient vs alpha for an airfoil"""
        af_data = self.db[self.db["airfoil_name"] == airfoil_name]
        
        if af_data.empty:
            raise ValueError(f"Airfoil '{airfoil_name}' not found in database")
        
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        for Re_val in sorted(af_data["Re"].unique()):
            d = af_data[af_data["Re"] == Re_val]
            ax.plot(
                d["alpha_deg"],
                d["CM"],
                label=f"Re = {eng_string(Re_val)}",
                linewidth=2
            )
        
        ax.set_title(f"$C_M$ vs $\\alpha$ - {airfoil_name}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Angle of attack $\\alpha$ [deg]", fontsize=12)
        ax.set_ylabel("Moment coefficient $C_M$", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, ax
    
    def plot_all_for_airfoil(self, airfoil_name):
        """Create all plots for a single airfoil"""
        self.plot_cl_vs_alpha(airfoil_name, show=False)
        self.plot_cd_vs_alpha(airfoil_name, show=False)
        self.plot_cl_vs_cd(airfoil_name, show=False)
        self.plot_ld_vs_alpha(airfoil_name, show=False)
        self.plot_cm_vs_alpha(airfoil_name, show=True)


class ComparisonPlotter:
    """Creates comparison plots for multiple airfoils"""
    
    def __init__(self, db, figsize=(10, 6), dpi=PLOT_DPI):
        """
        Initialize comparison plotter
        
        Args:
            db: DataFrame with airfoil analysis results
            figsize: Figure size tuple
            dpi: Plot resolution
        """
        self.db = db
        self.figsize = figsize
        self.dpi = dpi
    
    def plot_cl_comparison(self, airfoil_names, re_target, show=True):
        """
        Compare CL vs alpha for multiple airfoils at specific Re
        
        Args:
            airfoil_names: List of airfoil names to compare
            re_target: Target Reynolds number
            show: If True, displays plot immediately
        
        Returns:
            Figure and axes objects
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        for af in airfoil_names:
            d = self.db[
                (self.db["airfoil_name"] == af) & 
                (np.isclose(self.db["Re"], re_target, rtol=1e-4))
            ]
            if not d.empty:
                ax.plot(d["alpha_deg"], d["CL"], label=af, linewidth=2, marker='o', markersize=3)
        
        ax.set_title(f"$C_L$ vs $\\alpha$ Comparison at Re={eng_string(re_target)}", 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel("Angle of attack $\\alpha$ [deg]", fontsize=12)
        ax.set_ylabel("Lift coefficient $C_L$", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, ax
    
    def plot_cd_comparison(self, airfoil_names, re_target, show=True):
        """Compare CD vs alpha for multiple airfoils"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        for af in airfoil_names:
            d = self.db[
                (self.db["airfoil_name"] == af) & 
                (np.isclose(self.db["Re"], re_target, rtol=1e-4))
            ]
            if not d.empty:
                ax.plot(d["alpha_deg"], d["CD"], label=af, linewidth=2, marker='o', markersize=3)
        
        ax.set_title(f"$C_D$ vs $\\alpha$ Comparison at Re={eng_string(re_target)}", 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel("Angle of attack $\\alpha$ [deg]", fontsize=12)
        ax.set_ylabel("Drag coefficient $C_D$", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, ax
    
    def plot_polar_comparison(self, airfoil_names, re_target, show=True):
        """Compare drag polars for multiple airfoils"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        for af in airfoil_names:
            d = self.db[
                (self.db["airfoil_name"] == af) & 
                (np.isclose(self.db["Re"], re_target, rtol=1e-4))
            ]
            if not d.empty:
                ax.plot(d["CD"], d["CL"], label=af, linewidth=2, marker='o', markersize=3)
        
        ax.set_title(f"Drag Polar Comparison at Re={eng_string(re_target)}", 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel("Drag coefficient $C_D$", fontsize=12)
        ax.set_ylabel("Lift coefficient $C_L$", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, ax
    
    def plot_ld_comparison(self, airfoil_names, re_target, show=True):
        """Compare L/D ratio for multiple airfoils"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        for af in airfoil_names:
            d = self.db[
                (self.db["airfoil_name"] == af) & 
                (np.isclose(self.db["Re"], re_target, rtol=1e-4))
            ]
            if not d.empty:
                ax.plot(d["alpha_deg"], d["CL/CD"], label=af, linewidth=2, marker='o', markersize=3)
        
        ax.set_title(f"$C_L/C_D$ Comparison at Re={eng_string(re_target)}", 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel("Angle of attack $\\alpha$ [deg]", fontsize=12)
        ax.set_ylabel("Lift-to-drag ratio $C_L/C_D$", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, ax
    
    def plot_cm_comparison(self, airfoil_names, re_target, show=True):
        """Compare moment coefficient for multiple airfoils"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        for af in airfoil_names:
            d = self.db[
                (self.db["airfoil_name"] == af) & 
                (np.isclose(self.db["Re"], re_target, rtol=1e-4))
            ]
            if not d.empty:
                ax.plot(d["alpha_deg"], d["CM"], label=af, linewidth=2, marker='o', markersize=3)
        
        ax.set_title(f"$C_M$ Comparison at Re={eng_string(re_target)}", 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel("Angle of attack $\\alpha$ [deg]", fontsize=12)
        ax.set_ylabel("Moment coefficient $C_M$", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if show:
            plt.show()
        
        return fig, ax


def plot_airfoil_shape(airfoil_path, show=True):
    """
    Plot the geometry/shape of an airfoil
    
    Args:
        airfoil_path: Path to the .dat airfoil file
        show: If True, displays plot immediately
    
    Returns:
        Figure and axes objects
    """
    import aerosandbox as asb
    
    airfoil = asb.Airfoil(airfoil_path)
    airfoil_name = os.path.basename(airfoil_path).split('.')[0]
    
    fig, ax = plt.subplots(figsize=(12, 4), dpi=PLOT_DPI)
    
    # Plot airfoil coordinates
    ax.plot(airfoil.coordinates[:, 0], airfoil.coordinates[:, 1], 
           'b-', linewidth=2, label='Airfoil Shape')
    ax.fill(airfoil.coordinates[:, 0], airfoil.coordinates[:, 1], 
           alpha=0.2, color='steelblue')
    
    ax.set_xlabel('x/c', fontsize=12)
    ax.set_ylabel('y/c', fontsize=12)
    ax.set_title(f'Airfoil Geometry - {airfoil_name}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.legend()
    plt.tight_layout()
    
    if show:
        plt.show()
    
    return fig, ax


def create_ranking_barplot(ranked_df, top_n=10, show=True):
    """
    Create bar plot of top ranked airfoils
    
    Args:
        ranked_df: DataFrame with ranked airfoils
        top_n: Number of top airfoils to show
        show: If True, displays plot immediately
    
    Returns:
        Figure and axes objects
    """
    top_airfoils = ranked_df.head(top_n)
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=PLOT_DPI)
    
    bars = ax.barh(
        range(len(top_airfoils)),
        top_airfoils["score"],
        color='steelblue'
    )
    
    ax.set_yticks(range(len(top_airfoils)))
    ax.set_yticklabels(top_airfoils["airfoil_name"])
    ax.set_xlabel("Score", fontsize=12)
    ax.set_ylabel("Airfoil", fontsize=12)
    ax.set_title(f"Top {top_n} Ranked Airfoils", fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    ax.invert_yaxis()
    
    # Add score labels on bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
               f'{width:.3f}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    
    if show:
        plt.show()
    
    return fig, ax
