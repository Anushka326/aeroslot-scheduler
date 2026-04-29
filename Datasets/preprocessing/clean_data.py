import os
import pandas as pd
import numpy as np
from pathlib import Path
import glob

def ensure_directories():
    base_dir = Path(__file__).resolve().parent.parent
    for d in ['cleaned', 'features', 'merged_dataset']:
        (base_dir / d).mkdir(parents=True, exist_ok=True)
    return base_dir

def clean_metadata(base_dir: Path):
    """Processes OpenSky Aircraft Metadata retaining structural wake limits."""
    print("[Preprocessing] Cleaning Aircraft Metadata...")
    meta_path = base_dir / 'aircraft_metadata' / 'aircraft-database-complete-2024-10.csv'
    
    # Load focusing specifically on Wake Categories + Priority heuristics
    df = pd.read_csv(meta_path, dtype=str, on_bad_lines='skip')
    df.columns = df.columns.str.replace("'", "")
    
    cols_to_use = ['icao24', 'manufacturerName', 'model', 'typecode', 'engines']
    # Use fallback map for wake if icaowtc is missing:
    
    # Clean anomalies natively
    df = df.dropna(subset=['icao24'])
    df['icao24'] = df['icao24'].str.lower().str.strip()
    df.drop_duplicates(subset=['icao24'], keep='first', inplace=True)
    
    # Fill wake category strictly to Medium (M) to prevent separation faults globally
    if 'icaowtc' not in df.columns and 'icaoAircraftClass' in df.columns:
        df['icaowtc'] = df['icaoAircraftClass']
    if 'icaowtc' not in df.columns:
        df['icaowtc'] = 'M'
    df['icaowtc'] = df['icaowtc'].fillna('M')
    
    out_path = base_dir / 'cleaned' / 'clean_aircraft_metadata.parquet'
    df.to_parquet(out_path, engine='pyarrow', index=False)
    print(f" -> Exported Meta: {len(df)} records.")

def clean_opensky_telemetry(base_dir: Path):
    """Parses massive State Vectors isolating terminal approach trajectories."""
    print("[Preprocessing] Consolidating OpenSky Telemetry...")
    telemetry_files = glob.glob(str(base_dir / 'opensky_states' / 'week*.csv'))
    
    # We load a sample mapping to prevent blowing out memory entirely on standard nodes
    df_list = []
    for file in telemetry_files[:2]:  # Loading select weeks for benchmark throughput
        print(f" -> Parsing {os.path.basename(file)}...")
        df_week = pd.read_csv(file, usecols=['time', 'icao24', 'lat', 'lon', 'velocity', 'heading', 'vertrate', 'geoaltitude', 'onground'])
        
        # Isolate aircraft transitioning near terminal bounds (e.g. altitude < 15,000 ft) natively
        df_week = df_week[(df_week['geoaltitude'] < 4500) | (df_week['onground'] == True)]
        
        # Smooth absolute negative velocities securely
        df_week = df_week[df_week['velocity'] >= 0]
        df_list.append(df_week)

    if not df_list: return
    
    merged_telemetry = pd.concat(df_list, ignore_index=True)
    merged_telemetry['icao24'] = merged_telemetry['icao24'].str.strip()
    
    out_path = base_dir / 'cleaned' / 'clean_telemetry.parquet'
    merged_telemetry.to_parquet(out_path, engine='pyarrow', index=False)
    print(f" -> Exported Telemetry: {len(merged_telemetry)} points securely.")

def clean_delays(base_dir: Path):
    """Processes Kaggle Delays explicitly mapping operational congestion histories cleanly."""
    print("[Preprocessing] Cleansing Delay Metrics...")
    delay_path = base_dir / 'delays' / 'flight_dealys_cancellations' / 'flights_sample_3m.csv'
    
    if not delay_path.exists():
        print(f" -> [WARN] Delay file missing at {delay_path}. Skipping.")
        return
        
    df = pd.read_csv(delay_path, low_memory=False)
    
    # Target pure arrival delay metrics securely
    target_cols = ['FLIGHT_NUMBER', 'AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 
                   'SCHEDULED_ARRIVAL', 'ARRIVAL_DELAY', 'WEATHER_DELAY']
    
    df = df[[c for c in target_cols if c in df.columns]]
    
    # Impute missing natively
    if 'ARRIVAL_DELAY' in df.columns:
        df['ARRIVAL_DELAY'] = df['ARRIVAL_DELAY'].fillna(0)
    if 'WEATHER_DELAY' in df.columns:
        df['WEATHER_DELAY'] = df['WEATHER_DELAY'].fillna(0)
        
    out_path = base_dir / 'cleaned' / 'clean_delays.parquet'
    df.to_parquet(out_path, engine='pyarrow', index=False)
    print(f" -> Exported Delays: {len(df)} records.")

if __name__ == "__main__":
    b_dir = ensure_directories()
    clean_metadata(b_dir)
    clean_delays(b_dir)
    clean_opensky_telemetry(b_dir)
    print("[Preprocessing] Part 1: Data Cleaning Completed.")
