"""
Wing Analyzer - Streamlit UI Application
Main interface for airfoil analysis and wing design
"""
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

from config import *
from airfoil_analysis import AirfoilAnalyzer, create_combined_dataframe
from scoring import AirfoilScorer
from wing_design import WingDesigner, WingAnalyzer, WingSelector
from visualization import AirfoilPlotter, ComparisonPlotter, create_ranking_barplot, plot_airfoil_shape
from utils import save_dataframe_csv

# Page config
st.set_page_config(
    page_title="Wing Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'db' not in st.session_state:
    st.session_state.db = None
if 'ranked_df' not in st.session_state:
    st.session_state.ranked_df = None
if 'suitable_wings_df' not in st.session_state:
    st.session_state.suitable_wings_df = None


def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header"> Wing Analyzer </h1>', unsafe_allow_html=True)
    st.markdown("**Aerodynamic Analysis & Wing Design Tool for RC Aircraft**")
    st.markdown("---")
    
    # Sidebar - Parameters
    st.sidebar.title("Configuration")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Home", 
        "Airfoil Analysis", 
        "Ranking & Selection",
        "Wing Design",
        "Visualizations"
    ])
    
    # ===== TAB 1: HOME =====
    with tab1:
        st.header("Welcome to Wing Analyzer Pro")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Overview")
            st.write("""
            This application helps you:
            - Analyze multiple airfoils using NeuralFoil
            - Score and rank airfoils based on mission requirements
            - Design optimal wing configurations
            - Visualize aerodynamic characteristics
            - Select wings that meet weight requirements
            """)
            
            st.subheader("Quick Start")
            st.write("""
            1. Configure parameters in the sidebar
            2. Go to **Airfoil Analysis** to analyze airfoils
            3. View **Ranking & Selection** for scored results
            4. Design wings in **Wing Design** tab
            5. Explore **Visualizations** for plots
            """)
        
        with col2:
            st.subheader("📂 Input Configuration")
            
            # File paths
            airfoils_folder = st.text_input(
                "Airfoils Folder Path", 
                value=AIRFOILS_FOLDER,
                help="Path to folder containing .dat airfoil files"
            )
            
            # Show airfoil shape preview
            if os.path.exists(airfoils_folder):
                dat_files = [f for f in os.listdir(airfoils_folder) if f.endswith('.dat')]
                st.success(f"✓ Found {len(dat_files)} airfoil files")
                if dat_files:
                    preview_airfoil = st.selectbox(
                        "Select airfoil to preview",
                        dat_files,
                        key="preview_airfoil"
                    )
                    try:
                        airfoil_path = os.path.join(airfoils_folder, preview_airfoil)
                        fig, ax = plot_airfoil_shape(airfoil_path, show=False)
                        st.pyplot(fig)
                        plt.close()
                    except Exception as e:
                        st.error(f"Error plotting airfoil: {e}")
            
            # Design parameters
            st.subheader("Design Parameters")
            mtow = st.number_input("MTOW (kg)", value=float(DEFAULT_MTOW_KGS), min_value=0.1, step=0.1)
            max_span = st.number_input("Max Wingspan (m)", value=float(DEFAULT_MAX_WINGSPAN), min_value=0.1, step=0.1)
            velocity = st.number_input("Design Velocity (m/s)", value=float(DEFAULT_VELOCITY), min_value=1.0, step=0.5)
            
            # Application type
            application = st.selectbox(
                "Mission Type",
                options=list(APPLICATION_WEIGHTS.keys()),
                index=0,
                help="Select the primary mission profile"
            )
            
            # Store in session state
            st.session_state.airfoils_folder = airfoils_folder
            st.session_state.mtow = mtow
            st.session_state.max_span = max_span
            st.session_state.velocity = velocity
            st.session_state.application = application
    
    # ===== TAB 2: AIRFOIL ANALYSIS =====
    with tab2:
        st.header("Airfoil Analysis")
        
        st.write("Analyze airfoils using NeuralFoil across a range of angles of attack and Reynolds numbers.")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Alpha Range", f"{ALPHA_MIN}° to {ALPHA_MAX}°")
        with col2:
            st.metric("Reynolds Range", f"{RE_MIN:.1e} to {RE_MAX:.1e}")
        with col3:
            st.metric("Model", NEURALFOIL_MODEL_SIZE)
        
        if st.button("Start Airfoil Analysis", type="primary", use_container_width=True):
            if not hasattr(st.session_state, 'airfoils_folder'):
                st.error("Please configure parameters in Home tab first!")
                return
            
            try:
                # Initialize analyzer
                analyzer = AirfoilAnalyzer(
                    st.session_state.airfoils_folder,
                    velocity=st.session_state.velocity
                )
                
                # Run analysis with progress bar
                output_file = os.path.join(OUTPUT_FOLDER, NEURALFOIL_OUTPUT_CSV)
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(current, total, message):
                    progress = int((current / total) * 100)
                    progress_bar.progress(progress)
                    status_text.text(message)
                
                status_text.text("Starting NeuralFoil analysis...")
                db = analyzer.analyze_all_airfoils(output_file, progress_callback=update_progress)
                progress_bar.progress(100)
                
                # Store in session state
                st.session_state.db = db
                st.session_state.analysis_complete = True
                
                st.success(f"✓ Analysis complete! Analyzed {db['airfoil_name'].nunique()} airfoils")                    
            except Exception as e:
                st.error(f"Error during analysis: {e}")
        
        # Display results if available
        if st.session_state.analysis_complete and st.session_state.db is not None:
            st.markdown("---")
            st.subheader("Analysis Results")
            db = st.session_state.db
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Airfoils", db['airfoil_name'].nunique())
            with col2:
                st.metric("Data Points", len(db))
            with col3:
                st.metric("Reynolds Points", db['Re'].nunique())
            with col4:
                st.metric("Alpha Points", db['alpha_deg'].nunique())
            
            # Show sample data
            with st.expander("View Raw Data"):
                display_db = db.head(100).copy()
                display_db.index = range(1, len(display_db) + 1)
                st.dataframe(display_db, use_container_width=True)
            
            # Download button
            csv = db.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Full Analysis CSV",
                data=csv,
                file_name="airfoil_analysis.csv",
                mime="text/csv"
            )
    
    # ===== TAB 3: RANKING & SELECTION =====
    with tab3:
        st.header("Airfoil Ranking & Selection")
        
        if not st.session_state.analysis_complete:
            st.warning("Please complete airfoil analysis first!")
            return
        
        st.write("Score and rank airfoils based on mission requirements.")
        
        # Show application weights
        with st.expander("View Scoring Weights"):
            app = st.session_state.application
            weights_df = pd.DataFrame.from_dict(
                APPLICATION_WEIGHTS[app], 
                orient='index', 
                columns=['Weight']
            )
            st.dataframe(weights_df, use_container_width=True)
        
        if st.button("Calculate Rankings", type="primary", use_container_width=True):
            with st.spinner("Processing and scoring airfoils..."):
                try:
                    # Create combined dataframe
                    combined_df = create_combined_dataframe(st.session_state.db)
                    
                    # Score and rank
                    scorer = AirfoilScorer(application=st.session_state.application)
                    ranked_df = scorer.rank_airfoils(combined_df)
                    
                    # Add suitable chord
                    ranked_df["Suitable_chord"] = (
                        ranked_df["Re"] * KINEMATIC_VISCOSITY
                    ) / (AIR_DENSITY * st.session_state.velocity)
                    
                    # Store results
                    st.session_state.ranked_df = ranked_df
                    
                    # Save to file
                    output_file = os.path.join(OUTPUT_FOLDER, RANKED_OUTPUT_CSV)
                    save_dataframe_csv(ranked_df, output_file)
                    
                    st.success("✓ Ranking complete!")
                    
                except Exception as e:
                    st.error(f"Error during ranking: {e}")
        
        # Display rankings
        if st.session_state.ranked_df is not None:
            st.markdown("---")
            st.subheader("Top Ranked Airfoils")
            
            ranked_df = st.session_state.ranked_df
            
            # Number of results to show
            top_n = st.slider("Number of results to display", 5, 50, 20)
            
            # Display columns selection
            display_cols = [
                "airfoil_name", "Re", "Suitable_chord", "Optimum_angle", 
                "Optimum_CL", "MAX_CL/CD", "CL_max", "stall_angle_deg", 
                "angle_diff", "score"
            ]
            
            display_ranked = ranked_df[display_cols].head(top_n).copy()
            display_ranked.index = range(1, len(display_ranked) + 1)
            st.dataframe(
                display_ranked,
                use_container_width=True,
                height=400
            )
            
            # Bar plot
            st.subheader("Score Visualization")
            fig, ax = create_ranking_barplot(ranked_df, top_n=min(15, top_n), show=False)
            st.pyplot(fig)
            plt.close()
            
            # Download ranked results
            csv = ranked_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Ranked Results",
                data=csv,
                file_name="ranked_airfoils.csv",
                mime="text/csv"
            )
    
    # ===== TAB 4: WING DESIGN =====
    with tab4:
        st.header("Wing Design & Analysis")
        
        if st.session_state.ranked_df is None:
            st.warning("Please complete ranking first!")
            return
        
        st.write("Generate wing configurations and perform VLM analysis.")
        
        # Aspect ratio selection
        aspect_ratios_input = st.text_input(
            "Aspect Ratios (comma-separated)",
            value=",".join(map(str, DEFAULT_ASPECT_RATIOS))
        )
        aspect_ratios = [float(x.strip()) for x in aspect_ratios_input.split(",")]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Max Wingspan", f"{st.session_state.max_span} m")
        with col2:
            st.metric("MTOW", f"{st.session_state.mtow} kg")
        
        # Step 1: Generate configurations and run VLM analysis
        if st.button("Generate Wing Configurations & Run VLM Analysis", type="primary", use_container_width=True):
            try:
                # Step 1a: Generate configurations
                with st.spinner("Generating wing configurations..."):
                    designer = WingDesigner(
                        velocity=st.session_state.velocity,
                        max_wingspan=st.session_state.max_span,
                        aspect_ratios=aspect_ratios
                    )
                    
                    wing_configs = designer.generate_wing_configurations(st.session_state.ranked_df)
                    st.session_state.wing_configs = wing_configs
                    
                    st.success(f"✓ Generated {len(wing_configs)} wing configurations!")
                    
                    # Show preview
                    display_configs = wing_configs.head(20).copy()
                    display_configs.index = range(1, len(display_configs) + 1)
                    st.dataframe(display_configs, use_container_width=True)
                
                # Step 1b: Run VLM analysis immediately
                st.markdown("---")
                st.subheader("Running VLM Analysis...")
                
                analyzer = WingAnalyzer(st.session_state.airfoils_folder)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(current, total, message):
                    progress = int((current / total) * 100)
                    progress_bar.progress(progress)
                    status_text.text(message)
                
                status_text.text("Starting VLM analysis...")
                # Run analysis with progress updates
                wing_para_df = analyzer.analyze_all_wings(
                    st.session_state.wing_configs,
                    progress_callback=update_progress
                )
                progress_bar.progress(100)
                status_text.text("VLM analysis complete!")
                
                st.session_state.wing_para_df = wing_para_df
                
                # Save results
                output_file = os.path.join(OUTPUT_FOLDER, FINAL_WING_DATA_CSV)
                save_dataframe_csv(wing_para_df, output_file)
                
                st.success("✓ Wing configurations generated and VLM analysis complete!")
                
                # Step 1c: Filter suitable wings immediately
                st.markdown("---")
                st.subheader("Filtering Suitable Wings...")
                
                with st.spinner("Filtering wings that meet MTOW requirement..."):
                    selector = WingSelector(
                        mtow_kgs=st.session_state.mtow,
                        velocity=st.session_state.velocity
                    )
                    
                    suitable_df = selector.filter_suitable_wings(wing_para_df)
                    
                    if len(suitable_df) == 0:
                        st.error("❌ No wings meet the MTOW requirement!")
                    else:
                        ranked_suitable = selector.rank_suitable_wings(suitable_df)
                        st.session_state.suitable_wings_df = ranked_suitable
                        
                        st.success(f"✓ Found {len(ranked_suitable)} suitable wings!")
                        
                        # Display results
                        display_suitable = ranked_suitable[[
                            "airfoil_name", "Aspect_Ratio", "Suitable_chord",
                            "Wingspan_m", "Lift_Kgs", "MAX_CL/CD", "final_score"
                        ]].head(20).copy()
                        display_suitable.index = range(1, len(display_suitable) + 1)
                        st.dataframe(
                            display_suitable,
                            use_container_width=True
                        )
                        
                        # Save
                        output_file = os.path.join(OUTPUT_FOLDER, SUITABLE_WINGS_CSV)
                        save_dataframe_csv(ranked_suitable, output_file)
                        
                        # Download
                        csv = ranked_suitable.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Suitable Wings",
                            data=csv,
                            file_name="suitable_wings.csv",
                            mime="text/csv"
                        )
                
            except Exception as e:
                st.error(f"Error: {e}")
    
    # ===== TAB 5: VISUALIZATIONS =====
    with tab5:
        st.header("Aerodynamic Visualizations")
        
        if not st.session_state.analysis_complete:
            st.warning("Please complete airfoil analysis first!")
            return
        
        db = st.session_state.db
        
        # Visualization type selection
        viz_type = st.radio(
            "Visualization Type",
            ["Single Airfoil", "Compare Multiple Airfoils"],
            horizontal=True
        )
        
        if viz_type == "Single Airfoil":
            st.subheader("Single Airfoil Analysis")
            
            airfoils = sorted(db['airfoil_name'].unique())
            selected_airfoil = st.selectbox("Select Airfoil", airfoils)
            
            plot_type = st.selectbox(
                "Plot Type",
                ["CL vs Alpha", "CD vs Alpha", "CL vs CD (Polar)", "L/D vs Alpha", "CM vs Alpha"]
            )
            
            if st.button("Generate Plot"):
                plotter = AirfoilPlotter(db)
                
                try:
                    if plot_type == "CL vs Alpha":
                        fig, ax = plotter.plot_cl_vs_alpha(selected_airfoil, show=False)
                    elif plot_type == "CD vs Alpha":
                        fig, ax = plotter.plot_cd_vs_alpha(selected_airfoil, show=False)
                    elif plot_type == "CL vs CD (Polar)":
                        fig, ax = plotter.plot_cl_vs_cd(selected_airfoil, show=False)
                    elif plot_type == "L/D vs Alpha":
                        fig, ax = plotter.plot_ld_vs_alpha(selected_airfoil, show=False)
                    else:
                        fig, ax = plotter.plot_cm_vs_alpha(selected_airfoil, show=False)
                    
                    st.pyplot(fig)
                    plt.close()
                    
                except Exception as e:
                    st.error(f"Error creating plot: {e}")
        
        else:  # Compare Multiple
            st.subheader("Compare Multiple Airfoils")
            
            airfoils = sorted(db['airfoil_name'].unique())
            selected_airfoils = st.multiselect(
                "Select Airfoils to Compare",
                airfoils,
                default=airfoils[:min(3, len(airfoils))]
            )
            
            re_values = sorted(db['Re'].unique())
            re_target = st.selectbox("Select Reynolds Number", re_values)
            
            plot_type = st.selectbox(
                "Plot Type",
                ["CL vs Alpha", "CD vs Alpha", "Drag Polar", "L/D vs Alpha", "CM vs Alpha"]
            )
            
            if st.button("Generate Comparison"):
                if len(selected_airfoils) < 2:
                    st.error("Please select at least 2 airfoils to compare")
                else:
                    plotter = ComparisonPlotter(db)
                    
                    try:
                        if plot_type == "CL vs Alpha":
                            fig, ax = plotter.plot_cl_comparison(selected_airfoils, re_target, show=False)
                        elif plot_type == "CD vs Alpha":
                            fig, ax = plotter.plot_cd_comparison(selected_airfoils, re_target, show=False)
                        elif plot_type == "Drag Polar":
                            fig, ax = plotter.plot_polar_comparison(selected_airfoils, re_target, show=False)
                        elif plot_type == "L/D vs Alpha":
                            fig, ax = plotter.plot_ld_comparison(selected_airfoils, re_target, show=False)
                        else:
                            fig, ax = plotter.plot_cm_comparison(selected_airfoils, re_target, show=False)
                        
                        st.pyplot(fig)
                        plt.close()
                        
                    except Exception as e:
                        st.error(f"Error creating plot: {e}")


if __name__ == "__main__":
    main()
