import xgboost as xgb
from sklearn.metrics import f1_score, mean_absolute_error
import joblib
import os

def train_priority_model(X_train, y_train, X_val, y_val, model_dir):
    print("[Trainer: XGBoost Priority] Booting Gradient Boosting Maps...")
    
    model = xgb.XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
    
    preds = model.predict(X_val)
    f1 = f1_score(y_val, preds)
    print(f" -> [XGB Validation Results] F1 Score (Priority Classes): {f1:.3f}")
    
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, 'xgb_priority_model.pkl'))
    return model

def train_congestion_model(X_train, y_train, X_val, y_val, model_dir):
    print("[Trainer: XGBoost Congestion] Interpolating Queue Degradation vectors...")
    
    model = xgb.XGBRegressor(n_estimators=150, max_depth=7, learning_rate=0.08, random_state=42)
    model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)
    
    preds = model.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    print(f" -> [XGB Validation Results] Congestion MAE: {mae:.2f}")
    
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, 'xgb_congestion_model.pkl'))
    return model
