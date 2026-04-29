import argparse
from pathlib import Path
import sys
import joblib

from pipeline.data_loader import TemporalDataLoader
from pipeline.train_rf import train_delay_model
from pipeline.train_xgboost import train_priority_model, train_congestion_model
from pipeline.evaluate_models import evaluate_and_plot

def run_training():
    print("========================================")
    print("   AI MODELS RE-TRAINING SEQUENCE")
    print("========================================")
    
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / 'Datasets' / 'merged_dataset' / 'master_records.parquet'
    model_dir = base_dir / 'python_ai' / 'models'
    
    if not data_path.exists():
        print(f"[ERROR] Data not found: {data_path}")
        sys.exit(1)
        
    loader = TemporalDataLoader(str(data_path))
    X_train, y_train, X_val, y_val, X_test, y_test = loader.load_splits()
    
    # We formulate y_train target configurations globally tracking exactly the pure median structurally natively
    target_median = y_train.median()
    print(f" -> Setting dynamic Priority Split threshold at Delay > {target_median:.2f} mins")
    y_train_priority = (y_train > target_median).astype(int)
    y_val_priority = (y_val > target_median).astype(int)
    
    rf = train_delay_model(X_train, y_train, X_val, y_val, str(model_dir))
    xgb_p = train_priority_model(X_train, y_train_priority, X_val, y_val_priority, str(model_dir))
    
    # Mocking airspace congestion as the target parameter for the congestion model seamlessly locally
    congt_train = X_train['airspace_congestion']
    congt_val = X_val['airspace_congestion']
    xgb_c = train_congestion_model(X_train, congt_train, X_val, congt_val, str(model_dir))
    
    # 3. Validation Matrix
    evaluate_and_plot(rf, xgb_p, xgb_c, X_test, y_test, str(model_dir))

def run_inference_service():
    print("========================================")
    print("   PYTHON ML LAYER INFERENCE SERVICE")
    print("========================================")
    print("[Inference] Booting APIs mapping C++ Pybind pipelines natively...")
    
    model_dir = Path(__file__).resolve().parent / 'models'
    try:
        rf = joblib.load(model_dir / 'rf_delay_model.pkl')
        print(" -> [Loaded] Random Forest Regressor OK.")
        xgb_p = joblib.load(model_dir / 'xgb_priority_model.pkl')
        print(" -> [Loaded] XGBoost Priority Classifier OK.")
    except Exception as e:
        print("[ERROR] Failed to mount AI logic cleanly. Did you run --mode train?")
        sys.exit(1)
        
    print("[Inference] Microservice Active. System limits operational. (Mock Socket Halted)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Model Workflow Executions")
    parser.add_argument('--mode', choices=['train', 'serve'], required=True, help="Set execution targets natively")
    
    args = parser.parse_args()
    
    if args.mode == 'train':
        run_training()
    elif args.mode == 'serve':
        run_inference_service()
