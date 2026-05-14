from __future__ import annotations

from pathlib import Path
from typing import Any

import mlflow


class ModelRegistry:
    def __init__(self, tracking_uri: str | None = None) -> None:
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)

    def register(
        self,
        run_id: str,
        artifact_path: str = "xgboost_model",
        model_name: str = "sales_forecast",
        stage: str = "Production",
    ) -> Any:
        result = mlflow.register_model(
            model_uri=f"runs:/{run_id}/{artifact_path}",
            name=model_name,
        )
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name=model_name,
            version=result.version,
            stage=stage,
        )
        return result

    def load_latest(self, model_name: str = "sales_forecast") -> Any:
        return mlflow.pyfunc.load_model(f"models:/{model_name}/Production")

    def get_best_run(self, experiment_name: str, metric: str = "mae") -> str | None:
        client = mlflow.tracking.MlflowClient()
        experiment = client.get_experiment_by_name(experiment_name)
        if experiment is None:
            return None

        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=[f"metrics.{metric} ASC"],
            max_results=1,
        )
        return runs[0].info.run_id if runs else None
