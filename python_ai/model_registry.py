import os
import joblib
import json
from datetime import datetime
from typing import Optional, Dict, Any

class ModelRegistry:
    """
    Tracks, versions, and loads specific model `.pkl` artifacts natively 
    safeguarding high-speed inference environments explicitly.
    """
    def __init__(self, registry_path: str = "models/"):
        self.registry_path = registry_path
        os.makedirs(self.registry_path, exist_ok=True)
        self.metadata_file = os.path.join(self.registry_path, "registry_metadata.json")
        self._init_registry()

    def _init_registry(self):
        if not os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'w') as f:
                json.dump({"models": {}}, f)

    def save_model(self, model: Any, task_name: str, version: str, metrics: Dict[str, float]):
        """Persists physical models mapping versions securely."""
        filename = f"{task_name}_v{version}.pkl"
        filepath = os.path.join(self.registry_path, filename)
        joblib.dump(model, filepath)
        
        with open(self.metadata_file, 'r+') as f:
            data = json.load(f)
            data["models"][f"{task_name}_v{version}"] = {
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics,
                "file_path": filepath
            }
            f.seek(0)
            json.dump(data, f, indent=4)
            
    def load_model(self, task_name: str, version: str) -> Optional[Any]:
        filepath = os.path.join(self.registry_path, f"{task_name}_v{version}.pkl")
        if os.path.exists(filepath):
            return joblib.load(filepath)
        raise FileNotFoundError(f"Registry failed to locate tracking model: {task_name} version: {version}")
