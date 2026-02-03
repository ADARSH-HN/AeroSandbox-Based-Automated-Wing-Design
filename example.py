"""
Example: Basic Usage of Wing Analyzer Modules
Demonstrates how to use the modules programmatically
"""
import os
import pandas as pd

from config import *
from airfoil_analysis import AirfoilAnalyzer, create_combined_dataframe
from scoring import AirfoilScorer
from wing_design import WingDesigner, WingAnalyzer, WingSelector
from visualization import AirfoilPlotter, ComparisonPlotter


def main():
    """Example workflow"""
    
    print("="*60)
    print("Wing Analyzer - Example Usage")
    print("="*60)
    
    # ===== STEP 1: Analyze Airfoils =====
    print("\n[1/5] Analyzing airfoils...")
    
    analyzer = AirfoilAnalyzer(
        airfoils_folder=AIRFOILS_FOLDER,
        velocity=13  # m/s
    )
    
    output_file = os.path.join(OUTPUT_FOLDER, "example_output.csv")
    db = analyzer.analyze_all_airfoils(output_file)
    
    print(f"   ✓ Analyzed {db['airfoil_name'].nunique()} airfoils")
    print(f"   ✓ Generated {len(db)} data points")
    
    # ===== STEP 2: Extract Features and Score =====
    print("\n[2/5] Extracting features and scoring...")
    
    combined_df = create_combined_dataframe(db)
    
    scorer = AirfoilScorer(application="payload")
    ranked_df = scorer.rank_airfoils(combined_df)
    
    # Add suitable chord
    ranked_df["Suitable_chord"] = (
        ranked_df["Re"] * KINEMATIC_VISCOSITY
    ) / (AIR_DENSITY * 13)
    
    print(f"   ✓ Top 5 airfoils:")
    top5 = ranked_df.head(5)
    for idx, row in top5.iterrows():
        print(f"      {idx+1}. {row['airfoil_name']} (score: {row['score']:.3f})")
    
    # ===== STEP 3: Generate Wing Configurations =====
    print("\n[3/5] Generating wing configurations...")
    
    designer = WingDesigner(
        velocity=13,
        max_wingspan=1.8,
        aspect_ratios=[3, 4, 5, 6, 7]
    )
    
    wing_configs = designer.generate_wing_configurations(ranked_df)
    print(f"   ✓ Generated {len(wing_configs)} wing configurations")
    
    # ===== STEP 4: Filter Suitable Wings (Skip VLM for speed) =====
    print("\n[4/5] Filtering suitable wings...")
    print("   (Skipping VLM analysis for speed - using approximate aerodynamics)")
    
    # Use the optimum CL from airfoil analysis
    wing_configs["CL"] = wing_configs["Optimum_CL"]
    
    selector = WingSelector(mtow_kgs=8.5, velocity=13)
    suitable_df = selector.filter_suitable_wings(wing_configs)
    
    if len(suitable_df) > 0:
        ranked_suitable = selector.rank_suitable_wings(suitable_df)
        print(f"   ✓ Found {len(ranked_suitable)} suitable wings")
        
        print(f"\n   Top 3 suitable wings:")
        for idx, row in ranked_suitable.head(3).iterrows():
            print(f"      {idx+1}. {row['airfoil_name']} - AR:{row['Aspect_Ratio']}, "
                  f"Span:{row['Wingspan_m']:.2f}m, Lift:{row['Lift_Kgs']:.1f}kg")
        
        # Save results
        output_file = os.path.join(OUTPUT_FOLDER, "example_suitable_wings.csv")
        ranked_suitable.to_csv(output_file, index=False)
        print(f"\n   ✓ Saved results to: {output_file}")
    else:
        print("   ✗ No wings meet MTOW requirement")
    
    # ===== STEP 5: Create Visualizations =====
    print("\n[5/5] Creating visualizations...")
    
    # Get first airfoil for plotting
    first_airfoil = db['airfoil_name'].iloc[0]
    
    plotter = AirfoilPlotter(db)
    fig, ax = plotter.plot_cl_vs_alpha(first_airfoil, show=False)
    
    plot_file = os.path.join(OUTPUT_FOLDER, f"example_plot_{first_airfoil}.png")
    fig.savefig(plot_file, dpi=150, bbox_inches='tight')
    print(f"   ✓ Saved plot to: {plot_file}")
    
    print("\n" + "="*60)
    print("Example completed successfully!")
    print("="*60)


if __name__ == "__main__":
    main()
