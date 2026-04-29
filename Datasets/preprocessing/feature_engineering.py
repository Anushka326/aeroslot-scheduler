import pandas as pd
import numpy as np
from pathlib import Path
from pyarrow import parquet as pq

def engineer_features(base_dir: Path):
    print("[Feature Eng] Generating Physical Airport Descriptors...")
    
    # Load Telemetry and Metadata natively securely
    telemetry_path = base_dir / 'cleaned' / 'clean_telemetry.parquet'
    meta_path = base_dir / 'cleaned' / 'clean_aircraft_metadata.parquet'
    
    if not telemetry_path.exists() or not meta_path.exists():
        print("[Feature Eng] Missing cleaned requirements. Exiting.")
        return

    tel_df = pd.read_parquet(telemetry_path)
    meta_df = pd.read_parquet(meta_path)

    # Base Join: Intersecting physical tracks with Wake Separation geometries safely
    df = pd.merge(tel_df, meta_df[['icao24', 'icaowtc', 'typecode']], on='icao24', how='inner')

    # FEATURE 1: Operational Phase (Taxiing vs Approach)
    df['operational_phase'] = np.where(df['onground'] == True, 'TAXI', 
                                np.where(df['geoaltitude'] < 1000, 'FINAL_APPROACH', 'EN_ROUTE'))

    # FEATURE 2: Wake Separation Factor
    # Maps Heavy (H) to 3, Medium (M) to 2, Light (L) to 1 natively mapping the Wake bounds geometrically
    wake_map = {'H': 3, 'M': 2, 'L': 1, 'J': 4}  # J = Super (A380)
    df['wake_factor'] = df['icaowtc'].map(wake_map).fillna(2.0)

    # FEATURE 3: Temporal Aggregation (Hour Blocks)
    df['time'] = pd.to_numeric(df['time'], errors='coerce')
    df['hour_block'] = (df['time'] // 3600) % 24

    # FEATURE 4: Simulated Congestion Metric (Planes in airspace per hour block natively)
    congestion_df = df.groupby('hour_block').size().reset_index(name='airspace_congestion')
    df = pd.merge(df, congestion_df, on='hour_block', how='left')
    
    # FEATURE 5: Runway Occupancy Baseline (Seconds) based on Wake limits
    df['occupancy_est_sec'] = 45 + (df['wake_factor'] * 15)

    out_path = base_dir / 'features' / 'advanced_telemetry_features.parquet'
    df.to_parquet(out_path, engine='pyarrow', index=False)
    
    print(f" -> Feature Space Constructed: {len(df.columns)} Features | {len(df)} Records globally.")

if __name__ == "__main__":
    b_dir = Path(__file__).resolve().parent.parent
    engineer_features(b_dir)
