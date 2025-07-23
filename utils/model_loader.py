import json, os, pickle

class ModelLoader:
    """Tiny helper to load + serve a pickled scikit/xgboost model."""

    def __init__(self, cfg_path="config/model_paths.json"):
        with open(cfg_path, "r", encoding="utf-8") as f:
            self.model_folders = json.load(f)
        self.model = None
        self.current_location = ""
        self.current_name = ""

    def load(self, location:str, pkl_name:str):
        folder = self.model_folders[location]
        path   = os.path.join(folder, pkl_name)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        with open(path, "rb") as f:
            self.model = pickle.load(f)
        self.current_location, self.current_name = location, pkl_name
        return self.model

    def predict(self, X):
        if self.model is None: raise RuntimeError("Load a model first!")
        return self.model.predict(X)
