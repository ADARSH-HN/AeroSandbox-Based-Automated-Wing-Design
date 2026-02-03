"""
Configuration file for Wing Analyzer application
Contains all constants and default settings
"""

# Default Analysis Parameters
DEFAULT_MTOW_KGS = 8.5  # Maximum Takeoff Weight in kilograms
DEFAULT_MAX_WINGSPAN = 1.8  # Maximum Wingspan in meters
DEFAULT_VELOCITY = 13.0  # m/s
DEFAULT_ASPECT_RATIOS = [3, 4, 5, 6, 7]

# Airfoil Analysis Parameters
ALPHA_MIN = -5  # Minimum angle of attack
ALPHA_MAX = 20   # Maximum angle of attack
ALPHA_STEP = 0.2 # Angle step size
RE_MIN = 1.5e5   # Minimum Reynolds number
RE_MAX = 4e5     # Maximum Reynolds number
RE_POINTS = 10   # Number of Reynolds number points
MACH_BASE = 343  # Speed of sound for Mach calculation

# NeuralFoil Configuration
NEURALFOIL_MODEL_SIZE = "xxxlarge"

# Operating Range for Optimization
OPER_ALPHA_MIN = 0
OPER_ALPHA_MAX = 5

# Application Weights for Scoring
APPLICATION_WEIGHTS = {
    "payload": {
        "MAX_CL/CD_n": 0.25,
        "Optimum_CL_n": 0.30,
        "CL_max_n": 0.20,
        "CL_at_0_deg_n": 0.10,
        "angle_diff_n": 0.10,
        "Optimum_CD_n": 0.05,
    },
    "endurance": {
        "MAX_CL/CD_n": 0.40,
        "Optimum_CD_n": 0.20,
        "Optimum_CL_n": 0.15,
        "angle_diff_n": 0.15,
        "CL_at_0_deg_n": 0.10,
    },
    "trainer": {
        "angle_diff_n": 0.35,
        "CL_at_0_deg_n": 0.20,
        "CL_max_n": 0.20,
        "MAX_CL/CD_n": 0.15,
        "Optimum_CL_n": 0.10,
    }
}

# Physical Constants
GRAVITY = 9.81  # m/s^2
AIR_DENSITY = 1.225  # kg/m^3 (at sea level, 15°C)
KINEMATIC_VISCOSITY = 1.81e-5  # m^2/s (at sea level, 15°C)

# File Paths (relative to project root)
AIRFOILS_FOLDER = r"E:\Aeroclub\Airfoils_twst"
OUTPUT_FOLDER = r"E:\Aeroclub\software"

# Output Files
NEURALFOIL_OUTPUT_CSV = "neuralfoil_output.csv"
RANKED_OUTPUT_CSV = "ranked_airfoils.csv"
FINAL_WING_DATA_CSV = "final_wing_data.csv"
SUITABLE_WINGS_CSV = "suitable_wings.csv"

# Visualization Settings
PLOT_COLORS = ["red", "green", "blue"]
PLOT_DPI = 100
PLOT_STYLE = "seaborn"
