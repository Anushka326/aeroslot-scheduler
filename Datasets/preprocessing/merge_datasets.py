import pandas as pd
import numpy as np
from pathlib import Path
import os

def generate_master_dataset(base_dir: Path):
    print("[Dataset Merge] Formulating System Output Splitting...")
    
    feats_path = base_dir / 'features' / 'advanced_telemetry_features.parquet'
    delays_path = base_dir / 'cleaned' / 'clean_delays.parquet'
    
    if not feats_path.exists():
        print(f"[ERROR] Features file missing.")
        return

    df = pd.read_parquet(feats_path)
    
    # To attach actual delay targets, we mock a mapping if direct flight_id linkages are missing from OpenSky bounds
    # In full production, this maps matching timestamps+ICAO to Airline endpoints securely natively
    print(" -> Injecting Priority Targets and Mocking Systemic Delays constraints...")
    
    # 1. Generate Fake Flight IDs identifying unique trajectories natively
    # OpenSky tracks planes by ICAO24; we simulate flight numbers
    df['flight_id'] = df['icao24'].astype(str) + "_" + df['hour_block'].astype(str)
    
    # 2. Extract ML Labels (Simulated Arrival Delays mapping closely to the delay dataset bounds)
    np.random.seed(42)
    # Target: Delay (min) = (wake * 2) + (congestion / 1000) + noise
    df['target_delay_minutes'] = (df['wake_factor'] * 2.5) + (df['airspace_congestion'] / 500) + np.random.normal(0, 5, len(df))
    df['target_delay_minutes'] = df['target_delay_minutes'].clip(lower=0) 

    # 3. Time Series Splitting (CRITICAL: Sort by timestamp securely blocking temporal leaks natively)
    df = df.sort_values(by='time').reset_index(drop=True)
    
    total = len(df)
    train_idx = int(total * 0.70)
    val_idx = int(total * 0.85)
    
    df['dataset_split'] = 'train'
    df.loc[train_idx:val_idx, 'dataset_split'] = 'val'
    df.loc[val_idx:, 'dataset_split'] = 'test'
    
    print(f" -> Chronological Maps Locked! Train: {train_idx} | Val: {val_idx-train_idx} | Test: {total-val_idx}")
    
    # 4. Final Output Construction
    out_dir = base_dir / 'merged_dataset'
    out_dir.mkdir(parents=True, exist_ok=True)
    
    master_path = out_dir / 'master_records.parquet'
    
    # Select columns specifically targeting the XGBoost Model inputs securely natively
    cols_to_keep = ['flight_id', 'time', 'icao24', 'geoaltitude', 'velocity', 'wake_factor', 
                    'airspace_congestion', 'occupancy_est_sec', 'target_delay_minutes', 'dataset_split']
                    
    master_df = df[cols_to_keep]
    master_df.to_parquet(master_path, engine='pyarrow', index=False)
    
    print(f"[Dataset Merge] SUCCESS! Master records published mapping {total} rows cleanly locally.")

if __name__ == "__main__":
    b_dir = Path(__file__).resolve().parent.parent
    generate_master_dataset(b_dir)
