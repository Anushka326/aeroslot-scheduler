from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import joblib
import os

def train_delay_model(X_train, y_train, X_val, y_val, model_dir):
    print("[Trainer: RF] Booting Random Forest Matrix globally...")
    
    # Utilizing n_jobs=-1 parallelizing processing trees securely locally
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    rmse = root_mean_squared_error(y_val, preds)
    
    print(f" -> [RF Validation Results] MAE: {mae:.2f} | RMSE: {rmse:.2f}")
    
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, 'rf_delay_model.pkl'))
    print(" -> Saved localized payload locally into model_registry.")
    return model
