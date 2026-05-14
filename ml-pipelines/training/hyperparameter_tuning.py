import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, r2_score, mean_absolute_percentage_error
import xgboost as xgb


def grid_search(
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int = 3,
    n_trials: int = 20,
    random_state: int = 42,
) -> dict:
    tscv = TimeSeriesSplit(n_splits=n_splits)

    param_space = {
        "max_depth": [3, 4, 5, 6, 7],
        "learning_rate": [0.01, 0.05, 0.1, 0.15],
        "n_estimators": [100, 200, 300],
        "subsample": [0.7, 0.8, 0.9, 1.0],
        "colsample_bytree": [0.7, 0.8, 0.9, 1.0],
        "min_child_weight": [1, 3, 5],
    }

    best_score = float("inf")
    best_params: dict = {}
    results: list[dict] = []

    rng = np.random.default_rng(random_state)

    for _ in range(n_trials):
        params = {k: rng.choice(v).item() for k, v in param_space.items()}

        scores: list[float] = []
        for train_idx, val_idx in tscv.split(X):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

            model = xgb.XGBRegressor(
                objective="reg:squarederror",
                random_state=random_state,
                **params,
            )
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            scores.append(mean_absolute_error(y_val, y_pred))

        avg_score = float(np.mean(scores))
        params["mae"] = avg_score
        results.append(params)

        if avg_score < best_score:
            best_score = avg_score
            best_params = {k: v for k, v in params.items() if k != "mae"}

    results.sort(key=lambda x: x["mae"])

    return {
        "best_params": best_params,
        "best_mae": best_score,
        "top_5": results[:5],
        "total_trials": n_trials,
    }


def save_hyperparameter_results(results: dict, output_path: str | None = None) -> str:
    if output_path is None:
        output_path = str(
            Path(__file__).parent.parent / "artifacts" / "hyperparameter_results.json"
        )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    return output_path
