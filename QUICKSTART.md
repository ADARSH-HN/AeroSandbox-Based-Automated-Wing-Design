# 🚀 Quick Start Guide - Wing Analyzer Pro

## Installation (First Time Only)

### Option 1: Using the Batch File (Windows - Easiest)
1. Double-click `run_app.bat`
2. The script will automatically install dependencies and launch the app

### Option 2: Manual Installation
1. Open PowerShell or Command Prompt
2. Navigate to project folder:
   ```bash
   cd "e:\Aeroclub\Wing parameter decide"
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Method 1: Batch File (Windows)
- Double-click `run_app.bat`

### Method 2: Python Launcher
```bash
python launcher.py
```

### Method 3: Direct Streamlit
```bash
streamlit run app.py
```

## First Time Usage

1. **Launch the app** using any method above
2. **Configure parameters** in the Home tab:
   - Verify airfoils folder path (default: `E:\Aeroclub\Airfoils_twst`)
   - Set your MTOW (kg)
   - Set maximum wingspan (m)
   - Choose design velocity (m/s)
   - Select mission type

3. **Run Analysis** (Airfoil Analysis tab):
   - Click "Start Airfoil Analysis"
   - Wait for completion (may take 5-10 minutes)
   - Download results CSV

4. **Rank Airfoils** (Ranking & Selection tab):
   - Click "Calculate Rankings"
   - Review top-ranked airfoils
   - Adjust scoring weights if needed

5. **Design Wings** (Wing Design tab):
   - Click "Generate Wing Configurations"
   - Optionally run VLM analysis (time-intensive)
   - Click "Filter Suitable Wings"
   - Download suitable wings CSV

6. **Visualize** (Visualizations tab):
   - Select single airfoil or comparison mode
   - Choose plot type
   - Generate plots

## Example Script

To test the modules without the UI:
```bash
python example.py
```

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "Airfoils folder not found"
- Update path in Home tab or in `config.py`
- Ensure `.dat` files are in the folder

### Application won't start
```bash
python -m streamlit run app.py
```

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

## Tips

- **First run**: Use a small set of airfoils (2-3) to test
- **VLM Analysis**: Skip for quick results, enable for accuracy
- **Performance**: Reduce Reynolds points in `config.py` for faster analysis
- **Results**: All outputs saved to `E:\Aeroclub\software` by default

## Need Help?

- Check the full [README.md](README.md)
- Review `config.py` for customization options
- See `example.py` for programmatic usage

---
**Happy designing! ✈️**
