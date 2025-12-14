from datetime import datetime
from typing import Dict, Optional
import json
from pathlib import Path


class ModelVersioning:
\
\
       
    
    def __init__(self, registry_path: str = "./models/registry.json"):
        self.registry_path = Path(registry_path)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict:
                                     
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        return {"models": []}
    
    def _save_registry(self):
                                   
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
    
    def register_model(
        self,
        version: str,
        metrics: Dict[str, float],
        model_path: str,
        metadata: Optional[Dict] = None
    ):
\
\
           
        entry = {
            "version": version,
            "metrics": metrics,
            "model_path": model_path,
            "registered_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.registry["models"].append(entry)
        self._save_registry()
        
        print(f"Registered model {version}")
        print(f"Metrics: {metrics}")
    
    def get_best_model(self, metric: str = "f1") -> Optional[Dict]:
\
\
           
        if not self.registry["models"]:
            return None
        
        best_model = max(
            self.registry["models"],
            key=lambda x: x["metrics"].get(metric, 0)
        )
        
        return best_model
    
    def get_latest_model(self) -> Optional[Dict]:
\
\
           
        if not self.registry["models"]:
            return None
        
        return max(
            self.registry["models"],
            key=lambda x: x["registered_at"]
        )
    
    def list_models(self) -> list:
\
\
           
        return self.registry["models"]
