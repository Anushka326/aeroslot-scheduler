import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, f1_score
import pandas as pd
import os

def evaluate_and_plot(rf_model, xgb_priority, xgb_congestion, X_test, y_test, model_dir):
    print("[Evaluation Engine] Extracting final Test limits natively...")
    
    # Random Forest metrics natively
    rf_preds = rf_model.predict(X_test)
    rf_mae = mean_absolute_error(y_test, rf_preds)
    
    y_test_priority = (y_test > y_test.median()).astype(int)
    prio_preds = xgb_priority.predict(X_test)
    prio_f1 = f1_score(y_test_priority, prio_preds)

    print(f"\n=========================================")
    print(f"      SMART SCHEDULER SYSTEM METRICS     ")
    print(f"=========================================")
    print(f" Random Forest Target Delays: MAE = {rf_mae:.2f}")
    print(f" XGBoost Priority Inference : F1  = {prio_f1:.3f}")
    print(f"=========================================\n")
    
    # Feature Importances plotting boundaries securely locally
    importances = xgb_priority.feature_importances_
    features = X_test.columns
    
    df_imp = pd.DataFrame({'Feature': features, 'Importance': importances})
    df_imp = df_imp.sort_values(by='Importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.barh(df_imp['Feature'], df_imp['Importance'], color='teal')
    plt.gca().invert_yaxis()
    plt.title("XGBoost Predictive Feature Importance bounds (Priority)")
    
    out_plot = os.path.join(model_dir, 'feature_importance.png')
    plt.savefig(out_plot)
    print(f"[Evaluation] Feature Importance map plotted into: {out_plot}")
    
    return df_imp
