from catboost import CatBoostClassifier
import os


def get_model_path(path: str) -> str:
    MODEL_PATH = path

    return MODEL_PATH

def load_models():
    model_path = get_model_path("../model/balanced_model")
    from_file = CatBoostClassifier()

    return from_file.load_model(model_path)