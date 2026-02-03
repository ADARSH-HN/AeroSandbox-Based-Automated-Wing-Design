# Wing Analyzer Pro - Project Structure

## 📁 Complete File Organization

```
Wing parameter decide/
│
├── 🚀 MAIN APPLICATION FILES
│   ├── app.py                    # Streamlit web UI (main interface)
│   ├── launcher.py               # Quick launcher script
│   └── run_app.bat               # Windows batch launcher
│
├── 🔧 CORE MODULES
│   ├── config.py                 # Configuration & constants
│   ├── utils.py                  # Utility functions
│   ├── airfoil_analysis.py       # Airfoil analysis & NeuralFoil
│   ├── scoring.py                # Ranking & scoring algorithms
│   ├── wing_design.py            # Wing design & VLM analysis
│   └── visualization.py          # Plotting & charts
│
├── 📚 DOCUMENTATION
│   ├── README.md                 # Full documentation
│   ├── QUICKSTART.md             # Quick start guide
│   └── PROJECT_STRUCTURE.md      # This file
│
├── 📦 CONFIGURATION
│   ├── requirements.txt          # Python dependencies
│   └── .gitignore                # Git ignore rules
│
├── 💡 EXAMPLES & LEGACY
│   ├── example.py                # Example usage script
│   └── wing analyzer.py          # Original monolithic script (backup)
│
└── 📊 OUTPUT (generated at runtime)
    ├── neuralfoil_output.csv     # Raw analysis data
    ├── ranked_airfoils.csv       # Scored & ranked airfoils
    ├── final_wing_data.csv       # Wing configurations
    └── suitable_wings.csv        # Wings meeting requirements

```

## 🔍 Module Dependencies

```
app.py
├── config.py
├── airfoil_analysis.py
│   ├── config.py
│   └── utils.py
├── scoring.py
│   ├── config.py
│   └── utils.py
├── wing_design.py
│   ├── config.py
│   └── utils.py
└── visualization.py
    └── config.py
```

## 📝 Module Descriptions

### **app.py** (Main UI)
- Streamlit-based web interface
- 5 tabs: Home, Analysis, Ranking, Wing Design, Visualizations
- Session state management
- Interactive parameter configuration
- Progress tracking and result display

### **config.py** (Configuration)
- Design parameters (MTOW, wingspan, velocity)
- Analysis settings (alpha range, Reynolds range)
- Mission-specific scoring weights
- Physical constants
- File paths

### **utils.py** (Utilities)
- Normalization functions
- File management helpers
- Reynolds number calculations
- Lift force calculations
- Unit conversions

### **airfoil_analysis.py** (Analysis)
- `AirfoilAnalyzer`: NeuralFoil analysis orchestration
- Batch processing of .dat files
- Stall data extraction
- Optimum operating point detection
- Zero-alpha performance metrics

### **scoring.py** (Ranking)
- `AirfoilScorer`: Mission-based scoring system
- Feature normalization
- Weighted scoring algorithms
- Application comparison tools
- Top-N selection

### **wing_design.py** (Wing Design)
- `WingDesigner`: Configuration generation
- `WingAnalyzer`: VLM analysis wrapper
- `WingSelector`: Performance filtering
- Aspect ratio variations
- MTOW compliance checking

### **visualization.py** (Plotting)
- `AirfoilPlotter`: Single airfoil plots
- `ComparisonPlotter`: Multi-airfoil comparisons
- CL, CD, CM, L/D plots
- Drag polar visualization
- Ranking bar charts

## 🎯 Data Flow

```
1. Airfoil .dat files
   ↓
2. AirfoilAnalyzer (NeuralFoil)
   ↓
3. neuralfoil_output.csv
   ↓
4. Feature extraction & combination
   ↓
5. AirfoilScorer (mission-based)
   ↓
6. ranked_airfoils.csv
   ↓
7. WingDesigner (configurations)
   ↓
8. WingAnalyzer (VLM - optional)
   ↓
9. final_wing_data.csv
   ↓
10. WingSelector (MTOW filtering)
    ↓
11. suitable_wings.csv
```

## 🚀 Entry Points

### For End Users:
- **Windows**: Double-click `run_app.bat`
- **Cross-platform**: `python launcher.py`
- **Direct**: `streamlit run app.py`

### For Developers:
- **Import modules**: Use as Python library
- **Example script**: `python example.py`
- **Customize**: Edit `config.py` and modules

## 📊 Key Features by Module

| Module | Key Features |
|--------|-------------|
| **app.py** | Web UI, 5 tabs, interactive parameters, session state |
| **airfoil_analysis.py** | NeuralFoil, batch processing, feature extraction |
| **scoring.py** | 3 mission profiles, normalized scoring, ranking |
| **wing_design.py** | AR variations, VLM analysis, MTOW filtering |
| **visualization.py** | 10+ plot types, single/comparison modes |
| **config.py** | Centralized settings, easy customization |
| **utils.py** | Common functions, calculations, file I/O |

## 🔄 Workflow Summary

1. **Configure** → Home tab or `config.py`
2. **Analyze** → Airfoil Analysis tab (NeuralFoil)
3. **Score** → Ranking & Selection tab (mission weights)
4. **Design** → Wing Design tab (AR variations + VLM)
5. **Filter** → Suitable wings (MTOW compliance)
6. **Visualize** → Visualizations tab (plots & charts)
7. **Export** → Download CSVs and plots

## 💾 Output Files Location

Default: `E:\Aeroclub\software`

Can be changed in `config.py`:
```python
OUTPUT_FOLDER = r"your\custom\path"
```

## 🛠️ Customization Points

- **Mission weights**: Edit `APPLICATION_WEIGHTS` in `config.py`
- **Analysis range**: Modify `ALPHA_MIN/MAX`, `RE_MIN/MAX` in `config.py`
- **Aspect ratios**: Change `DEFAULT_ASPECT_RATIOS` in `config.py`
- **UI styling**: Edit CSS in `app.py`
- **Plot settings**: Adjust in `visualization.py`

## 📋 Dependencies

Core:
- aerosandbox (analysis)
- streamlit (UI)
- pandas (data)
- matplotlib (plotting)
- numpy (computation)

See `requirements.txt` for versions.

---

**Last Updated**: Project creation
**Version**: 1.0
**Status**: Production Ready ✅
