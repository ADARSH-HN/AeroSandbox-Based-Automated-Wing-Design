"""
Quick launcher script for Wing Analyzer
"""
import subprocess
import sys
import os


def main():
    """Launch the Wing Analyzer application"""
    
    print("="*60)
    print("  Wing Analyzer Pro - Launcher")
    print("="*60)
    print()
    print("Starting Streamlit application...")
    print("The app will open in your default browser.")
    print()
    print("To stop the application, press Ctrl+C in this terminal.")
    print("="*60)
    print()
    
    try:
        # Launch streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\nApplication stopped.")
    except Exception as e:
        print(f"\nError launching application: {e}")
        print("\nTry running manually with:")
        print("  streamlit run app.py")


if __name__ == "__main__":
    main()
