import pandas as pd
import matplotlib.pyplot as plt
import os

FOLDER = "dataset"
FILES_TO_PLOT = ["LEFT/LEFT_01.csv", "RIGHT/RIGHT_01.csv", "FORWARD/FORWARD_01.csv"]

def plot_files():
    plt.figure(figsize=(12, 6))
    
    for file_path in FILES_TO_PLOT:
        full_path = os.path.join(FOLDER, file_path)
        if not os.path.exists(full_path):
            print(f"[WARNING] File not found: {full_path} - Skipping")
            continue
        
        df = pd.read_csv(full_path)
        
        if 'timestamp' not in df.columns or 'value' not in df.columns:
            print(f"[WARNING] {full_path} missing required columns (timestamp, value)")
            continue
        
        label = file_path.replace(".csv", "").replace("/", " - ")
        plt.plot(df['timestamp'], df['value'], label=label, linewidth=2)

    plt.xlabel("Time (ms)", fontsize=12)
    plt.ylabel("Hall Sensor Value (ADC)", fontsize=12)
    plt.title("Magnetic Signal Comparison for Different Classes", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_files()
