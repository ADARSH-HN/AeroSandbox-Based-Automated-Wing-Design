# ✈️ Wing Analyzer 

**Aerodynamic Analysis & Wing Design Tool for RC Aircraft**

A comprehensive Python application for analyzing airfoils, scoring them based on mission requirements, and designing optimal wing configurations for remote control aircraft.

## 🌟 Features

- **Airfoil Analysis**: Uses NeuralFoil to analyze airfoils across ranges of angles of attack and Reynolds numbers
- **Multi-Mission Scoring**: Ranks airfoils based on payload, endurance, or trainer mission profiles
- **Wing Design**: Generates and evaluates wing configurations with different aspect ratios
- **VLM Analysis**: Performs Vortex Lattice Method analysis for accurate aerodynamic predictions
- **Performance Filtering**: Selects wings that meet MTOW (Maximum Takeoff Weight) requirements
- **Interactive UI**: Beautiful Streamlit interface for easy parameter configuration and visualization
- **Comprehensive Plots**: Visualizes CL, CD, L/D ratios, moment coefficients, and comparisons

## 📁 Project Structure

```
Wing parameter decide/
├── app.py                    # Main Streamlit UI application
├── config.py                 # Configuration and constants
├── utils.py                  # Utility functions
├── airfoil_analysis.py       # Airfoil analysis module
├── scoring.py                # Scoring and ranking module
├── wing_design.py            # Wing design and VLM analysis
├── visualization.py          # Plotting and visualization
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── wing analyzer.py          # Original monolithic script (legacy)
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or navigate to the project folder**:
   ```bash
   cd "e:\Aeroclub\Wing parameter decide"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare airfoil files**:
   - Place your `.dat` airfoil files in the designated folder
   - Default: `E:\Aeroclub\Airfoils_twst`
   - Update path in `config.py` if different

## 💻 Usage

### Running the Streamlit Application

```bash
streamlit run app.py
```

This will open the application in your default web browser.

### Application Workflow

1. **Home Tab**: Configure design parameters
   - Set MTOW (Maximum Takeoff Weight)
   - Set maximum wingspan constraint
   - Choose design velocity
   - Select mission type (payload/endurance/trainer)

2. **Airfoil Analysis Tab**: Analyze airfoils
   - Click "Start Airfoil Analysis"
   - Wait for NeuralFoil to analyze all airfoils
   - View and download results

3. **Ranking & Selection Tab**: Score airfoils
   - Review scoring weights for your mission
   - Calculate rankings
   - View top-ranked airfoils
   - Download ranked results

4. **Wing Design Tab**: Generate wing configurations
   - Generate configurations with different aspect ratios
   - Optionally run VLM analysis (time-intensive)
   - Filter wings meeting MTOW requirements
   - Download suitable wing designs

5. **Visualizations Tab**: Create plots
   - Single airfoil plots (CL, CD, L/D, CM vs alpha)
   - Compare multiple airfoils at specific Reynolds numbers
   - Export plots as needed

### Using as Python Modules

You can also import and use the modules in your own scripts:

```python
from airfoil_analysis import AirfoilAnalyzer
from scoring import AirfoilScorer
from wing_design import WingDesigner, WingAnalyzer
from visualization import AirfoilPlotter

# Analyze airfoils
analyzer = AirfoilAnalyzer(folder="path/to/airfoils", velocity=13)
db = analyzer.analyze_all_airfoils("output.csv")

# Score and rank
scorer = AirfoilScorer(application="payload")
ranked = scorer.rank_airfoils(combined_df)

# Design wings
designer = WingDesigner(velocity=13, max_wingspan=1.8)
configs = designer.generate_wing_configurations(ranked)

# Visualize
plotter = AirfoilPlotter(db)
plotter.plot_cl_vs_alpha("airfoil_name")
```

## ⚙️ Configuration

Edit [config.py](config.py) to customize:

- **Analysis parameters**: Alpha range, Reynolds range, NeuralFoil model size
- **Design constraints**: Default MTOW, wingspan limits, aspect ratios
- **Scoring weights**: Mission-specific criteria weights
- **File paths**: Input/output directories
- **Physical constants**: Air density, viscosity, etc.

### Mission Type Scoring Weights

**Payload Mission** (optimized for carrying capacity):
- MAX_CL/CD: 25%
- Optimum_CL: 30%
- CL_max: 20%
- Others: 25%

**Endurance Mission** (optimized for flight time):
- MAX_CL/CD: 40%
- Optimum_CD: 20%
- Optimum_CL: 15%
- Others: 25%

**Trainer Mission** (optimized for gentle handling):
- angle_diff: 35%
- CL_at_0_deg: 20%
- CL_max: 20%
- Others: 25%

## 📊 Output Files

The application generates several CSV files in the output folder:

- `neuralfoil_output.csv`: Raw aerodynamic data for all airfoils
- `ranked_airfoils.csv`: Scored and ranked airfoils
- `final_wing_data.csv`: Wing configurations with VLM results
- `suitable_wings.csv`: Wings meeting MTOW requirements

## 🔧 Technical Details

### Analysis Process

1. **Airfoil Loading**: Reads `.dat` coordinate files
2. **Kulfan Transformation**: Converts to parametric representation
3. **NeuralFoil Analysis**: Predicts CL, CD, CM across operating envelope
4. **Feature Extraction**: Identifies stall points, optimum L/D, zero-alpha performance
5. **Normalization**: Scales features to [0,1] range
6. **Weighted Scoring**: Applies mission-specific weights
7. **Wing Generation**: Creates configurations within constraints
8. **VLM Analysis**: Computes 3D aerodynamics (optional)
9. **Performance Filtering**: Selects designs meeting requirements

### Key Algorithms

- **NeuralFoil**: Machine learning-based airfoil aerodynamics prediction
- **VLM (Vortex Lattice Method)**: Potential flow solver for finite wings
- **Multi-criteria scoring**: Weighted sum of normalized features

## 📚 Dependencies

- **aerosandbox**: Aerodynamic analysis and VLM solver
- **numpy**: Numerical computations
- **pandas**: Data manipulation and analysis
- **matplotlib**: Plotting and visualization
- **streamlit**: Web-based user interface

## 🐛 Troubleshooting

### "Airfoil folder not found"
- Verify the path in [config.py](config.py) or enter correct path in UI
- Ensure `.dat` files are present

### "No airfoils meet MTOW requirement"
- Increase max wingspan constraint
- Reduce MTOW requirement
- Try different aspect ratios
- Check if VLM analysis ran correctly

### VLM analysis fails
- Verify airfoil `.dat` files are valid
- Check for corrupted airfoil geometry
- Ensure sufficient memory for large batches

### Slow performance
- Reduce number of airfoils
- Decrease Reynolds number points in [config.py](config.py)
- Skip VLM analysis for quick estimates
- Use smaller NeuralFoil model size

## 📝 License

This project is for educational and research purposes. Please cite AeroSandbox and NeuralFoil if used in publications.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add tapered wing support
- Include structural analysis
- Export to CAD formats
- Support for multi-segment wings
- Optimization algorithms

## 📧 Contact

For questions or support related to this project, please refer to the AeroSandbox documentation:
- GitHub: https://github.com/peterdsharpe/AeroSandbox
- Documentation: https://peterdsharpe.github.io/AeroSandbox/

## 🙏 Acknowledgments

- **AeroSandbox** by Peter Sharpe - Aircraft design optimization framework
- **NeuralFoil** - Machine learning airfoil aerodynamics
- AEROCLUB NITTE - Original project development

---

**Made with ❤️ for RC aircraft enthusiasts**
