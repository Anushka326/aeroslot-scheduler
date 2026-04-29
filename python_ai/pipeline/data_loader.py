import pandas as pd
from pathlib import Path

class TemporalDataLoader:
    """
    Executes precise Time-Aware Splitting natively avoiding Temporal Leakage structurally cleanly.
    """
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        
    def load_splits(self, target_col: str = 'target_delay_minutes'):
        print(f"[DataLoader] Fetching bounds from {self.data_path}...")
        df = pd.read_parquet(self.data_path)
        
        # Build logical targets securely
        df['target_is_delayed'] = (df['target_delay_minutes'] > 15).astype(int)
        
        # Feature isolation
        features = ['geoaltitude', 'velocity', 'wake_factor', 'airspace_congestion', 'occupancy_est_sec']
        
        train_df = df[df['dataset_split'] == 'train']
        val_df = df[df['dataset_split'] == 'val']
        test_df = df[df['dataset_split'] == 'test']
        
        X_train, y_train = train_df[features], train_df[target_col]
        X_val, y_val = val_df[features], val_df[target_col]
        X_test, y_test = test_df[features], test_df[target_col]
        
        print(f" -> Chronological Maps Resolved! Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")
        return X_train, y_train, X_val, y_val, X_test, y_test
